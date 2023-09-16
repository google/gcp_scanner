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


"""The main module that initiates scanning of GCP resources."""
import collections
from datetime import datetime
import json
from json.decoder import JSONDecodeError
import logging
import os
from pathlib import Path
import sys
import threading
import time
from typing import Any, Dict, List, Optional, Union

from google.auth.exceptions import MalformedError
from google.cloud import container_v1
from google.cloud import iam_credentials
from google.cloud.iam_credentials_v1.services.iam_credentials.client import IAMCredentialsClient
from httplib2 import Credentials

from . import arguments
from . import credsdb
from . import models
from . import scanner
from .client.client_factory import ClientFactory
from .crawler import misc_crawler
from .crawler.crawler_factory import CrawlerFactory

# We define the schema statically to make it easier for the user and avoid extra
# config files.
LIGHT_VERSION_SCAN_SCHEMA = {
    'compute_instances': [
        'name',
        'zone',
        'machineType',
        'networkInterfaces',
        'status',
    ],
    'compute_images': ['name', 'status', 'diskSizeGb', 'sourceDisk'],
    'machine_images': [
        'name',
        'description',
        'status',
        'sourceInstance',
        'totalStorageBytes',
        'savedDisks',
    ],
    'compute_disks': [
        'name',
        'sizeGb',
        'zone',
        'status',
        'sourceImage',
        'users',
    ],
    'compute_snapshots': ['name', 'status', 'sourceDisk', 'downloadBytes'],
    'managed_zones': ['name', 'dnsName', 'description', 'nameServers'],
    'sql_instances': [
        'name',
        'region',
        'ipAddresses',
        'databaseVersion',
        'state',
    ],
    'cloud_functions': [
        'name',
        'eventTrigger',
        'status',
        'entryPoint',
        'serviceAccountEmail',
    ],
    'kms': ['name', 'primary', 'purpose', 'createTime'],
    'services': ['name'],
}

# The following map is used to establish the relationship between
# crawlers and clients. It determines the appropriate crawler and
# client to be selected from the respective factory classes.
CRAWL_CLIENT_MAP = {
    'app_services': 'appengine',
    'bigtable_instances': 'bigtableadmin',
    'bq': 'bigquery',
    'cloud_functions': 'cloudfunctions',
    'compute_disks': 'compute',
    'compute_images': 'compute',
    'compute_instances': 'compute',
    'compute_snapshots': 'compute',
    'datastore_kinds': 'datastore',
    'dns_policies': 'dns',
    'endpoints': 'servicemanagement',
    'firestore_collections': 'firestore',
    'filestore_instances': 'file',
    'firewall_rules': 'compute',
    'iam_policy': 'cloudresourcemanager',
    'kms': 'cloudkms',
    'machine_images': 'compute',
    'managed_zones': 'dns',
    'pubsub_subs': 'pubsub',
    'registered_domains': 'domains',
    'services': 'serviceusage',
    'service_accounts': 'iam',
    'sourcerepos': 'sourcerepo',
    'spanner_instances': 'spanner',
    'sql_instances': 'sqladmin',
    'static_ips': 'compute',
    'storage_buckets': 'storage',
    'subnets': 'compute',
}


def is_set(config: Optional[dict], config_setting: str) -> Union[dict, bool]:
  if config is None:
    return True
  obj = config.get(config_setting, {})
  return obj.get('fetch', False)


def save_results(res_data: Dict, res_path: str, is_light: bool):
  """The function to save scan results on disk in json format.

  Args:
    res_data: scan results as a dictionary of entries
    res_path: full path to save data in file
    is_light: save only the most interesting results
  """

  if is_light is True:
    # returning the light version of the scan based on predefined schema
    for gcp_resource, schema in LIGHT_VERSION_SCAN_SCHEMA.items():
      projects = res_data.get('projects', {})
      for project_name, project_data in projects.items():
        scan_results = project_data.get(gcp_resource, {})
        light_results = list()
        for scan_result in scan_results:
          light_results.append({key: scan_result.get(key) for key in schema})

        project_data.update({gcp_resource: light_results})
        projects.update({project_name: project_data})
      res_data.update({'projects': projects})

  # Write out results to json DB
  sa_results_data = json.dumps(res_data, indent=2, sort_keys=False)

  with open(res_path, 'a', encoding='utf-8') as outfile:
    outfile.write(sa_results_data)


