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

"""The module to perform functional test of the GCP Scanner.

"""

from . import scanner
import unittest.mock
import os
import json

# Resource count for each resource type
RESOURCE_COUNT = 28
RESULTS_JSON_COUNT = 1
PROJECT_INFO_COUNT = 5
IAM_POLICY_COUNT = 14
COMPUTE_INSTANCES_COUNT = 3
COMPUTE_IMAGES_COUNT = 1
COMPUTE_DISKS_COUNT = 3
STATIC_IPS_COUNT = 1
COMPUTE_SNAPSHOTS_COUNT = 1
SUBNETS_COUNT = 38
FIREWALL_RULES_COUNT = 8
APP_SERVICES_COUNT = 2
STORAGE_BUCKETS_COUNT = 5
MANAGED_ZONES_COUNT = 1
GKE_CLUSTERS_COUNT = 1
GKE_IMAGES_COUNT = 4
SQL_INSTANCES_COUNT = 1
BQ_COUNT = 1
BIGTABLE_COUNT = 0
SPANNER_COUNT = 1
CLOUDSTORE_COUNT = 1
PUBSUB_COUNT = 1
CLOUD_FUNCTIONS = 1
ENDPOINTS_COUNT = 0
KMS_COUNT = 1
SERVICES_COUNT = 1
SERVICE_ACCOUNTS_COUNT = 3

def check_obj_entry(res_dict, subojects_count, entry_name, volatile=False):
    # Check if an object entry exists in the given dictionary and has the expected number of objects
    obj = res_dict.get(entry_name, None)
    if volatile is True:
        assert obj is not None and (len(obj) == subojects_count or len(obj) == subojects_count - 1)
    else:
        assert obj is not None and len(obj) == subojects_count

def validate_result():
    # Load the results file and validate the resource counts
    file_name = os.listdir("res/")[0]
    with open("res/" + file_name, "r", encoding="utf-8") as f:
        res_data = json.load(f)

    # project
    project = res_data["projects"].get("test-gcp-scanner", None)
    assert project is not None
    assert len(project) == RESOURCE_COUNT

    check_obj_entry(project, PROJECT_INFO_COUNT, "project_info")
    check_obj_entry(project, IAM_POLICY_COUNT, "iam_policy")
    check_obj_entry(project, SERVICE_ACCOUNTS_COUNT, "service_accounts")

    check_obj_entry(project, COMPUTE_INSTANCES_COUNT, "compute_instances")
    check_obj_entry(project, COMPUTE_IMAGES_COUNT, "compute_images")
    check_obj_entry(project, COMPUTE_DISKS_COUNT, "compute_disks")
    check_obj_entry(project, COMPUTE_SNAPSHOTS_COUNT, "compute_snapshots")

    check_obj_entry(project, STATIC_IPS_COUNT, "static_ips")
    check_obj_entry(project, SUBNETS_COUNT, "subnets")
    check_obj_entry(project, FIREWALL_RULES_COUNT, "firewall_rules")
    check_obj_entry(project, MANAGED_ZONES_COUNT, "managed_zones")

    check_obj_entry(project, APP_SERVICES_COUNT, "app_services")

    check_obj_entry(project, STORAGE_BUCKETS_COUNT, "storage_buckets")

    check_obj_entry(project, GKE_CLUSTERS_COUNT, "gke_clusters")
     # Volatile test. US zone sometimes appear and disappear.
    check_obj_entry(project, GKE_IMAGES_COUNT, "gke_images", True)

    check_obj_entry(project, SQL_INSTANCES_COUNT, "sql_instances")
    check_obj_entry(project, BQ_COUNT, "bq")
    check_obj_entry(project, BIGTABLE_COUNT, "bigtable_instances")
    check_obj_entry(project, SPANNER_COUNT, "spanner_instances")
    check_obj_entry(project, CLOUDSTORE_COUNT, "cloudstore_instances")

    check_obj_entry(project, PUBSUB_COUNT, "pubsub_subs")
    check_obj_entry(project, CLOUD_FUNCTIONS, "cloud_functions")
    check_obj_entry(project, ENDPOINTS_COUNT, "endpoints")

    check_obj_entry(project, KMS_COUNT, "kms")

    check_obj_entry(project, SERVICES_COUNT, "services")


def test_acceptance():
    # Create a directory to store the results
    os.mkdir("res")
    
    # Define the arguments to run the scanner in test mode and save results in the "res" directory
    testargs = ["__main__.py", "-m", "-p", "test-gcp-scanner", "-o", "res"]

    # Patch the command-line arguments to run the scanner with the specified arguments
    with unittest.mock.patch("sys.argv", testargs):
        # Run the scanner with the patched arguments and assert that it returns 0 (indicating success)
        assert scanner.main() == 0
        
        # Assert that the number of files in the "res" directory is equal to RESULTS_JSON_COUNT
        assert len(os.listdir("res/")) == RESULTS_JSON_COUNT
        
        # Validate the result to ensure that it conforms to the expected format and contains valid data
        validate_result()
