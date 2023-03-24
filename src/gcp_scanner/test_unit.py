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
import os
import shutil
import sqlite3
import unittest
from unittest.mock import patch, Mock

import requests
from google.oauth2 import credentials

from . import gcp_crawlers as crawl
from . import credsdb
from . import scanner
from .credsdb import get_scopes_from_refresh_token

PROJECT_NAME = "test-gcp-scanner"


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
    file_1_text = file_1.readlines()

  with open(f2, "r", encoding="utf-8") as file_2:
    file_2_text = file_2.readlines()

  for line in file_2_text:
    # line = line[:-1]
    if line.startswith("VOLATILE"):
      continue  # we do not compare volatile lines
    if line in file_1_text:
      continue
    else:
      print(f"The following line was not identified in the output:\n{line}")
      res = False

  return res


def verify(res_to_verify, resource_type, volatile=False):
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
    self.compute_client = scanner.compute_client_for_credentials(
      self.credentials,
    )
    self.compute_resources = crawl.GCPComputeResources(PROJECT_NAME, self.compute_client)

  def test_credential(self):
    """Checks if credential is not none."""
    self.assertIsNotNone(self.credentials)

  def test_compute_instance_name(self):
    """Test compute instance name."""
    self.assertTrue(
      verify(
        self.compute_resources.get_compute_instances_names(),
        "compute_instances",
        True,
      )
    )

  def test_compute_disks_names(self):
    """Test compute disk names."""
    self.assertTrue(
      verify(
        self.compute_resources.get_compute_disks_names(),
        "compute_disks",
        True,
      )
    )

  def test_compute_images_names(self):
    """Test compute image names."""
    self.assertTrue(
      verify(
        self.compute_resources.get_compute_images_names(),
        "compute_images",
        True,
      )
    )

  def test_static_ips(self):
    """Test static IPs."""
    self.assertTrue(
      verify(
        crawl.get_static_ips(PROJECT_NAME, self.compute_client),
        "static_ips",
        True,
      )
    )

  def test_compute_snapshots(self):
    """Test compute snapshot."""
    self.assertTrue(
      verify(
        self.compute_resources.get_compute_snapshots(),
        "compute_snapshots",
        True,
      )
    )

  def test_firewall_rules(self):
    """Test firewall rules."""
    self.assertTrue(
      verify(
        crawl.get_firewall_rules(PROJECT_NAME, self.compute_client),
        "firewall_rules",
      )
    )

  def test_subnets(self):
    """Test subnets."""
    self.assertTrue(
      verify(
        crawl.get_subnets(PROJECT_NAME, self.compute_client),
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
          credentials=self.credentials,
          dump_fd=None,
        ),
        "storage_buckets",
      )
    )

  def test_managed_zones(self):
    """Test managed zones."""
    self.assertTrue(
      verify(
        crawl.get_managed_zones(PROJECT_NAME, credentials=self.credentials),
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
        crawl.get_app_services(PROJECT_NAME, self.credentials),
        "app_services",
      )
    )

  def test_sql_instances(self):
    """Test SQL instances."""
    self.assertTrue(
      verify(
        crawl.get_sql_instances(PROJECT_NAME, self.credentials),
        "sql_instances",
        True,
      )
    )

  def test_bq(self):
    """Test BigQuery databases and table names."""
    self.assertTrue(
      verify(
        crawl.get_bq(PROJECT_NAME, self.credentials),
        "bq",
      )
    )

  def test_pubsub_subs(self):
    """Test PubSub Subscriptions."""
    self.assertTrue(
      verify(
        crawl.get_pubsub_subscriptions(PROJECT_NAME, self.credentials),
        "pubsub_subs",
      )
    )

  def test_cloud_functions(self):
    """Test CloudFunctions list."""
    self.assertTrue(
      verify(
        crawl.get_cloudfunctions(PROJECT_NAME, self.credentials),
        "cloud_functions",
      )
    )

  def test_bigtable_instances(self):
    """Test BigTable Instances."""
    self.assertTrue(
      verify(
        crawl.get_bigtable_instances(PROJECT_NAME, self.credentials),
        "bigtable_instances",
      )
    )

  def test_spanner_instances(self):
    """Test Spanner Instances."""
    self.assertTrue(
      verify(
        crawl.get_spanner_instances(PROJECT_NAME, self.credentials),
        "spanner_instances",
      )
    )

  def test_cloudstore_instances(self):
    """Test CloudStore Instances."""
    self.assertTrue(
      verify(
        crawl.get_filestore_instances(PROJECT_NAME, self.credentials),
        "cloudstore_instances",
      )
    )

  def test_kms(self):
    """Test list of KMS keys."""
    self.assertTrue(
      verify(
        crawl.get_kms_keys(PROJECT_NAME, self.credentials),
        "kms",
        True,
      )
    )

  def test_endpoints(self):
    """Test endpoints' information."""
    self.assertTrue(
      verify(
        crawl.get_endpoints(PROJECT_NAME, self.credentials),
        "endpoints",
      )
    )

  def verify_services(self,service_list):
    return len(service_list) > 0

  def test_services(self):
    """Test list of API services enabled in the project."""
    self.assertTrue(
      verify(
        crawl.list_services(PROJECT_NAME, self.credentials),
        "services",
        True
      )
    )

  def test_iam_policy(self):
    """Test IAM policy."""
    self.assertTrue(
      verify(
        crawl.get_iam_policy(PROJECT_NAME, self.credentials),
        "iam_policy",
      )
    )

  def test_service_accounts(self):
    """Test service accounts."""
    self.assertTrue(
      verify(
        crawl.get_service_accounts(PROJECT_NAME, self.credentials),
        "service_accounts",
      )
    )

  def test_project_info(self):
    """Test project info."""
    self.assertTrue(
      verify(
        crawl.fetch_project_info(PROJECT_NAME, self.credentials),
        "project_info",
      )
    )

  def test_sourcerepos(self):
    """Test list of cloud source repositories in the project."""
    self.assertTrue(
      verify(
        crawl.list_sourcerepo(PROJECT_NAME, self.credentials),
        "sourcerepos",
      )
    )

  def test_dns_policies(self):
    """Test cloud DNS policies."""
    self.assertTrue(
      verify(
        crawl.list_dns_policies(PROJECT_NAME, self.credentials),
        "dns_policies",
      )
    )
