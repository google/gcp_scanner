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
from httplib2 import Credentials
import requests
from requests.auth import HTTPBasicAuth


def infinite_defaultdict():
  """Initialize infinite default.

  Returns:
    DefaultDict
  """
  return collections.defaultdict(infinite_defaultdict)


def fetch_project_info(project_name: str,
                       credentials: Credentials) -> Dict[str, Any]:
  """Retrieve information about specific project.

  Args:
    project_name: Name of project to request info about
    credentials: An google.oauth2.credentials.Credentials object.

  Returns:
    Project info object or None.
  """
  project_info = None
  logging.info("Retrieving info about: %s", project_name)

  try:
    service = googleapiclient.discovery.build(
        "cloudresourcemanager",
        "v1",
        credentials=credentials,
        cache_discovery=False)
    request = service.projects().get(projectId=project_name)
    response = request.execute()
    if "projectNumber" in response:
      project_info = response

  except Exception:
    logging.info("Failed to enumerate projects")
    logging.info(sys.exc_info())

  return project_info


def get_project_list(credentials: Credentials) -> List[Dict[str, Any]]:
  """Retrieve a list of projects accessible by credentials provided.

  Args:
    credentials: An google.oauth2.credentials.Credentials object.

  Returns:
    A list of Project objects from cloudresourcemanager RestAPI.
  """

  logging.info("Retrieving projects list")
  project_list = list()
  try:
    service = googleapiclient.discovery.build(
        "cloudresourcemanager",
        "v1",
        credentials=credentials,
        cache_discovery=False)
    request = service.projects().list()
    while request is not None:
      response = request.execute()
      project_list = response.get("projects",[])
      request = service.projects().list_next(
          previous_request=request, previous_response=response)
  except Exception:
    logging.info("Failed to enumerate projects")
    logging.info(sys.exc_info())
  return project_list


def get_compute_instances_names(
    project_name: str, service: discovery.Resource) -> List[Dict[str, Any]]:
  """Retrieve a list of Compute VMs available in the project.

  Args:
    project_name: A name of a project to query info about.
    service: A resource object for interacting with the Compute API.

  Returns:
    A list of instance objects.
  """

  logging.info("Retrieving list of Compute Instances")
  images_result = list()
  try:
    request = service.instances().aggregatedList(project=project_name)
    while request is not None:
      response = request.execute()
      if response.get("items", None) is not None:
        images_result = [instance
          for _, instances_scoped_list in response["items"].items()
          for instance in instances_scoped_list.get("instances",[])]
      request = service.instances().aggregatedList_next(
          previous_request=request, previous_response=response)
  except Exception:
    logging.info("Failed to enumerate compute instances in the %s",
                 project_name)
    logging.info(sys.exc_info())
  return images_result


def get_compute_images_names(
    project_name: str, service: discovery.Resource) -> List[Dict[str, Any]]:
  """Retrieve a list of Compute images available in the project.

  Args:
    project_name: A name of a project to query info about.
    service: A resource object for interacting with the Compute API.

  Returns:
    A list of image objects.
  """

  logging.info("Retrieving list of Compute Image names")
  images_result = list()
  try:
    request = service.images().list(project=project_name)
    while request is not None:
      response = request.execute()
      images_result = response.get("items", [])
      request = service.images().list_next(
          previous_request=request, previous_response=response)
  except Exception:
    logging.info("Failed to enumerate compute images in the %s", project_name)
    logging.info(sys.exc_info())
  return images_result


def get_machine_images(
    project_name: str, service: discovery.Resource) -> List[Dict[str, Any]]:
  """Retrieve a list of Machine Images Resources available in the project.

  Args:
    project_name: A name of a project to query info about.
    service: A resource object for interacting with the Compute API.

  Returns:
    A list of machine image resources.
  """

  logging.info("Retrieving list of Machine Images Resources")
  machine_images_list = list()
  try:
    request = service.machineImages().list(project=project_name)
    while request is not None:
      response = request.execute()
      machine_images_list = response.get("items", [])
      request = service.machineImages().list_next(
        previous_request=request, previous_response=response
      )
  except Exception:
    logging.info("Failed to enumerate machine images in the %s", project_name)
    logging.info(sys.exc_info())
  return machine_images_list


