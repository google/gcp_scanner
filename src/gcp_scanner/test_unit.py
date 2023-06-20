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

"""The module to perform unit tests of the GCP Scanner.

"""

import datetime
import difflib
import filecmp
import json
import logging
import os
import shutil
import sqlite3
import unittest
from unittest.mock import patch, Mock

import requests
from google.oauth2 import credentials


from . import crawl
from . import credsdb
from . import scanner
from .client.appengine_client import AppEngineClient
from .client.bigquery_client import BQClient
from .client.bigtable_client import BigTableClient
from .client.client_factory import ClientFactory
from .client.cloud_functions_client import CloudFunctionsClient
from .client.cloud_source_manager_client import CloudSourceManagerClient
from .client.compute_client import ComputeClient
from .client.dns_client import DNSClient
from .client.filestore_client import FilestoreClient
from .client.iam_client import IAMClient
from .client.kms_client import CloudKMSClient
from .client.pubsub_client import PubSubClient
from .client.service_management_client import ServiceManagementClient
from .client.serviceusage_client import ServiceUsageClient
from .client.sourcerepo_client import SourceRepoClient
from .client.spanner_client import SpannerClient
from .client.sql_client import SQLClient
from .client.storage_client import StorageClient
from .crawler.app_services_crawler import AppServicesCrawler
from .crawler.cloud_functions_crawler import CloudFunctionsCrawler
from .crawler.bigtable_instances_crawler import BigTableInstancesCrawler
from .crawler.compute_disks_crawler import ComputeDisksCrawler
from .crawler.compute_firewall_rules_crawler import ComputeFirewallRulesCrawler
from .crawler.compute_images_crawler import ComputeImagesCrawler
from .crawler.compute_instances_crawler import ComputeInstancesCrawler
from .crawler.compute_snapshots_crawler import ComputeSnapshotsCrawler
from .crawler.compute_static_ips_crawler import ComputeStaticIPsCrawler
from .crawler.compute_subnets_crawler import ComputeSubnetsCrawler
from .crawler.crawler_factory import CrawlerFactory
from .crawler.filestore_instances_crawler import FilestoreInstancesCrawler
from .crawler.dns_managed_zones_crawler import DNSManagedZonesCrawler
from .crawler.dns_policies_crawler import DNSPoliciesCrawler
from .crawler.machine_images_crawler import ComputeMachineImagesCrawler
from .crawler.sql_instances_crawler import SQLInstancesCrawler
from .crawler.spanner_instances_crawler import SpannerInstancesCrawler
from .crawler.pubsub_subscriptions_crawler import PubSubSubscriptionsCrawler
from .credsdb import get_scopes_from_refresh_token

PROJECT_NAME = "test-gcp-scanner-2"


def print_diff(f1, f2):
  with open(f1, "r", encoding="utf-8") as file_1:
    file_1_text = file_1.readlines()

  with open(f2, "r", encoding="utf-8") as file_2:
    file_2_text = file_2.readlines()

  # Find and print the diff:
  res = ""
  for line in difflib.unified_diff(file_1_text, file_2_text, fromfile=f1,
                                   tofile=f2, lineterm=""):
    print(line)
    res += line


def save_to_test_file(res):
  res = json.dumps(res, indent=2, sort_keys=False)
  with open("test_res", "w", encoding="utf-8") as outfile:
    outfile.write(res)


def compare_volatile(f1, f2):
  res = True
  with open(f1, "r", encoding="utf-8") as file_1:
    file_1_text = file_1.read()

  with open(f2, "r", encoding="utf-8") as file_2:
    file_2_text = file_2.readlines()

  for line in file_2_text:
    if not line.startswith("CHECK"):
      continue  # we compare only important part of output
    line = line.replace("CHECK", "")
    line = line.strip()
    if line in file_1_text:
      continue
    else:
      print(f"The following line was not identified in the output:\n{line}")
      res = False

  if res is False:
    print(file_1_text)
  return res