def get_crawl(
    crawler: Any,
    project_id: str,
    client: Any,
    crawler_config: dict,
    scan_results: dict,
    crawler_name: str,
):
  """The function calls the crawler and returns result in dictionary

  Args:
    crawler: crawler method to start
    project_id: id of a project to scan
    client: appropriate client method
    crawler_config: a dictionary containing specific parameters for a crawler
    scan_results: a dictionary to save scanning results
    crawler_name: name of a crawler

  Returns:
    scan_result: a dictionary with scanning results
  """

  res = crawler.crawl(project_id, client, crawler_config)
  if res is not None and len(res) != 0:
    scan_results[crawler_name] = res
  return scan_results


def get_resources(project: models.ProjectInfo):
  """The function crawls the data for a project and stores the results in a

     dictionary.

  Args:
    project: class to store project scan configration
  """

  if (
      project.target_project
      and project.target_project not in project.project['projectId']
  ):
    return

  project_id = project.project['projectId']
  print(f'Inspecting project {project_id}')
  project_result = dict()

  project_result['project_info'] = project.project
  project_result['service_account_chain'] = project.sa_results[
      'service_account_chain'
  ]
  project_result['current_service_account'] = project.sa_results[
      'current_service_account'
  ]
  project_result['token_scopes'] = project.sa_results['token_scopes']
  project_result['service_account_edges'] = project.sa_results[project_id][
      'service_account_edges'
  ]

  # Fail with error if the output file already exists
  output_file_name = f'{project_id}-{project.scan_time_suffix}.json'
  output_path = Path(project.out_dir, output_file_name)
  gcs_output_path = Path(project.out_dir, f'gcs-{output_file_name}')

  try:
    with open(output_path, 'x', encoding='utf-8'):
      pass

  except FileExistsError:
    logging.error(
        'Try removing the %s file and restart the scanner.', output_file_name
    )

  threads_list = list()
  for crawler_name, client_name in CRAWL_CLIENT_MAP.items():
    if is_set(project.scan_config, crawler_name):
      crawler_config = {}
      if project.scan_config is not None:
        crawler_config = project.scan_config.get(crawler_name)

      # add gcs output path to the config.
      # this path is used by the storage bucket crawler as of now.
      crawler_config['gcs_output_path'] = gcs_output_path

      # crawl the data
      crawler = CrawlerFactory.create_crawler(crawler_name)
      client = ClientFactory.get_client(client_name).get_service(
          project.credentials,
      )

      t = threading.Thread(
          target=get_crawl,
          args=(
              crawler,
              project_id,
              client,
              crawler_config,
              project_result,
              crawler_name,
          ),
      )
      t.daemon = True
      t.start()
      threads_list.append(t)

      while True:
        active_threads = 0
        for t in threads_list:
          if t.is_alive():
            active_threads += 1
        if active_threads >= project.resource_worker_count:
          time.sleep(0.1)
        else:
          break

  for t in threads_list:
    t.join()

  # Call other miscellaneous crawlers here
  if is_set(project.scan_config, 'gke_clusters'):
    gke_client = gke_client_for_credentials(project.credentials)
    res = misc_crawler.get_gke_clusters(
        project_id,
        gke_client,
    )
    if res is not None and len(res) != 0:
      project_result['gke_clusters'] = res
  if is_set(project.scan_config, 'gke_images'):
    res = misc_crawler.get_gke_images(
        project_id,
        project.credentials.token,
    )
    if res is not None and len(res) != 0:
      project_result['gke_images'] = res

  logging.info('Saving results for %s into the file', project_id)
  save_results(project_result, output_path, project.light_scan)