def get_compute_disks_names(
    project_name: str, service: discovery.Resource) -> List[Dict[str, Any]]:
  """Retrieve a list of Compute disks available in the project.

  Args:
    project_name: A name of a project to query info about.
    service: A resource object for interacting with the Compute API.

  Returns:
    A list of disk objects.
  """

  logging.info("Retrieving list of Compute Disk names")
  disk_names_list = list()
  try:
    request = service.disks().aggregatedList(project=project_name)
    while request is not None:
      response = request.execute()
      if response.get("items", None) is not None:
        disk_names_list = [disk
          for _, disks_scoped_list in response["items"].items()
          for disk in disks_scoped_list.get("disks", [])]
      request = service.disks().aggregatedList_next(
          previous_request=request, previous_response=response)
  except Exception:
    logging.info("Failed to enumerate compute disks in the %s", project_name)
    logging.info(sys.exc_info())

  return disk_names_list


def get_static_ips(project_name: str,
                   service: discovery.Resource) -> List[Dict[str, Any]]:
  """Retrieve a list of static IPs available in the project.

  Args:
    project_name: A name of a project to query info about.
    service: A resource object for interacting with the Compute API.

  Returns:
    A list of static IPs in the project.
  """

  logging.info("Retrieving Static IPs")

  ips_list = list()
  try:
    request = service.addresses().aggregatedList(project=project_name)
    while request is not None:
      response = request.execute()
      ips_list = [{name: addresses_scoped_list}
        for name, addresses_scoped_list in response["items"].items()
        if addresses_scoped_list.get("addresses", None) is not None]
      request = service.addresses().aggregatedList_next(
          previous_request=request, previous_response=response)
  except Exception:
    logging.info("Failed to get static IPs in the %s", project_name)
    logging.info(sys.exc_info())

  return ips_list


def get_compute_snapshots(project_name: str,
                          service: discovery.Resource) -> List[Dict[str, Any]]:
  """Retrieve a list of Compute snapshots available in the project.

  Args:
    project_name: A name of a project to query info about.
    service: A resource object for interacting with the Compute API.

  Returns:
    A list of snapshot objects.
  """

  logging.info("Retrieving Compute Snapshots")
  snapshots_list = list()
  try:
    request = service.snapshots().list(project=project_name)
    while request is not None:
      response = request.execute()
      snapshots_list = response.get("items", [])
      request = service.snapshots().list_next(
          previous_request=request, previous_response=response)
  except Exception:
    logging.info("Failed to get compute snapshots in the %s", project_name)
    logging.info(sys.exc_info())

  return snapshots_list


def get_subnets(project_name: str,
                compute_client: discovery.Resource) -> List[Dict[str, Any]]:
  """Retrieve a list of subnets available in the project.

  Args:
    project_name: A name of a project to query info about.
    compute_client: A resource object for interacting with the Compute API.

  Returns:
    A list of subnets in the project.
  """

  logging.info("Retrieving Subnets")
  subnets_list = list()
  try:
    request = compute_client.subnetworks().aggregatedList(project=project_name)
    while request is not None:
      response = request.execute()
      if response.get("items", None) is not None:
        subnets_list = list(response["items"].items())
      request = compute_client.subnetworks().aggregatedList_next(
          previous_request=request, previous_response=response)
  except Exception:
    logging.info("Failed to get subnets in the %s", project_name)
    logging.info(sys.exc_info())

  return subnets_list


def get_firewall_rules(
    project_name: str,
    compute_client: discovery.Resource) -> List[Dict[str, Any]]:
  """Retrieve a list of firewall rules in the project.

  Args:
    project_name: A name of a project to query info about.
    compute_client: A resource object for interacting with the Compute API.

  Returns:
    A list of firewall rules in the project.
  """

  logging.info("Retrieving Firewall Rules")
  firewall_rules_list = list()
  try:
    request = compute_client.firewalls().list(project=project_name)
    while request is not None:
      response = request.execute()
      firewall_rules_list=[(firewall["name"],)
        for firewall in response.get("items",[])]
      request = compute_client.firewalls().list_next(
          previous_request=request, previous_response=response)
  except Exception:
    logging.info("Failed to get firewall rules in the %s", project_name)
    logging.info(sys.exc_info())
  return firewall_rules_list