def verify(res_to_verify, resource_type, volatile=True):
  save_to_test_file(res_to_verify)
  f1 = "test_res"
  f2 = f"test/{resource_type}"

  if volatile is True:
    result = compare_volatile(f1, f2)
  else:
    result = filecmp.cmp(f1, f2)
    if result is False:
      print_diff(f1, f2)

  return result


def test_creds_fetching():
  os.mkdir("unit")
  conn = sqlite3.connect("unit/credentials.db")
  c = conn.cursor()
  c.execute("""
           CREATE TABLE credentials (account_id TEXT PRIMARY KEY, value BLOB)
            """)
  sqlite_insert_with_param = """INSERT INTO "credentials"
                                ("account_id", "value")
                                VALUES (?, ?);"""

  data_value = ("test_account@gmail.com", "test_data")
  c.execute(sqlite_insert_with_param, data_value)
  conn.commit()

  assert str(credsdb.find_creds("./unit")) == "['./unit/credentials.db']"

  conn = sqlite3.connect("unit/access_tokens.db")
  c = conn.cursor()
  c.execute("""
            CREATE TABLE IF NOT EXISTS access_tokens
            (account_id TEXT PRIMARY KEY,
             access_token TEXT, token_expiry TIMESTAMP, 
             rapt_token TEXT, id_token TEXT)
            """)

  valid_tm = datetime.datetime.now() + datetime.timedelta(hours=2, minutes=10)
  expired_tm = datetime.datetime.now() - datetime.timedelta(hours=2, minutes=10)
  sqlite_insert_with_param = """INSERT INTO "access_tokens"
                                ("account_id", "access_token",
                                 "token_expiry", "rapt_token", "id_token")
                                VALUES (?, ?, ?, ?, ?);"""

  data_value = ("test_account@gmail.com", "ya.29c.TEST",
                valid_tm, "test", "test2")
  c.execute(sqlite_insert_with_param, data_value)
  data_value = ("test_account2@gmail.com", "ya.29c.TEST",
                expired_tm, "test", "test2")
  c.execute(sqlite_insert_with_param, data_value)
  conn.commit()

  assert str(credsdb.get_access_tokens_dict("./unit/credentials.db")) == \
         "{'test_account@gmail.com': 'ya.29c.TEST'}"

  res = str(credsdb.extract_creds("./unit/credentials.db"))
  print(res)
  assert res == "[SA(account_name='test_account@gmail.com', \
creds='test_data', token='ya.29c.TEST')]"

  res = credsdb.get_account_creds_list("./unit")
  print(str(res))
  assert str(credsdb.get_account_creds_list("./unit")) == \
         "[[SA(account_name='test_account@gmail.com', \
creds='test_data', token='ya.29c.TEST')]]"

  # impersonate_sa()
  shutil.rmtree("unit")


class TestScopes(unittest.TestCase):
  """Test fetching scopes from a refresh token."""

  def setUp(self):
    """Setup common variables."""
    self.ctx = {
      "refresh_token": "<token>",
      "client_id": "id",
      "client_secret": "secret",
    }

  @patch("requests.post")
  def test_get_scope_from_rt(self, mocked_post):
    """Test get_scope_from_rt valid."""
    scope_str = "scope1 scope2 scope3 openid"
    mocked_post.return_value = Mock(
      status_code=201,
      json=lambda: {
        "scope": scope_str
      }
    )
    expect = scope_str.split()
    actual = get_scopes_from_refresh_token(self.ctx)
    self.assertEqual(actual, expect)

  @patch("requests.post")
  def test_get_scope_from_rt_exception(self, mocked_post):
    """Test get_scope_from_rt for exception."""

    mocked_post.side_effect = Mock(
      side_effect=requests.exceptions.ConnectionError()
    )

    # returns None if any error occurs
    self.assertEqual(
      None,
      get_scopes_from_refresh_token(self.ctx),
    )

  @patch("requests.post")
  def test_get_scope_from_rt_no_scope(self, mocked_post):
    """Test get_scope_from_rt for invalid json."""

    # Empty JSON returned
    mocked_post.return_value = Mock(
      status_code=201,
      json=lambda: {}
    )

    # returns None if any error occurs
    self.assertEqual(
      None,
      get_scopes_from_refresh_token(self.ctx),
    )


