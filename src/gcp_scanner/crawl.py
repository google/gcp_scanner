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


"""The module to query GCP resources via RestAPI.

"""

import collections
import json
import logging
import io
import sys
from typing import List, Dict, Any, Tuple

from google.cloud import container_v1
import googleapiclient
from googleapiclient import discovery
import requests
from requests.auth import HTTPBasicAuth


def infinite_defaultdict():
  """Initialize infinite default.

  Returns:
    DefaultDict
  """
  return collections.defaultdict(infinite_defaultdict)


def get_bucket_names(project_name: str, service: discovery.Resource,
                     dump_fd: io.TextIOWrapper, dump_iam_policies: bool
                     ) -> Dict[str, Tuple[Any, List[Any]]]:
  """Retrieve a list of buckets available in the project.

  Args:
    project_name: A name of a project to query info about.
    service: A resource object for interacting with the Storage API.
    dump_fd: If set, the function will enumerate files stored in buckets and
      save them in a file corresponding to provided file descriptor.
      This is a very slow, noisy operation and should be used with caution.

  Returns:
    A dictionary where key is bucket name and value is a bucket Object.
  """

  logging.info("Retrieving GCS Buckets")
  buckets_dict = dict()
  # Make an authenticated API request
  request = service.buckets().list(project=project_name)
  while request is not None:
    try:
      response = request.execute()
    except googleapiclient.errors.HttpError:
      logging.info("Failed to list buckets in the %s", project_name)
      logging.info(sys.exc_info())
      break

    for bucket in response.get("items", []):
      buckets_dict[bucket["name"]] = bucket
      if dump_iam_policies is True:
        buckets_dict[bucket["name"]]["iam_policy"] = \
          get_bucket_iam(bucket["name"], service)
      if dump_fd is not None:
        ret_fields = "nextPageToken,items(bucket,name,size,contentType,\
timeCreated)"

        req = service.objects().list(bucket=bucket["name"], fields=ret_fields)

        while req:
          try:
            resp = req.execute()
            for item in resp.get("items", []):
              dump_fd.write(json.dumps(item, indent=2, sort_keys=False))

            req = service.objects().list_next(req, resp)
          except googleapiclient.errors.HttpError:
            logging.info("Failed to read the bucket %s", bucket["name"])
            logging.info(sys.exc_info())
            break

    request = service.buckets().list_next(
        previous_request=request, previous_response=response)

  return buckets_dict

def get_bucket_iam(bucket_name: str, discovery_service: str
                   ) -> List[Any]:
  """Retrieve IAM policies in the bucket.

  Args:
    bucket_name: A name of bucket to query info about.
    discovery_service: An authenticated API request.
  Returns:
    A list with bucket IAM policies.
  """

  logging.info("Retrieving GCS Bucket %s IAM Policy", bucket_name)
  bucket_iam_policies = list()
  request = discovery_service.buckets().getIamPolicy(bucket=bucket_name)
  try:
    response = request.execute()
  except googleapiclient.errors.HttpError:
    logging.info("Failed to IAM Policy in the %s", bucket_name)
    logging.info(sys.exc_info())
    return []

  for bucket_iam_policy in response.get("bindings", []):
    bucket_iam_policies.append(bucket_iam_policy)


  return bucket_iam_policies


def get_gke_clusters(
    project_name: str, gke_client: container_v1.services.cluster_manager.client
    .ClusterManagerClient
) -> List[Tuple[str, str]]:
  """Retrieve a list of GKE clusters available in the project.

  Args:
    project_name: A name of a project to query info about.
    gke_client: I do not know TBD.

  Returns:
    A list of GKE clusters in the project.
  """

  logging.info("Retrieving list of GKE clusters")
  parent = f"projects/{project_name}/locations/-"
  try:
    clusters = gke_client.list_clusters(parent=parent)
    return [(cluster.name, cluster.description)
      for cluster in clusters.clusters]
  except Exception:
    logging.info("Failed to retrieve cluster list for project %s", project_name)
    logging.info(sys.exc_info())
    return []


def get_gke_images(project_name: str, access_token: str) -> Dict[str, Any]:
  """Retrieve a list of GKE images available in the project.

  Args:
    project_name: A name of a project to query info about.
    access_token: An Oauth2 token with permissions to query list of gke images.

  Returns:
    A gke images JSON object for each accessible zone.
  """

  images = dict()
  logging.info("Retrieving list of GKE images")
  project_name = project_name.replace(":", "/")
  regions = ["", "us.", "eu.", "asia."]
  for region in regions:
    gcr_url = f"https://{region}gcr.io/v2/{project_name}/tags/list"
    try:
      res = requests.get(
          gcr_url, auth=HTTPBasicAuth("oauth2accesstoken", access_token),
          timeout=120)
      if not res.ok:
        logging.info("Failed to retrieve gcr images list. Status code: %d",
                     res.status_code)
        continue
      images[region.replace(".", "")] = res.json()
    except Exception:
      logging.info("Failed to retrieve gke images for project %s", project_name)
      logging.info(sys.exc_info())

  return images


def get_endpoints(project_id: str,
                  service: discovery.Resource) -> List[Dict[str, Any]]:
  """Retrieve a list of Endpoints available in the project.

  Args:
    project_id: A name of a project to query info about.
    service: A resource object for interacting with the service management API.

  Returns:
    A list of Endpoints in the project.
  """

  logging.info("Retrieving info about endpoints")
  endpoints_list = list()
  try:
    request = service.services().list(producerProjectId=project_id)
    while request is not None:
      response = request.execute()
      endpoints_list = response.get("services", [])
      request = service.services().list_next(
          previous_request=request, previous_response=response)
  except Exception:
    logging.info("Failed to retrieve endpoints list for project %s", project_id)
    logging.info(sys.exc_info())
  return endpoints_list


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
    for sa_name in entry.get("members", []):
      if sa_name.startswith("serviceAccount") and "@" in sa_name:
        account_name = sa_name.split(":")[1]
        if account_name not in list_of_sas:
          list_of_sas.append(account_name)

  return list_of_sas


def get_service_accounts(project_name: str,
                         service: discovery.Resource) -> List[Tuple[str, str]]:
  """Retrieve a list of service accounts managed in the project.

  Args:
    project_name: A name of a project to query info about.
    service: A resource object for interacting with the IAM API.

  Returns:
    A list of service accounts managed in the project.
  """

  logging.info("Retrieving SA list %s", project_name)
  service_accounts = []

  name = f"projects/{project_name}"

  try:
    request = service.projects().serviceAccounts().list(name=name)
    while request is not None:
      response = request.execute()
      service_accounts = [(service_account["email"],
        service_account.get("description",""))
        for service_account in response.get("accounts",[])]

      request = service.projects().serviceAccounts().list_next(
          previous_request=request, previous_response=response)
  except Exception:
    logging.info("Failed to retrieve SA list for project %s", project_name)
    logging.info(sys.exc_info())

  return service_accounts