def get_bucket_names(project_name: str, credentials: Credentials,
                     dump_fd: io.TextIOWrapper
                     ) -> Dict[str, Tuple[Any, List[Any]]]:
  """Retrieve a list of buckets available in the project.

  Args:
    project_name: A name of a project to query info about.
    credentials: An google.oauth2.credentials.Credentials object.
    dump_fd: If set, the function will enumerate files stored in buckets and
      save them in a file corresponding to provided file descriptor.
      This is a very slow, noisy operation and should be used with caution.

  Returns:
    A dictionary where key is bucket name and value is a bucket Object.
  """

  logging.info("Retrieving GCS Buckets")
  buckets_dict = dict()
  service = discovery.build(
      "storage", "v1", credentials=credentials, cache_discovery=False)
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


def get_managed_zones(project_name: str,
                      service: discovery.Resource) -> List[Dict[str, Any]]:
  """Retrieve a list of DNS zones available in the project.

  Args:
    project_name: A name of a project to query info about.
    credentials: An google.oauth2.credentials.Credentials object.

  Returns:
    A list of DNS zones in the project.
  """

  logging.info("Retrieving DNS Managed Zones")
  zones_list = list()

  try:
    request = service.managedZones().list(project=project_name)
    while request is not None:
      response = request.execute()
      zones_list = response.get("managedZones",[])
      request = service.managedZones().list_next(
          previous_request=request, previous_response=response)
  except Exception:
    logging.info("Failed to enumerate DNS zones for project %s", project_name)
    logging.info(sys.exc_info())

  return zones_list


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


def get_sql_instances(project_name: str,
                      credentials: Credentials) -> List[Dict[str, Any]]:
  """Retrieve a list of SQL instances available in the project.

  Args:
    project_name: A name of a project to query info about.
    credentials: An google.oauth2.credentials.Credentials object.

  Returns:
    A list of sql instances in the project.
  """

  logging.info("Retrieving CloudSQL Instances")
  sql_instances_list = list()
  try:
    service = discovery.build(
        "sqladmin", "v1beta4", credentials=credentials, cache_discovery=False)

    request = service.instances().list(project=project_name)
    while request is not None:
      response = request.execute()
      sql_instances_list = response.get("items", [])
      request = service.instances().list_next(
          previous_request=request, previous_response=response)
  except Exception:
    logging.info("Failed to get SQL instances for project %s", project_name)
    logging.info(sys.exc_info())

  return sql_instances_list


def get_bq_tables(project_id: str, dataset_id: str,
                  bq_service: discovery.Resource) -> List[Dict[str, Any]]:
  """Retrieve a list of BigQuery tables available in the dataset.

  Args:
    project_id: A name of a project to query info about.
    dataset_id: A name of dataset to query data from.
    bq_service: I do not know.

  Returns:
    A list of BigQuery tables in the dataset.
  """

  logging.info("Retrieving BigQuery Tables for dataset %s", dataset_id)
  list_of_tables = list()
  try:
    request = bq_service.tables().list(
        projectId=project_id, datasetId=dataset_id)
    while request is not None:
      response = request.execute()
      list_of_tables = response.get("tables", [])
      request = bq_service.tables().list_next(
          previous_request=request, previous_response=response)
  except Exception:
    logging.info("Failed to retrieve BQ tables for dataset %s", dataset_id)
    logging.info(sys.exc_info())
  return list_of_tables


def get_bq(project_id: str,
           credentials: Credentials) -> Dict[str, List[Dict[str, Any]]]:
  """Retrieve a list of BigQuery datasets available in the project.

  Args:
    project_id: A name of a project to query info about.
    credentials: An google.oauth2.credentials.Credentials object.

  Returns:
    A dictionary of BigQuery dataset and corresponding tables.
  """

  logging.info("Retrieving BigQuery Datasets")
  bq_datasets = dict()
  try:
    service = discovery.build(
        "bigquery", "v2", credentials=credentials, cache_discovery=False)

    request = service.datasets().list(projectId=project_id)
    while request is not None:
      response = request.execute()

      for dataset in response.get("datasets", []):
        dataset_id = dataset["datasetReference"]["datasetId"]
        bq_datasets[dataset_id] = get_bq_tables(project_id,dataset_id, service)

      request = service.datasets().list_next(
          previous_request=request, previous_response=response)
  except Exception:
    logging.info("Failed to retrieve BQ datasets for project %s", project_id)
    logging.info(sys.exc_info())
  return bq_datasets


