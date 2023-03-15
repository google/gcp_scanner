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

from crawlers import (ComputeCrawler,
                      DBCrawler,
                      GKECrawler,
                      MQCrawler,
                      NetworkCrawler,
                      ProjectInfoCrawler,
                      SecurityCrawler,
                      ServerlessCrawler,
                      ServiceAccountCrawler,
                      SourceRepoCrawler,
                      StorageCrawler)


def infinite_defaultdict():
  """Initialize infinite default.

  Returns:
    DefaultDict
  """
  return collections.defaultdict(infinite_defaultdict)

class Crawler:

  def __init__(self):
    self._compute_crawler = ComputeCrawler()
    self._db_crawler = DBCrawler()
    self._gke_crawler = GKECrawler()
    self._mq_crawler = MQCrawler()
    self._network_crawler = NetworkCrawler()
    self._project_crawler = ProjectInfoCrawler()
    self._security_crawler = SecurityCrawler()
    self._serverless_crawler = ServerlessCrawler()
    self._service_account_crawler = ServiceAccountCrawler()
    self._source_repo_crawler = SourceRepoCrawler()
    self._storage_crawler = StorageCrawler()
  
  def get_compute_instances_names(
      self,project_name, service):
    return self._compute_crawler.get_compute_instances_names(
      project_name, service)

  def get_compute_images_names(
      self, project_name, service):
    return self._compute_crawler.get_compute_images_names(
      project_name, service)

  def get_compute_disks_names(
      self, project_name, service):
    return self._compute_crawler.get_compute_disks_names(
      project_name, service)

  def get_compute_snapshots(
      self, project_name, service):
    return self._compute_crawler.get_compute_snapshots(
      project_name, service)

  def get_sql_instances(
      self, project_name, credentials):
    return self._db_crawler.get_sql_instances(
      project_name, credentials)

  def get_bq_tables(
      self, project_id, dataset_id, bq_service):
    return self._db_crawler.get_bq_tables(
      project_id, dataset_id, bq_service)

  def get_bq(
      self, project_id, credentials):
    return self._db_crawler.get_bq(
      project_id, credentials)

  def get_bigtable_instances(
      self, project_id, credentials):
    return self._db_crawler.get_bigtable_instances(
      project_id, credentials)

  def get_spanner_instances(
      self, project_id, credentials):
    return self._db_crawler.get_spanner_instances(
      project_id, credentials)

  def get_gke_clusters(
      self, project_name, gke_client):
    return self._gke_crawler.get_gke_clusters(
      project_name, gke_client)

  def get_gke_images(
      self, project_name, access_token):
    return self._gke_crawler.get_gke_images(
      project_name, access_token)

  def get_pubsub_subscriptions(
      self, project_id, credentials):
    return self._mq_crawler.get_pubsub_subscriptions(
      project_id, credentials)

  def get_static_ips(
      self, project_name, service):
    return self._network_crawler.get_static_ips(
      project_name, service)

  def get_subnets(
      self, project_name, compute_client):
    return self._network_crawler.get_subnets(
      project_name, compute_client)

  def get_firewall_rules(
      self, project_name, compute_client):
    return self._network_crawler.get_firewall_rules(
      project_name, compute_client)

  def get_managed_zones(
      self, project_name, credentials):
    return self._network_crawler.get_managed_zones(
      project_name, credentials)

  def get_endpoints(
      self, project_id, credentials):
    return self._network_crawler.get_endpoints(
      project_id, credentials)

  def list_dns_policies(
      self, project_id, credentials):
    return self._network_crawler.list_dns_policies(
      project_id, credentials)

  def fetch_project_info(
      self, project_name, credentials):
    return self._project_crawler.fetch_project_info(
      project_name, credentials)

  def get_project_list(
      self, credentials):
    return self._project_crawler.get_project_list(credentials)

  def get_kms_keys(
      self, project_id, credentials):
    return self._security_crawler.get_kms_keys(
      project_id, credentials)

  def get_iam_policy(
      self, project_name, credentials):
    return self._security_crawler.get_iam_policy(
      project_name, credentials)

  def get_cloudfunctions(
      self, project_id, credentials):
    return self._serverless_crawler.get_cloudfunctions(
      project_id, credentials)

  def get_app_services(
      self, project_name, credentials):
    return self._serverless_crawler.get_app_services(
      project_name, credentials)

  def get_associated_service_accounts(
      self, iam_policy):
    return self._service_account_crawler.get_associated_service_accounts(
      iam_policy)

  def get_service_accounts(
      self, project_name, credentials):
    return self._service_account_crawler.get_service_accounts(
      project_name, credentials)

  def list_services(
      self, project_id, credentials):
    return self._service_account_crawler.list_services(
      project_id, credentials)

  def list_sourcerepo(
      self, project_id, credentials):
    return self._source_repo_crawler.list_sourcerepo(
      project_id, credentials)

  def get_bucket_names(
      self, project_name, credentials, dump_fd):
    return self._storage_crawler.get_bucket_names(
      project_name, credentials, dump_fd)

  def get_filestore_instances(
      self, project_id, credentials):
    return self._storage_crawler.get_filestore_instances(
      project_id, credentials)