def impersonate_service_accounts(
    context,
    project,
    scan_config,
    sa_results,
    chain_so_far,
    sa_name,
    credentials,
):
  """The function enumerates projects accessible by SA and impersonates them."""

  # Enumerate projects accessible by SA
  project_id = project['projectId']
  print(f'Looking for impersonation options in {project_id}')
  project_result = sa_results['projects'][project_id]
  project_result['project_info'] = project
  # Iterate over discovered service accounts by attempting impersonation
  project_result['service_account_edges'] = []
  updated_chain = chain_so_far + [sa_name]

  if scan_config is not None:
    impers = scan_config.get('service_accounts', None)
  else:
    impers = {'impersonate': False}  # do not impersonate by default

  # trying to impersonate SAs within project
  if impers is not None and impers.get('impersonate', False) is True:
    iam_client = iam_client_for_credentials(credentials)
    if is_set(scan_config, 'iam_policy') is False:
      iam_policy = CrawlerFactory.create_crawler('iam_policy').crawl(
          project_id,
          ClientFactory.get_client('cloudresourcemanager').get_service(
              credentials,
          ),
      )

    project_service_accounts = get_sas_for_impersonation(iam_policy)
    for candidate_service_account in project_service_accounts:
      try:
        logging.info('Trying %s', candidate_service_account)
        creds_impersonated = credsdb.impersonate_sa(
            iam_client, candidate_service_account
        )
        context.service_account_queue.put(
            (candidate_service_account, creds_impersonated, updated_chain)
        )
        project_result['service_account_edges'].append(
            candidate_service_account
        )
        logging.info(
            'Successfully impersonated %s using %s',
            candidate_service_account,
            sa_name,
        )
      except Exception:
        logging.error('Failed to get token for %s', candidate_service_account)
        logging.error(sys.exc_info()[1])


def iam_client_for_credentials(
    credentials: Credentials,
) -> IAMCredentialsClient:
  return iam_credentials.IAMCredentialsClient(credentials=credentials)


def gke_client_for_credentials(
    credentials: Credentials,
) -> container_v1.services.cluster_manager.client.ClusterManagerClient:
  return container_v1.services.cluster_manager.ClusterManagerClient(
      credentials=credentials
  )


def get_sa_details_from_key_files(key_path):
  malformed_keys = []
  sa_details = []
  for keyfile in os.listdir(key_path):
    if not keyfile.endswith('.json'):
      malformed_keys.append(keyfile)
      continue

    full_key_path = os.path.join(key_path, keyfile)
    try:
      account_name, credentials = credsdb.get_creds_from_file(full_key_path)
      if credentials is None:
        logging.error('Failed to retrieve credentials for %s', account_name)
        continue

      sa_details.append((account_name, credentials, []))
    except (MalformedError, JSONDecodeError, Exception):
      malformed_keys.append(keyfile)

  if len(malformed_keys) > 0:
    for malformed_key in malformed_keys:
      logging.error('Failed to parse keyfile: %s', malformed_key)

  return sa_details


def get_sas_for_impersonation(iam_policy: List[Dict[str, Any]]) -> List[str]:
  """Extract a list of unique SAs from IAM policy associated with project.

  Args:
    iam_policy: An IAM policy provided by get_iam_policy function.

  Returns:
    A list of service accounts represented as string
  """

  if not iam_policy:
    return []

  list_of_sas = list()
  for entry in iam_policy:
    for sa_name in entry.get('members', []):
      if sa_name.startswith('serviceAccount') and '@' in sa_name:
        account_name = sa_name.split(':')[1]
        if account_name not in list_of_sas:
          list_of_sas.append(account_name)

  return list_of_sas


def infinite_defaultdict():
  """Initialize infinite default.

  Returns:
    DefaultDict
  """
  return collections.defaultdict(infinite_defaultdict)


def get_sa_tuples(args):
  """The function extracts service account (SA) credentials from various

  sources and returns a list of tuples.
  """

  sa_tuples = []
  if args.key_path:
    # extracting SA keys from folder
    sa_tuples.extend(get_sa_details_from_key_files(args.key_path))

  if args.use_metadata:
    # extracting GCP credentials from instance metadata
    account_name, credentials = credsdb.get_creds_from_metadata()
    if credentials is None:
      logging.error('Failed to retrieve credentials from metadata')
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

        logging.info('Retrieving credentials for %s', account_name)
        credentials = credsdb.get_creds_from_data(
            access_token, json.loads(account_creds)
        )
        if credentials is None:
          logging.error('Failed to retrieve access token for %s', account_name)
          continue

        sa_tuples.append((account_name, credentials, []))

  if args.access_token_files:
    for access_token_file in args.access_token_files.split(','):
      credentials = credsdb.creds_from_access_token(access_token_file)

      if credentials is None:
        logging.error('Failed to retrieve credentials using token provided')
      else:
        token_file_name = os.path.basename(access_token_file)
        sa_tuples.append((token_file_name, credentials, []))

  if args.refresh_token_files:
    for refresh_token_file in args.refresh_token_files.split(','):
      credentials = credsdb.creds_from_refresh_token(refresh_token_file)

      if credentials is None:
        logging.error('Failed to retrieve credentials using token provided')
      else:
        token_file_name = os.path.basename(refresh_token_file)
        sa_tuples.append((token_file_name, credentials, []))

  return sa_tuples