def get_pubsub_subscriptions(project_id: str,
                             credentials: Credentials) -> List[Dict[str, Any]]:
  """Retrieve a list of PubSub subscriptions available in the project.

  Args:
    project_id: A name of a project to query info about.
    credentials: An google.oauth2.credentials.Credentials object.

  Returns:
    A list of PubSub subscriptions in the project.
  """

  logging.info("Retrieving PubSub Subscriptions")
  pubsubs_list = list()
  try:
    service = discovery.build(
        "pubsub", "v1", credentials=credentials, cache_discovery=False)

    request = service.projects().subscriptions().list(
        project=f"projects/{project_id}")
    while request is not None:
      response = request.execute()
      pubsubs_list = response.get("subscriptions", [])
      request = service.projects().subscriptions().list_next(
          previous_request=request, previous_response=response)
  except Exception:
    logging.info("Failed to get PubSubs for project %s", project_id)
    logging.info(sys.exc_info())
  return pubsubs_list


def get_cloudfunctions(project_id: str,
                       credentials: Credentials) -> List[Dict[str, Any]]:
  """Retrieve a list of CloudFunctions available in the project.

  Args:
    project_id: A name of a project to query info about.
    credentials: An google.oauth2.credentials.Credentials object.

  Returns:
    A list of CloudFunctions in the project.
  """

  logging.info("Retrieving CloudFunctions")
  functions_list = list()
  service = discovery.build(
      "cloudfunctions", "v1", credentials=credentials, cache_discovery=False)
  try:
    request = service.projects().locations().functions().list(
        parent=f"projects/{project_id}/locations/-")
    while request is not None:
      response = request.execute()
      functions_list = response.get("functions", [])
      request = service.projects().locations().functions().list_next(
          previous_request=request, previous_response=response)
  except Exception:
    logging.info("Failed to retrieve CloudFunctions for project %s", project_id)
    logging.info(sys.exc_info())

  return functions_list


def get_bigtable_instances(project_id: str,
                           credentials: Credentials) -> List[Dict[str, Any]]:
  """Retrieve a list of BigTable instances available in the project.

  Args:
    project_id: A name of a project to query info about.
    credentials: An google.oauth2.credentials.Credentials object.

  Returns:
    A list of BigTable instances in the project.
  """

  logging.info("Retrieving bigtable instances")
  bigtable_instances_list = list()
  try:
    service = discovery.build(
        "bigtableadmin", "v2", credentials=credentials, cache_discovery=False)

    request = service.projects().instances().list(
        parent=f"projects/{project_id}")
    while request is not None:
      response = request.execute()
      bigtable_instances_list = response.get("instances", [])
      request = service.projects().instances().list_next(
          previous_request=request, previous_response=response)
  except Exception:
    logging.info("Failed to retrieve BigTable instances for project %s",
                 project_id)
    logging.info(sys.exc_info())
  return bigtable_instances_list


def get_spanner_instances(project_id: str,
                          credentials: Credentials) -> List[Dict[str, Any]]:
  """Retrieve a list of Spanner instances available in the project.

  Args:
    project_id: A name of a project to query info about.
    credentials: An google.oauth2.credentials.Credentials object.

  Returns:
    A list of Spanner instances in the project.
  """

  logging.info("Retrieving spanner instances")
  spanner_instances_list = list()
  try:
    service = discovery.build(
        "spanner", "v1", credentials=credentials, cache_discovery=False)

    request = service.projects().instances().list(
        parent=f"projects/{project_id}")
    while request is not None:
      response = request.execute()
      spanner_instances_list = response.get("instances", [])
      request = service.projects().instances().list_next(
          previous_request=request, previous_response=response)
  except Exception:
    logging.info("Failed to retrieve Spanner instances for project %s",
                 project_id)
    logging.info(sys.exc_info())
  return spanner_instances_list


