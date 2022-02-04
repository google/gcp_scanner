# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""The main module that initiates scanning of GCP resources.

"""

import argparse
import json
import logging
import os
import sys
from typing import List, Tuple, Optional

import crawl
import credsdb
from google.cloud import container_v1
from google.cloud import iam_credentials
from google.cloud.iam_credentials_v1.services.iam_credentials.client import IAMCredentialsClient
from googleapiclient import discovery
from httplib2 import Credentials
from models import SpiderContext


def crawl_loop(initial_sa_tuples: List[Tuple[str, Credentials, List[str]]],
               out_dir: str,
               target_project: Optional[str] = None,
               force_projects: Optional[str] = None):
  """The main loop function to crawl GCP resources.

  Args:
    initial_sa_tuples: [(sa_name, sa_object, chain_so_far)]
    out_dir: directory to save results
    target_project: project name to scan
    force_projects: a list of projects to force scan
  """

  context = SpiderContext(initial_sa_tuples)
  # Main loop
  processed_sas = set()
  while not context.service_account_queue.empty():
    # Get a new candidate service account / token
    sa_name, credentials, chain_so_far = context.service_account_queue.get()
    if sa_name in processed_sas:
      continue

    # Don't process this service account again
    processed_sas.add(sa_name)
    print('>> current service account: {}'.format(sa_name))
    sa_results = crawl.infinite_defaultdict()
    # Log the chain we used to get here (even if we have no privs)
    sa_results['service_account_chain'] = chain_so_far
    sa_results['current_service_account'] = sa_name

    project_list = crawl.get_project_list(credentials)
    if len(project_list) <= 0:
      print('Unable to list projects accessible from service account')

    # Establish the various Cloud SDK clients
    iam_client = iam_client_for_credentials(credentials)
    compute_client = compute_client_for_credentials(credentials)
    gke_client = gke_client_for_credentials(credentials)

    if force_projects:
      for force_project_id in force_projects:
        res = crawl.fetch_project_info(force_project_id, credentials)
        if res:
          project_list.append(res)

    # Enumerate projects accessible by SA
    for project in project_list:
      if target_project and target_project not in project['projectId']:
        continue

      project_id = project['projectId']
      project_number = project['projectNumber']
      print('Inspecting project {}'.format(project_id))
      project_result = sa_results['projects'][project_id]

      project_result['project_info'] = project
      # Get IAM policy
      iam_policy = crawl.get_iam_policy(project_id, credentials)
      project_result['iam_policy'] = iam_policy

      # Get service accounts
      project_service_accounts = crawl.get_service_accounts(
          project_number, credentials)
      project_result['service_accounts'] = project_service_accounts

      # Iterate over discovered service accounts by attempting impersonation
      project_result['service_account_edges'] = []
      updated_chain = chain_so_far + [sa_name]

      # Get GCP Compute Resources
      compute_instances = crawl.get_compute_instances_names(
          project_id, compute_client)
      compute_images = crawl.get_compute_images_names(project_id,
                                                      compute_client)
      compute_disks = crawl.get_compute_disks_names(project_id, compute_client)
      static_ips = crawl.get_static_ips(project_id, compute_client)
      compute_snapshots = crawl.get_compute_snapshots(project_id,
                                                      compute_client)
      subnets = crawl.get_subnets(project_id, compute_client)
      firewall_rules = crawl.get_firewall_rules(project_id, compute_client)

      project_result['compute_instances'] = compute_instances
      project_result['compute_images'] = compute_images
      project_result['compute_disks'] = compute_disks
      project_result['static_ips'] = static_ips
      project_result['compute_snapshots'] = compute_snapshots
      project_result['subnets'] = subnets
      project_result['firewall_rules'] = firewall_rules

      # Get GCP APP Resources
      project_result['app_services'] = crawl.get_app_services(
          project_id, credentials)

      # Get storage buckets
      storage_buckets = crawl.get_bucket_names(project_id, credentials, False)
      project_result['storage_buckets'] = storage_buckets

      # Get DNS managed zones
      dns_zones = crawl.get_managed_zones(project_id, credentials)
      project_result['managed_zones'] = dns_zones

      # Get GKE resources
      gke_clusters = crawl.get_gke_clusters(project_id, gke_client)
      gke_images = crawl.get_gke_images(project_id, credentials.token)
      project_result['gke_clusters'] = gke_clusters
      project_result['gke_images'] = gke_images

      # Get SQL instances
      project_result['sql_instances'] = crawl.get_sql_instances(
          project_id, credentials)

      # Get BigQuery databases and table names
      project_result['bq'] = crawl.get_bq(project_id, credentials)

      # Get PubSub Subscriptions
      project_result['pubsub_subs'] = crawl.get_pubsub_subscriptions(
          project_id, credentials)

      # Get CloudFunctions list
      project_result['cloud_functions'] = crawl.get_cloudfunctions(
          project_id, credentials)

      # Get List of BigTable Instanses
      project_result['bigtable_instances'] = crawl.get_bigtable_instances(
          project_id, credentials)

      # Get Spanner Instances
      project_result['spanner_instances'] = crawl.get_spanner_instances(
          project_id, credentials)

      # Get CloudStore Instances
      project_result['cloudstore_instances'] = crawl.get_filestore_instances(
          project_id, credentials)

      # Get list of KMS keys
      project_result['kms'] = crawl.get_kms_keys(project_id, credentials)

      # Get information about Endpoints
      project_result['endpoints'] = crawl.get_endpoints(project_id, credentials)

      # Get list of API services enabled in the project
      project_result['services'] = crawl.list_services(project_id, credentials)

      # trying to impersonate SAs within project
      project_service_accounts = crawl.get_associated_service_accounts(
          iam_policy)

      for candidate_service_account in project_service_accounts:
        print('Trying %s' % candidate_service_account)
        if not candidate_service_account.startswith('serviceAccount'):
          continue
        try:
          creds_impersonated = credsdb.impersonate_sa(
              iam_client, candidate_service_account)
          context.service_account_queue.put(
              (candidate_service_account, creds_impersonated, updated_chain))
          project_result['service_account_edges'].append(
              candidate_service_account)
          print('Successfully impersonated %s using %s ' %
                (candidate_service_account, sa_name))
        except Exception:
          logging.info('Failed to get token for %s', candidate_service_account)
          logging.info(sys.exc_info()[1])

    # Write out results to json DB
    logging.info('Saving results into the file')

    sa_results_data = json.dumps(sa_results, indent=2, sort_keys=False)

    with open(out_dir + '/%s.json' % sa_name, 'w') as outfile:
      outfile.write(sa_results_data)


def iam_client_for_credentials(
    credentials: Credentials) -> IAMCredentialsClient:
  return iam_credentials.IAMCredentialsClient(credentials=credentials)


def compute_client_for_credentials(
    credentials: Credentials) -> discovery.Resource:
  return discovery.build(
      'compute', 'v1', credentials=credentials, cache_discovery=False)


def gke_client_for_credentials(
    credentials: Credentials
) -> container_v1.services.cluster_manager.client.ClusterManagerClient:
  return container_v1.services.cluster_manager.ClusterManagerClient(
      credentials=credentials)


def main():
  logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)
  logging.getLogger('googleapiclient.http').setLevel(logging.ERROR)

  parser = argparse.ArgumentParser(
      prog='scanner.py',
      description='GCP Scanner',
      usage='python3 %(prog)s -o folder_to_save_results -g -')
  required_named = parser.add_argument_group('Required parameters')
  required_named.add_argument(
      '-o',
      required=True,
      dest='output',
      default='scan_db',
      help='Path to output directory')

  parser.add_argument(
      '-k',
      '--sa_key_path',
      default=None,
      dest='key_path',
      help='Path to directory with SA keys in json format')
  parser.add_argument(
      '-g',
      '--gcloud_profile_path',
      default=None,
      dest='gcloud_profile_path',
      help='Path to directory with gcloud profile. Specify - to search for credentials in default gcloud config path'
  )
  parser.add_argument(
      '-m',
      default=False,
      dest='use_metadata',
      action='store_true',
      help='Extract credentials from GCE instance metadata')
  parser.add_argument(
      '-at',
      default=None,
      dest='access_token',
      help='Use access token directly to scan GCP resources. Limited by TTL')
  parser.add_argument(
      '-rt',
      default=None,
      dest='refresh_token_files',
      help='A list of comma separated files with refresh_token, client_id, token_uri and client_secret'
  )
  parser.add_argument(
      '-s', default=None, dest='key_name', help='Name of individual SA to scan')
  parser.add_argument(
      '-p',
      default=None,
      dest='target_project',
      help='Name of individual project to scan')
  parser.add_argument(
      '-f',
      default=None,
      dest='force_projects',
      help='Comma separated list of project names to include in the scan')

  parser.add_argument(
      '-l',
      '--logging',
      default='WARNING',
      dest='log_level',
      choices=('INFO', 'WARNING', 'ERROR'),
      help='Set logging level (INFO, WARNING, ERROR)')

  args = parser.parse_args()
  if not args.key_path and not args.gcloud_profile_path and not args.use_metadata \
    and not args.access_token and not args.refresh_token_files:
    print(
        'Please select at least one option to begin scan -k/--sa_key_path,-g/--gcloud_profile_path, -m, -rt, -at'
    )

  force_projects_list = list()
  if args.force_projects:
    force_projects_list = args.force_projects.split(',')

  logging.basicConfig(level=getattr(logging, args.log_level.upper(), None))

  sa_tuples = []
  if args.key_path:
    # extracting SA keys from folder
    for keyfile in os.listdir(args.key_path):
      full_key_path = os.path.join(args.key_path, keyfile)
      account_name, credentials = credsdb.get_creds_from_file(full_key_path)
      if credentials is None:
        logging.info('Failed to retrieve credentials for %s', account_name)
        continue
      sa_tuples.append((account_name, credentials, []))

  if args.use_metadata:
    # extracting GCP credentials from instance metadata
    account_name, credentials = credsdb.get_creds_from_metadata()
    if credentials is None:
      logging.info('Failed to retrieve credentials from metadata')
    else:
      sa_tuples.append((account_name, credentials, []))

  if args.gcloud_profile_path:
    # extracting GCP credentials from gcloud configs
    auths_list = credsdb.get_account_creds_list(args.gcloud_profile_path)

    for accounts in auths_list:
      for creds in accounts:
        # switch between accounts
        account_name = creds.account_name
        account_creds = creds.creds
        access_token = creds.token

        if args.key_name and args.key_name not in account_name:
          continue

        print('Retrieving credentials for %s' % account_name)
        credentials = credsdb.get_creds_from_data(access_token,
                                                  json.loads(account_creds))
        if credentials is None:
          logging.info('Failed to retrieve access token for %s', account_name)
          continue

        sa_tuples.append((account_name, credentials, []))
  if args.access_token:
    credentials = credsdb.credentials_from_token(
        args.access_token,
        None,
        None,
        None,
        None,
        scopes_user='https://www.googleapis.com/auth/cloud-platform')
    if credentials is None:
      logging.info('Failed to retrieve credentials using token provided')
    else:
      sa_tuples.append(('access_token_user_provided', credentials, []))

  if args.refresh_token_files:
    for refresh_token_file in args.refresh_token_files.split(','):
      credentials = credsdb.creds_from_refresh_token(refresh_token_file)

      if credentials is None:
        logging.info('Failed to retrieve credentials using token provided')
      else:
        token_file_name = os.path.basename(refresh_token_file)
        sa_tuples.append((token_file_name, credentials, []))

  crawl_loop(sa_tuples, args.output, args.target_project, force_projects_list)
