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

import crawl
import credsdb
import json
import scanner
import filecmp
import difflib
import os
import shutil
import sqlite3
import datetime

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
    #line = line[:-1]
    if line.startswith("VOLATILE"):
      continue # we do not compare volatile lines
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

  if volatile == True:
    result = compare_volatile(f1, f2)
  else:
    result = filecmp.cmp(f1, f2)
    if result is False:
      print_diff(f1, f2)

  return result


def test_creds_fetching():
  os.mkdir("creds")
  conn = sqlite3.connect("creds/credentials.db")
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

  assert str(credsdb.find_creds("./creds")) == "['./creds/credentials.db']"

  conn = sqlite3.connect("creds/access_tokens.db")
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

  assert str(credsdb.get_access_tokens_dict("./creds/credentials.db")) == \
    "{'test_account@gmail.com': 'ya.29c.TEST'}"

  res = str(credsdb.extract_creds("./creds/credentials.db"))
  print(res)
  assert res == "[SA(account_name='test_account@gmail.com', \
creds='test_data', token='ya.29c.TEST')]"

  assert str(credsdb.get_account_creds_list("./creds")) == \
    "[[SA(account_name='test_account@gmail.com', \
creds='test_data', token='ya.29c.TEST')]]"

  #impersonate_sa()
  shutil.rmtree("creds")


def test_crawler():
  _, credentials = credsdb.get_creds_from_metadata()
  assert credentials is not None

  # GCE section
  compute_client = scanner.compute_client_for_credentials(credentials)
  assert verify(crawl.get_compute_instances_names(PROJECT_NAME, compute_client),
                                                  "compute_instances",
                                                  True) is True
  assert verify(crawl.get_compute_disks_names(PROJECT_NAME, compute_client),
                                             "compute_disks",
                                             True) is True
  assert verify(crawl.get_compute_images_names(PROJECT_NAME, compute_client),
                                             "compute_images") is True
  assert verify(crawl.get_static_ips(PROJECT_NAME, compute_client),
                                     "static_ips") is True
  assert verify(crawl.get_compute_snapshots(PROJECT_NAME, compute_client),
                                            "compute_snapshots") is True
  assert verify(crawl.get_firewall_rules(PROJECT_NAME, compute_client),
                                         "firewall_rules") is True
  assert verify(crawl.get_subnets(PROJECT_NAME, compute_client),
                                  "subnets",
                                  True) is True

  assert verify(crawl.get_bucket_names(PROJECT_NAME, credentials=credentials,
                                       enum_files = False),
                                      "storage_buckets") is True

  assert verify(crawl.get_managed_zones(PROJECT_NAME, credentials=credentials),
                                        "managed_zones") is True

  gke_client = scanner.gke_client_for_credentials(credentials=credentials)
  assert verify(crawl.get_gke_clusters(PROJECT_NAME, gke_client),
                                       "gke_clusters") is True

  assert verify(crawl.get_gke_images(PROJECT_NAME, credentials.token),
                                     "gke_images",
                                     True) is True

  assert verify(crawl.get_app_services(PROJECT_NAME, credentials),
                                       "app_services") is True

  # Get SQL instances
  assert verify(crawl.get_sql_instances(PROJECT_NAME, credentials),
                                        "sql_instances",
                                        True) is True

  # Get BigQuery databases and table names
  assert verify(crawl.get_bq(PROJECT_NAME, credentials), "bq") is True

  # Get PubSub Subscriptions
  assert verify(crawl.get_pubsub_subscriptions(
          PROJECT_NAME, credentials), "pubsub_subs") is True

  # Get CloudFunctions list
  assert verify(crawl.get_cloudfunctions(
          PROJECT_NAME, credentials), "cloud_functions") is True

  # Get List of BigTable Instanses
  assert verify(crawl.get_bigtable_instances(
          PROJECT_NAME, credentials), "bigtable_instances") is True

  # Get Spanner Instances
  assert verify(crawl.get_spanner_instances(
          PROJECT_NAME, credentials), "spanner_instances") is True

  # Get CloudStore Instances
  assert verify(crawl.get_filestore_instances(
          PROJECT_NAME, credentials), "cloudstore_instances") is True

  # Get list of KMS keys
  assert verify(crawl.get_kms_keys(PROJECT_NAME, credentials),
                                   "kms") is True

  # Get information about Endpoints
  assert verify(crawl.get_endpoints(PROJECT_NAME, credentials),
                                    "endpoints") is True

  # Get list of API services enabled in the project
  assert verify(crawl.list_services(PROJECT_NAME, credentials),
                                    "services",
                                    True) is True

  # IAM Policy
  assert verify(crawl.get_iam_policy(PROJECT_NAME, credentials),
                                     "iam_policy") is True

  # Get service accounts
  assert verify(crawl.get_service_accounts(PROJECT_NAME, credentials),
                                           "service_accounts") is True

  # Get project info
  assert verify(crawl.fetch_project_info(PROJECT_NAME, credentials),
                                         "project_info") is True