def get_filestore_instances(project_id: str,
                            credentials: Credentials) -> List[Dict[str, Any]]:
  """Retrieve a list of Filestore instances available in the project.

  Args:
    project_id: A name of a project to query info about.
    credentials: An google.oauth2.credentials.Credentials object.

  Returns:
    A list of Filestore instances in the project.
  """

  logging.info("Retrieving filestore instances")
  filestore_instances_list = list()
  service = discovery.build(
      "file", "v1", credentials=credentials, cache_discovery=False)
  try:
    request = service.projects().locations().instances().list(
        parent=f"projects/{project_id}/locations/-")
    while request is not None:
      response = request.execute()
      filestore_instances_list = response.get("instances", [])
      request = service.projects().locations().instances().list_next(
          previous_request=request, previous_response=response)
  except Exception:
    logging.info("Failed to get filestore instances for project %s", project_id)
    logging.info(sys.exc_info())
  return filestore_instances_list


def get_kms_keys(project_id: str,
                 credentials: Credentials) -> List[Dict[str, Any]]:
  """Retrieve a list of KMS keys available in the project.

  Args:
    project_id: A name of a project to query info about.
    credentials: An google.oauth2.credentials.Credentials object.

  Returns:
    A list of KMS keys in the project.
  """

  logging.info("Retrieving KMS keys")
  kms_keys_list = list()
  try:
    service = discovery.build(
        "cloudkms", "v1", credentials=credentials, cache_discovery=False)

    # list all possible locations
    locations_list = list()
    request = service.projects().locations().list(name=f"projects/{project_id}")
    while request is not None:
      response = request.execute()
      for location in response.get("locations", []):
        locations_list.append(location["locationId"])
      request = service.projects().locations().list_next(
          previous_request=request, previous_response=response)

    for location_id in locations_list:
      request_loc = service.projects().locations().keyRings().list(
          parent=f"projects/{project_id}/locations/{location_id}")
      while request_loc is not None:
        response_loc = request_loc.execute()
        for keyring in response_loc.get("keyRings", []):
          request = service.projects().locations().keyRings().cryptoKeys().list(
              parent=keyring["name"])
          while request is not None:
            response = request.execute()
            for key in response.get("cryptoKeys", []):
              kms_keys_list.append(key)

            request = service.projects().locations().keyRings().cryptoKeys(
            ).list_next(
                previous_request=request, previous_response=response)

        request_loc = service.projects().locations().keyRings().list_next(
            previous_request=request, previous_response=response)
  except Exception:
    logging.info("Failed to retrieve KMS keys for project %s", project_id)
    logging.info(sys.exc_info())
  return kms_keys_list


def get_app_services(project_name: str,
                     credentials: Credentials) -> Dict[str, Any]:
  """Retrieve a list of AppEngine instances available in the project.

  Args:
    project_name: A name of a project to query info about.
    credentials: An google.oauth2.credentials.Credentials object.

  Returns:
    A dict representing default apps and services available in the project.
  """

  app_client = discovery.build(
      "appengine", "v1", credentials=credentials, cache_discovery=False)

  logging.info("Retrieving app services")
  app_services = dict()
  try:
    request = app_client.apps().get(appsId=project_name)
    response = request.execute()
    if response.get("name", None) is not None:
      app_services["default_app"] = (response["name"],
                                     response["defaultHostname"],
                                     response["servingStatus"])

    request = app_client.apps().services().list(appsId=project_name)

    app_services["services"] = list()
    while request is not None:
      response = request.execute()
      app_services["services"] = response.get("services", [])
      request = app_client.apps().services().list_next(
          previous_request=request, previous_response=response)
  except Exception:
    logging.info("Failed to retrieve App services for project %s", project_name)
    logging.info(sys.exc_info())
  return app_services


def get_endpoints(project_id: str,
                  credentials: Credentials) -> List[Dict[str, Any]]:
  """Retrieve a list of Endpoints available in the project.

  Args:
    project_id: A name of a project to query info about.
    credentials: An google.oauth2.credentials.Credentials object.

  Returns:
    A list of Endpoints in the project.
  """

  logging.info("Retrieving info about endpoints")
  endpoints_list = list()
  try:
    service = discovery.build(
        "servicemanagement",
        "v1",
        credentials=credentials,
        cache_discovery=False)

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


