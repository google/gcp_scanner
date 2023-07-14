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

"""Utilities used in GCP Scanner."""

import json
import collections
import logging
import os
from json.decoder import JSONDecodeError
from typing import List, Dict, Optional, Union, Any

from google.auth.exceptions import MalformedError
from google.cloud import container_v1
from google.cloud import iam_credentials
from google.cloud.iam_credentials_v1.services.iam_credentials.client import IAMCredentialsClient
from googleapiclient import discovery
from httplib2 import Credentials

from . import credsdb


# We define the schema statically to make it easier for the user and avoid extra
# config files.
light_version_scan_schema = {
  'compute_instances': ['name', 'zone', 'machineType', 'networkInterfaces',
                        'status'],
  'compute_images': ['name', 'status', 'diskSizeGb', 'sourceDisk'],
  'machine_images': ['name', 'description', 'status', 'sourceInstance',
                     'totalStorageBytes', 'savedDisks'],
  'compute_disks': ['name', 'sizeGb', 'zone', 'status', 'sourceImage', 'users'],
  'compute_snapshots': ['name', 'status', 'sourceDisk', 'downloadBytes'],
  'managed_zones': ['name', 'dnsName', 'description', 'nameServers'],
  'sql_instances': ['name', 'region', 'ipAddresses', 'databaseVersion',
                    'state'],
  'cloud_functions': ['name', 'eventTrigger', 'status', 'entryPoint',
                      'serviceAccountEmail'],
  'kms': ['name', 'primary', 'purpose', 'createTime'],
  'services': ['name'],
}


def infinite_defaultdict():
  """Initialize infinite default.

  Returns:
    DefaultDict
  """
  return collections.defaultdict(infinite_defaultdict)


def is_set(config: Optional[dict], config_setting: str) -> Union[dict, bool]:
  if config is None:
    return True
  obj = config.get(config_setting, {})
  return obj.get('fetch', False)


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


def get_sas_for_impersonation(
  iam_policy: List[Dict[str, Any]]) -> List[str]:
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


def save_results(res_data: Dict, res_path: str, is_light: bool):
  """The function to save scan results on disk in json format.

  Args:
    res_data: scan results as a dictionary of entries
    res_path: full path to save data in file
    is_light: save only the most interesting results
  """

  if is_light is True:
    # returning the light version of the scan based on predefined schema
    for gcp_resource, schema in light_version_scan_schema.items():
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
