#  Copyright 2023 Google LLC
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import logging

from gcp_scanner.client.appengine_client import AppEngineClient
from gcp_scanner.client.bigquery_client import BQClient
from gcp_scanner.client.bigtable_client import BigTableClient
from gcp_scanner.client.cloud_functions_client import CloudFunctionsClient
from gcp_scanner.client.cloud_resource_manager_client import CloudResourceManagerClient
from gcp_scanner.client.compute_client import ComputeClient
from gcp_scanner.client.datastore_client import DatastoreClient
from gcp_scanner.client.dns_client import DNSClient
from gcp_scanner.client.domains_client import DomainsClient
from gcp_scanner.client.filestore_client import FilestoreClient
from gcp_scanner.client.firestore_client import FirestoreClient
from gcp_scanner.client.iam_client import IAMClient
from gcp_scanner.client.kms_client import CloudKMSClient
from gcp_scanner.client.pubsub_client import PubSubClient
from gcp_scanner.client.service_management_client import ServiceManagementClient
from gcp_scanner.client.serviceusage_client import ServiceUsageClient
from gcp_scanner.client.sourcerepo_client import SourceRepoClient
from gcp_scanner.client.spanner_client import SpannerClient
from gcp_scanner.client.sql_client import SQLClient
from gcp_scanner.client.storage_client import StorageClient


class ClientFactory:
  """Factory class for creating clients."""

  clients = {
    "appengine": AppEngineClient,
    "bigquery": BQClient,
    "bigtableadmin": BigTableClient,
    "cloudfunctions": CloudFunctionsClient,
    "cloudkms": CloudKMSClient,
    "cloudresourcemanager": CloudResourceManagerClient,
    "compute": ComputeClient,
    "datastore": DatastoreClient,
    "domains": DomainsClient,
    "dns": DNSClient,
    "firestore": FirestoreClient,
    "file": FilestoreClient,
    "iam": IAMClient,
    "pubsub": PubSubClient,
    "servicemanagement": ServiceManagementClient,
    "serviceusage": ServiceUsageClient,
    "sourcerepo": SourceRepoClient,
    "spanner": SpannerClient,
    "sqladmin": SQLClient,
    "storage": StorageClient,
  }

  @classmethod
  def get_client(cls, name):
    """Returns the appropriate client."""

    client_cls = cls.clients.get(name.lower())
    if client_cls:
      return client_cls()

    logging.error("Client not supported.")
    return None