def main():
  """The main scanner loop for GCP Scanner"""

  logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
  logging.getLogger('googleapiclient.http').setLevel(logging.ERROR)

  args = arguments.arg_parser()

  logging.basicConfig(
      level=getattr(logging, args.log_level.upper(), None),
      format='%(asctime)s - %(levelname)s - %(message)s',
      datefmt='%Y-%m-%d %H:%M:%S',
      filename=args.log_file,
      filemode='a',
  )

  force_projects_list = list()
  if args.force_projects:
    force_projects_list = args.force_projects.split(',')

  sa_tuples = scanner.get_sa_tuples(args)

  scan_config = None
  if args.config_path is not None:
    with open(args.config_path, 'r', encoding='utf-8') as f:
      scan_config = json.load(f)

  # Generate current timestamp to append to the filename
  scan_time_suffix = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

  context = models.SpiderContext(sa_tuples)

  project_queue = list()
  processed_sas = set()

  while not context.service_account_queue.empty():
    # Get a new candidate service account / token
    sa_name, credentials, chain_so_far = context.service_account_queue.get()
    if sa_name in processed_sas:
      continue

    # Don't process this service account again
    processed_sas.add(sa_name)

    logging.info('>> current service account: %s', sa_name)
    sa_results = scanner.infinite_defaultdict()
    # Log the chain we used to get here (even if we have no privs)
    sa_results['service_account_chain'] = chain_so_far
    sa_results['current_service_account'] = sa_name
    # Add token scopes in the result
    sa_results['token_scopes'] = credentials.scopes

    project_list = CrawlerFactory.create_crawler(
        'project_list',
    ).crawl(
        ClientFactory.get_client('cloudresourcemanager').get_service(
            credentials
        ),
    )

    if len(project_list) <= 0:
      logging.info('Unable to list projects accessible from service account')

    if force_projects_list:
      for force_project_id in force_projects_list:
        res = CrawlerFactory.create_crawler(
            'project_info',
        ).crawl(
            force_project_id,
            ClientFactory.get_client('cloudresourcemanager').get_service(
                credentials,
            ),
        )
        if res:
          project_list.append(res)
        else:
          # force object creation anyway
          project_list.append(
              {'projectId': force_project_id, 'projectNumber': 'N/A'}
          )

    # Enumerate projects accessible by SA
    for project in project_list:
      project_obj = models.ProjectInfo(
          project,
          sa_results,
          args.output,
          scan_config,
          args.light_scan,
          args.target_project,
          scan_time_suffix,
          sa_name,
          credentials,
          chain_so_far,
          int(args.resource_worker_count),
      )
      project_queue.append(project_obj)
      impersonate_service_accounts(
          context,
          project,
          scan_config,
          sa_results,
          chain_so_far,
          sa_name,
          credentials,
      )

  all_thread_handles = list()

  # See i#267 on why we use the native threading approach here.
  for i, project_obj in enumerate(project_queue):
    print('Finished %d projects out of %d' % (i, len(project_queue) - 1))
    sync_t = threading.Thread(target=scanner.get_resources, args=(project_obj,))
    sync_t.daemon = True
    sync_t.start()
    all_thread_handles.append(sync_t)

    while True:  # enforce explicit block on number of threads
      active_threads = 0
      for t in all_thread_handles:
        if t.is_alive():
          active_threads += 1

      if active_threads >= int(args.project_worker_count):
        time.sleep(0.1)
      else:
        break

  # wait for any threads left to finish
  for t in all_thread_handles:
    t.join()

  return 0
