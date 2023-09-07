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

from gcp_scanner.crawler.app_services_crawler import AppServicesCrawler
from gcp_scanner.crawler.bigquery_crawler import BigQueryCrawler
from gcp_scanner.crawler.bigtable_instances_crawler import BigTableInstancesCrawler
from gcp_scanner.crawler.cloud_functions_crawler import CloudFunctionsCrawler
from gcp_scanner.crawler.cloud_resource_manager_iam_policy_crawler import CloudResourceManagerIAMPolicyCrawler
from gcp_scanner.crawler.cloud_resource_manager_project_info_crawler import CloudResourceManagerProjectInfoCrawler
from gcp_scanner.crawler.cloud_resource_manager_project_list_crawler import CloudResourceManagerProjectListCrawler
from gcp_scanner.crawler.compute_disks_crawler import ComputeDisksCrawler
from gcp_scanner.crawler.compute_firewall_rules_crawler import ComputeFirewallRulesCrawler
from gcp_scanner.crawler.compute_images_crawler import ComputeImagesCrawler
from gcp_scanner.crawler.compute_instances_crawler import ComputeInstancesCrawler
from gcp_scanner.crawler.compute_snapshots_crawler import ComputeSnapshotsCrawler
from gcp_scanner.crawler.compute_static_ips_crawler import ComputeStaticIPsCrawler
from gcp_scanner.crawler.compute_subnets_crawler import ComputeSubnetsCrawler
from gcp_scanner.crawler.datastore_crawler import DatastoreCrawler
from gcp_scanner.crawler.dns_managed_zones_crawler import DNSManagedZonesCrawler
from gcp_scanner.crawler.dns_policies_crawler import DNSPoliciesCrawler
from gcp_scanner.crawler.domains_crawler import DomainsCrawler
from gcp_scanner.crawler.endpoints_crawler import EndpointsCrawler
from gcp_scanner.crawler.filestore_instances_crawler import FilestoreInstancesCrawler
from gcp_scanner.crawler.firestore_collections_crawler import FirestoreCollectionsCrawler
from gcp_scanner.crawler.kms_keys_crawler import KMSKeysCrawler
from gcp_scanner.crawler.machine_images_crawler import ComputeMachineImagesCrawler
from gcp_scanner.crawler.pubsub_subscriptions_crawler import PubSubSubscriptionsCrawler
from gcp_scanner.crawler.service_accounts_crawler import ServiceAccountsCrawler
from gcp_scanner.crawler.service_usage_crawler import ServiceUsageCrawler
from gcp_scanner.crawler.source_repo_crawler import CloudSourceRepoCrawler
from gcp_scanner.crawler.spanner_instances_crawler import SpannerInstancesCrawler
from gcp_scanner.crawler.sql_instances_crawler import SQLInstancesCrawler
from gcp_scanner.crawler.storage_buckets_crawler import StorageBucketsCrawler

service_crawler_map = {
  "app_services": AppServicesCrawler,
  "bigtable_instances": BigTableInstancesCrawler,
  "bq": BigQueryCrawler,
  "cloud_functions": CloudFunctionsCrawler,
  "compute_disks": ComputeDisksCrawler,
  "compute_images": ComputeImagesCrawler,
  "compute_instances": ComputeInstancesCrawler,
  "compute_snapshots": ComputeSnapshotsCrawler,
  "datastore_kinds": DatastoreCrawler,
  "dns_policies": DNSPoliciesCrawler,
  "endpoints": EndpointsCrawler,
  "filestore_instances": FilestoreInstancesCrawler,
  "firestore_collections": FirestoreCollectionsCrawler,
  "firewall_rules": ComputeFirewallRulesCrawler,
  "iam_policy": CloudResourceManagerIAMPolicyCrawler,
  "kms": KMSKeysCrawler,
  "machine_images": ComputeMachineImagesCrawler,
  "managed_zones": DNSManagedZonesCrawler,
  "project_info": CloudResourceManagerProjectInfoCrawler,
  "project_list": CloudResourceManagerProjectListCrawler,
  "pubsub_subs": PubSubSubscriptionsCrawler,
  "registered_domains": DomainsCrawler,
  "services": ServiceUsageCrawler,
  "service_accounts": ServiceAccountsCrawler,
  "sourcerepos": CloudSourceRepoCrawler,
  "spanner_instances": SpannerInstancesCrawler,
  "sql_instances": SQLInstancesCrawler,
  "static_ips": ComputeStaticIPsCrawler,
  "storage_buckets": StorageBucketsCrawler,
  "subnets": ComputeSubnetsCrawler,
}


class CrawlerFactory:
  """Factory class for creating crawlers."""

  @classmethod
  def create_crawler(cls, name):
    """Returns the appropriate crawler."""
    if name in service_crawler_map:
      return service_crawler_map[name]()

    logging.error("Crawler not supported.")
    return None
