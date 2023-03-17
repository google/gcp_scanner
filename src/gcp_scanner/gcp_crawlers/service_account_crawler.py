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


"""This module contains several functions for interacting with Google Cloud
Platform (GCP) services. The functions included in this module allow users 
to retrieve information about GCP projects, KMS keys, IAM policies, Cloud 
Functions, App Engine instances, service accounts, and enabled APIs. The module 
utilizes the google-auth and google-api-python-client libraries for authentication
and interacting with GCP REST APIs.

"""

import logging
import sys
from typing import List, Dict, Any, Tuple

import googleapiclient
from googleapiclient import discovery
from httplib2 import Credentials

def get_associated_service_accounts(
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
    for member in entry["members"]:
      if "deleted:" in member:
        continue
      account_name = None
      for element in member.split(":"):
        if "@" in element:
          account_name = element
          break
      if account_name and account_name not in list_of_sas:
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
  print("debug: list_services")
  logging.info("Retrieving services list %s", project_id)
  list_of_services = list()
  serviceusage = discovery.build("serviceusage", "v1", credentials=credentials)

  request = serviceusage.services().list(
      parent="projects/" + project_id, pageSize=200, filter="state:ENABLED")
  try:
    while request is not None:
      response = request.execute()
      list_of_services.append(response.get("services", None))

      request = serviceusage.services().list_next(
          previous_request=request, previous_response=response)
  except Exception:
    logging.info("Failed to retrieve services for project %s", project_id)
    logging.info(sys.exc_info())
  print("debug: end")
  print(list_of_services)
  return list_of_services