class TestScopesIntegration(unittest.TestCase):
  """Integration test against the live test-project."""

  # TODO: This is a test boilerplate, Ref: Issue #69
  def setUp(self):
    # TODO: get_creds_from_metadata or some other method should
    # TODO: return refresh token
    # TODO: this self.credentials does not have refresh_token
    # for example, get credential form get_creds_from_metadata
    # _, self.credentials = credsdb.get_creds_from_metadata()

    # for now, fake data in the credentials is added.
    # This line must be removed once a method
    # is implemented in credsdb to return refresh token.
    self.credentials = credentials.Credentials(
      token="faketoken",
      refresh_token="<token>",
      client_id="id",
      client_secret="secret",
    )

  def test_get_scope_from_rt(self):
    """Test get_scope_from_rt valid."""
    ctx = {
      "refresh_token": self.credentials.refresh_token,
      "client_id": self.credentials.client_id,
      "client_secret": self.credentials.client_secret,
    }
    actual = get_scopes_from_refresh_token(ctx)
    # self.assertTrue(
    #   verify(
    #     actual,
    #     "refresh_scopes",
    #     True,
    #   )
    # )
    # TODO: uncomment above lines and remove this assert
    # forced pass until the main logic is integrated.
    self.assertEqual(actual, None)


class TestCrawler(unittest.TestCase):
  """Test crawler functionalities."""

  def setUp(self):
    _, self.credentials = credsdb.get_creds_from_metadata()

  def test_credential(self):
    """Checks if credential is not none."""
    self.assertIsNotNone(self.credentials)

  def test_compute_instance_name(self):
    """Test compute instance name."""
    self.assertTrue(
      verify(
        CrawlerFactory.create_crawler(
          "compute_instances",
        ).crawl(
          PROJECT_NAME,
          ClientFactory.get_client("compute").get_service(self.credentials),
        ),
        "compute_instances",
        True,
      )
    )

  def test_compute_disks_names(self):
    """Test compute disk names."""
    self.assertTrue(
      verify(
        CrawlerFactory.create_crawler(
          "compute_disks",
        ).crawl(
          PROJECT_NAME,
          ClientFactory.get_client("compute").get_service(self.credentials),
        ),
        "compute_disks",
        True,
      )
    )

  def test_compute_images_names(self):
    """Test compute image names."""
    self.assertTrue(
      verify(
        CrawlerFactory.create_crawler(
          "compute_images",
        ).crawl(
          PROJECT_NAME,
          ClientFactory.get_client("compute").get_service(self.credentials),
        ),
        "compute_images",
        True,
      )
    )

  def test_machine_images(self):
    """Test machine images"""
    self.assertTrue(
      verify(
        CrawlerFactory.create_crawler(
          "machine_images",
        ).crawl(
          PROJECT_NAME,
          ClientFactory.get_client("compute").get_service(self.credentials),
        ),
        "machine_images",
        True,
      )
    )

  def test_static_ips(self):
    """Test static IPs."""
    self.assertTrue(
      verify(
        CrawlerFactory.create_crawler(
          "static_ips",
        ).crawl(
          PROJECT_NAME,
          ClientFactory.get_client("compute").get_service(self.credentials),
        ),
        "static_ips",
        True,
      )
    )

  def test_compute_snapshots(self):
    """Test compute snapshot."""
    self.assertTrue(
      verify(
        CrawlerFactory.create_crawler(
          "compute_snapshots",
        ).crawl(
          PROJECT_NAME,
          ClientFactory.get_client("compute").get_service(
            self.credentials,
          ),
        ),
        "compute_snapshots",
        True,
      )
    )

  def test_firewall_rules(self):
    """Test firewall rules."""
    self.assertTrue(
      verify(
        CrawlerFactory.create_crawler(
          "firewall_rules",
        ).crawl(
          PROJECT_NAME,
          ClientFactory.get_client("compute").get_service(
            self.credentials,
          ),
        ),
        "firewall_rules",
      )
    )

  def test_subnets(self):
    """Test subnets."""
    self.assertTrue(
      verify(
        CrawlerFactory.create_crawler(
          "subnets",
        ).crawl(
          PROJECT_NAME,
          ClientFactory.get_client("compute").get_service(self.credentials),
        ),
        "subnets",
        True,
      )
    )

  def test_storage_buckets(self):
    """Test storage bucket."""
    self.assertTrue(
      verify(
        crawl.get_bucket_names(
          PROJECT_NAME,
          service=ClientFactory.get_client("storage").get_service(
            self.credentials,
          ),
          dump_fd=None,
          dump_iam_policies=True
        ),
        "storage_buckets",
      )
    )

  def test_managed_zones(self):
    """Test managed zones."""
    self.assertTrue(
      verify(
        CrawlerFactory.create_crawler(
          "managed_zones",
        ).crawl(
          PROJECT_NAME,
          ClientFactory.get_client("dns").get_service(self.credentials),
        ),
        "managed_zones",
        True,
      )
    )

  def test_gke_clusters(self):
    """Test GKE clusters."""
    gke_client = scanner.gke_client_for_credentials(
      credentials=self.credentials,
    )
    self.assertTrue(
      verify(
        crawl.get_gke_clusters(PROJECT_NAME, gke_client),
        "gke_clusters",
      )
    )

  def test_gke_images(self):
    self.assertTrue(
      verify(
        crawl.get_gke_images(PROJECT_NAME, self.credentials.token),
        "gke_images",
        True,
      )
    )

  def test_app_services(self):
    """Test app services."""
    self.assertTrue(
      verify(
        CrawlerFactory.create_crawler(
          "app_services",
        ).crawl(
          PROJECT_NAME,
          ClientFactory.get_client("appengine").get_service(self.credentials),
        ),
        "app_services",
      )
    )

  def test_sql_instances(self):
    """Test SQL instances."""
    self.assertTrue(
      verify(
        CrawlerFactory.create_crawler(
          "sql_instances",
        ).crawl(
          PROJECT_NAME,
          ClientFactory.get_client("sqladmin").get_service(self.credentials),
        ),
        "sql_instances",
        True,
      )
    )

  def test_bq(self):
    """Test BigQuery databases and table names."""
    self.assertTrue(
      verify(
        crawl.get_bq(
          PROJECT_NAME,
          ClientFactory.get_client("bigquery").get_service(self.credentials),
        ),
        "bq",
      )
    )

  def test_pubsub_subs(self):
    """Test PubSub Subscriptions."""
    self.assertTrue(
      verify(
        CrawlerFactory.create_crawler(
          "pubsub_subs",
        ).crawl(
          PROJECT_NAME,
          ClientFactory.get_client("pubsub").get_service(self.credentials),
        ),
        "pubsub_subs",
      )
    )

  def test_cloud_functions(self):
    """Test CloudFunctions list."""
    self.assertTrue(
      verify(
        CrawlerFactory.create_crawler(
          "cloud_functions",
        ).crawl(
          PROJECT_NAME,
          ClientFactory.get_client("cloudfunctions").get_service(
            self.credentials,
          ),
        ),
        "cloud_functions",
      )
    )

  def test_bigtable_instances(self):
    """Test BigTable Instances."""
    self.assertTrue(
      verify(
        CrawlerFactory.create_crawler(
          "bigtable_instances",
        ).crawl(
          PROJECT_NAME,
          ClientFactory.get_client("bigtableadmin").get_service(
            self.credentials
          ),
        ),
        "bigtable_instances",
      )
    )

  def test_spanner_instances(self):
    """Test Spanner Instances."""
    self.assertTrue(
      verify(
        CrawlerFactory.create_crawler(
          "spanner_instances",
        ).crawl(
          PROJECT_NAME,
          ClientFactory.get_client("spanner").get_service(self.credentials),
        ),
        "spanner_instances",
      )
    )

  def test_filestore_instances(self):
    """Test FileStore Instances."""
    self.assertTrue(
      verify(
        CrawlerFactory.create_crawler(
          "filestore_instances",
        ).crawl(
          PROJECT_NAME,
          ClientFactory.get_client("file").get_service(self.credentials),
        ),
        "filestore_instances",
      )
    )

  def test_kms(self):
    """Test list of KMS keys."""
    self.assertTrue(
      verify(
        crawl.get_kms_keys(
          PROJECT_NAME,
          ClientFactory.get_client("cloudkms").get_service(self.credentials),
        ),
        "kms",
        True,
      )
    )

  def test_endpoints(self):
    """Test endpoints' information."""
    self.assertTrue(
      verify(
        crawl.get_endpoints(
          PROJECT_NAME,
          ClientFactory.get_client("servicemanagement").get_service(
            self.credentials,
          ),
        ),
        "endpoints",
      )
    )

  def test_services(self):
    """Test list of API services enabled in the project."""
    self.assertTrue(
      verify(
        crawl.list_services(
          PROJECT_NAME,
          ClientFactory.get_client("serviceusage").get_service(
            self.credentials,
          ),
        ),
        "services",
        True
      )
    )

  def test_iam_policy(self):
    """Test IAM policy."""
    self.assertTrue(
      verify(
        crawl.get_iam_policy(
          PROJECT_NAME,
          ClientFactory.get_client("cloudresourcemanager").get_service(
            self.credentials,
          ),
        ),
        "iam_policy",
      )
    )

  def test_service_accounts(self):
    """Test service accounts."""
    self.assertTrue(
      verify(
        crawl.get_service_accounts(
          PROJECT_NAME,
          ClientFactory.get_client("iam").get_service(
            self.credentials,
          ),
        ),
        "service_accounts",
      )
    )

  def test_project_info(self):
    """Test project info."""
    self.assertTrue(
      verify(
        crawl.fetch_project_info(
          PROJECT_NAME,
          ClientFactory.get_client("cloudresourcemanager").get_service(
            self.credentials,
          ),
        ),
        "project_info",
      )
    )

  def test_sourcerepos(self):
    """Test list of cloud source repositories in the project."""
    self.assertTrue(
      verify(
        crawl.list_sourcerepo(
          PROJECT_NAME,
          ClientFactory.get_client("sourcerepo").get_service(self.credentials),
        ),
        "sourcerepos",
      )
    )

  def test_dns_policies(self):
    """Test cloud DNS policies."""
    self.assertTrue(
      verify(
        CrawlerFactory.create_crawler(
          "dns_policies",
        ).crawl(
          PROJECT_NAME,
          ClientFactory.get_client("dns").get_service(self.credentials)
        ),
        "dns_policies",
      )
    )