def get_iam_policy(project_name: str,
                   credentials: Credentials) -> List[Dict[str, Any]]:
  """Retrieve an IAM Policy in the project.

  Args:
    project_name: A name of a project to query info about.
    credentials: An google.oauth2.credentials.Credentials object.

  Returns:
    An IAM policy enforced for the project.
  """

  logging.info("Retrieving IAM policy for %s", project_name)
  service = discovery.build(
      "cloudresourcemanager",
      "v1",
      credentials=credentials,
      cache_discovery=False)

  resource = project_name

  get_policy_options = {
      "requestedPolicyVersion": 3,
  }
  get_policy_options = {"options": {"requestedPolicyVersion": 3}}
  try:
    request = service.projects().getIamPolicy(
        resource=resource, body=get_policy_options)
    response = request.execute()
  except Exception:
    logging.info("Failed to get endpoints list for project %s", project_name)
    logging.info(sys.exc_info())
    return None

  if response.get("bindings", None) is not None:
    return response["bindings"]
  else:
    return None


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
                         credentials: Credentials) -> List[Tuple[str, str]]:
  """Retrieve a list of service accounts managed in the project.

  Args:
    project_name: A name of a project to query info about.
    credentials: An google.oauth2.credentials.Credentials object.

  Returns:
    A list of service accounts managed in the project.
  """

  logging.info("Retrieving SA list %s", project_name)
  service_accounts = []
  service = discovery.build(
      "iam", "v1", credentials=credentials, cache_discovery=False)

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


def list_services(project_id: str, credentials: Credentials) -> List[Any]:
  """Retrieve a list of services enabled in the project.

  Args:
    project_id: An id of a project to query info about.
    credentials: An google.oauth2.credentials.Credentials object.

  Returns:
    A list of service API objects enabled in the project.
  """

  logging.info("Retrieving services list %s", project_id)
  list_of_services = list()
  serviceusage = discovery.build("serviceusage", "v1", credentials=credentials)

  request = serviceusage.services().list(
      parent="projects/" + project_id, pageSize=200, filter="state:ENABLED")
  try:
    while request is not None:
      response = request.execute()
      list_of_services.extend(response.get("services", []))

      request = serviceusage.services().list_next(
          previous_request=request, previous_response=response)
  except Exception:
    logging.info("Failed to retrieve services for project %s", project_id)
    logging.info(sys.exc_info())

  return list_of_services


def list_sourcerepo(project_id: str, credentials: Credentials) -> List[Any]:
  """Retrieve a list of cloud source repositories enabled in the project.

  Args:
    project_id: An id of a project to query info about.
    credentials: An google.oauth2.credentials.Credentials object.

  Returns:
    A list of cloud source repositories in the project.
  """

  logging.info("Retrieving cloud source repositories %s", project_id)
  list_of_repos = list()
  service = discovery.build("sourcerepo", "v1", credentials=credentials)

  request = service.projects().repos().list(
    name="projects/" + project_id,
    pageSize=500
  )
  try:
    while request is not None:
      response = request.execute()
      list_of_repos.extend(response.get("repos", None))

      request = service.projects().repos().list_next(
        previous_request=request,
        previous_response=response
      )
  except Exception:
    logging.info("Failed to retrieve source repos for project %s", project_id)
    logging.info(sys.exc_info())

  return list_of_repos


def list_dns_policies(project_id: str,
                      service: discovery.Resource) -> List[Any]:
  """Retrieve a list of cloud DNS policies in the project.
  Args:
    project_id: An id of a project to query info about.
    credentials: An google.oauth2.credentials.Credentials object.
  Returns:
    A list of cloud DNS policies in the project.
  """

  logging.info("Retrieving cloud DNS policies %s", project_id)
  list_of_policies = list()

  request = service.policies().list(
    project=project_id,
    maxResults=500
  )
  try:
    while request is not None:
      response = request.execute()
      list_of_policies.extend(response.get("policies", None))

      request = service.policies().list_next(
        previous_request=request,
        previous_response=response
      )
  except Exception:
    logging.info("Failed to retrieve DNS policies for project %s", project_id)
    logging.info(sys.exc_info())

  return list_of_policies