class TestClientFactory(unittest.TestCase):
  """Unit tests for the ClientFactory class."""

  def test_get_client_dns(self):
    """Test get_client method with 'dns' name."""
    client = ClientFactory.get_client("dns")
    self.assertIsInstance(client, DNSClient)

  def test_get_client_compute(self):
    """Test get_client method with 'compute' name."""
    client = ClientFactory.get_client("compute")
    self.assertIsInstance(client, ComputeClient)

  def test_get_client_appengine(self):
    """Test get_client method with 'appengine' name."""
    client = ClientFactory.get_client("appengine")
    self.assertIsInstance(client, AppEngineClient)

  def test_get_client_storage(self):
    """Test get_client method with 'storage' name."""
    client = ClientFactory.get_client("storage")
    self.assertIsInstance(client, StorageClient)

  def test_get_client_sql(self):
    """Test get_client method with 'sqladmin' name."""
    client = ClientFactory.get_client("sqladmin")
    self.assertIsInstance(client, SQLClient)

  def test_get_client_bq(self):
    """Test get_client method with 'bigquery' name."""
    client = ClientFactory.get_client("bigquery")
    self.assertIsInstance(client, BQClient)

  def test_get_client_pubsub(self):
    """Test get_client method with 'pubsub' name."""
    client = ClientFactory.get_client("pubsub")
    self.assertIsInstance(client, PubSubClient)

  def test_get_client_cloudfunctions(self):
    """Test get_client method with 'cloudfunctions' name."""
    client = ClientFactory.get_client("cloudfunctions")
    self.assertIsInstance(client, CloudFunctionsClient)

  def test_get_client_bigtable(self):
    """Test get_client method with 'bigtableadmin' name."""
    client = ClientFactory.get_client("bigtableadmin")
    self.assertIsInstance(client, BigTableClient)

  def test_get_client_spanner(self):
    """Test get_client method with 'spanner' name."""
    client = ClientFactory.get_client("spanner")
    self.assertIsInstance(client, SpannerClient)

  def test_get_client_filestore(self):
    """Test get_client method with 'spanner' name."""
    client = ClientFactory.get_client("file")
    self.assertIsInstance(client, FilestoreClient)

  def test_get_client_cloud_kms(self):
    """Test get_client method with 'cloudkms' name."""
    client = ClientFactory.get_client("cloudkms")
    self.assertIsInstance(client, CloudKMSClient)

  def test_get_client_service_management(self):
    """Test get_client method with 'servicemanagement' name."""
    client = ClientFactory.get_client("servicemanagement")
    self.assertIsInstance(client, ServiceManagementClient)

  def test_get_client_source_repo(self):
    """Test get_client method with 'sourcerepo' name."""
    client = ClientFactory.get_client("sourcerepo")
    self.assertIsInstance(client, SourceRepoClient)

  def test_get_client_cloud_resource_manager(self):
    """Test get_client method with 'cloudresourcemanager' name."""
    client = ClientFactory.get_client("cloudresourcemanager")
    self.assertIsInstance(client, CloudSourceManagerClient)

  def test_get_client_service_usage(self):
    """Test get_client method with 'serviceusage' name."""
    client = ClientFactory.get_client("serviceusage")
    self.assertIsInstance(client, ServiceUsageClient)

  def test_get_client_iam(self):
    """Test get_client method with 'iam' name."""
    client = ClientFactory.get_client("iam")
    self.assertIsInstance(client, IAMClient)

  def test_get_client_invalid(self):
    """Test get_client method with invalid name."""
    with self.assertLogs(level=logging.ERROR) as log:
      client = ClientFactory.get_client("invalid")
      self.assertIsNone(client)
      self.assertEqual(log.output, ["ERROR:root:Client not supported."])


class TestCrawlerFactory(unittest.TestCase):
  """Unit tests for the CrawlerFactory class."""

  def test_create_crawler_app_services(self):
    """Test create_crawler method with 'app_services' name."""
    crawler = CrawlerFactory.create_crawler("app_services")
    self.assertIsInstance(crawler, AppServicesCrawler)

  def test_create_crawler_cloud_functions(self):
    """Test create_crawler method with 'cloud_functions' name."""
    crawler = CrawlerFactory.create_crawler("cloud_functions")
    self.assertIsInstance(crawler, CloudFunctionsCrawler)

  def test_create_crawler_bigtable_instances(self):
    """Test create_crawler method with 'app_services' name."""
    crawler = CrawlerFactory.create_crawler("bigtable_instances")
    self.assertIsInstance(crawler, BigTableInstancesCrawler)

  def test_create_crawler_compute_instances(self):
    """Test create_crawler method with 'compute_instances' name."""
    crawler = CrawlerFactory.create_crawler("compute_instances")
    self.assertIsInstance(crawler, ComputeInstancesCrawler)

  def test_create_crawler_compute_images(self):
    """Test create_crawler method with 'compute_images' name."""
    crawler = CrawlerFactory.create_crawler("compute_images")
    self.assertIsInstance(crawler, ComputeImagesCrawler)

  def test_create_crawler_compute_machine_images(self):
    """Test create_crawler method with 'machine_images' name."""
    crawler = CrawlerFactory.create_crawler("machine_images")
    self.assertIsInstance(crawler, ComputeMachineImagesCrawler)

  def test_create_crawler_compute_disks(self):
    """Test create_crawler method with 'compute_disks' name."""
    crawler = CrawlerFactory.create_crawler("compute_disks")
    self.assertIsInstance(crawler, ComputeDisksCrawler)

  def test_create_crawler_compute_static_ips(self):
    """Test create_crawler method with 'static_ips' name."""
    crawler = CrawlerFactory.create_crawler("static_ips")
    self.assertIsInstance(crawler, ComputeStaticIPsCrawler)

  def test_create_crawler_compute_snapshots(self):
    """Test create_crawler method with 'compute_snapshots' name."""
    crawler = CrawlerFactory.create_crawler("compute_snapshots")
    self.assertIsInstance(crawler, ComputeSnapshotsCrawler)

  def test_create_crawler_compute_subnets(self):
    """Test create_crawler method with 'subnets' name."""
    crawler = CrawlerFactory.create_crawler("subnets")
    self.assertIsInstance(crawler, ComputeSubnetsCrawler)

  def test_create_crawler_compute_firewall_rules(self):
    """Test create_crawler method with 'firewall_rules' name."""
    crawler = CrawlerFactory.create_crawler("firewall_rules")
    self.assertIsInstance(crawler, ComputeFirewallRulesCrawler)

  def test_create_crawler_sql_instances(self):
    """Test create_crawler method with 'sql_instances' name."""
    crawler = CrawlerFactory.create_crawler("sql_instances")
    self.assertIsInstance(crawler, SQLInstancesCrawler)

  def test_create_crawler_spanner_instances(self):
    """Test create_crawler method with 'spanner_instances' name."""
    crawler = CrawlerFactory.create_crawler("spanner_instances")
    self.assertIsInstance(crawler, SpannerInstancesCrawler)

  def test_create_crawler_filestore_instances(self):
    """Test create_crawler method with 'filestore_instances' name."""
    crawler = CrawlerFactory.create_crawler("filestore_instances")
    self.assertIsInstance(crawler, FilestoreInstancesCrawler)

  def test_create_crawler_pubsub_subscriptions(self):
    """Test create_crawler method with 'pubsub_subs' name."""
    crawler = CrawlerFactory.create_crawler("pubsub_subs")
    self.assertIsInstance(crawler, PubSubSubscriptionsCrawler)

  def test_create_crawler_dns_managed_zones(self):
    """Test create_crawler method with 'managed_zones' name."""
    crawler = CrawlerFactory.create_crawler("managed_zones")
    self.assertIsInstance(crawler, DNSManagedZonesCrawler)

  def test_create_crawler_dns_policies(self):
    """Test create_crawler method with 'dns_policies' name."""
    crawler = CrawlerFactory.create_crawler("dns_policies")
    self.assertIsInstance(crawler, DNSPoliciesCrawler)

  def test_create_crawler_invalid(self):
    """Test create_crawler method with invalid name."""
    with self.assertLogs(level=logging.ERROR) as log:
      crawler = CrawlerFactory.create_crawler("invalid")
      self.assertIsNone(crawler)
      self.assertEqual(log.output, ["ERROR:root:Crawler not supported."])
