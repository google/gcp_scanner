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


"""This module contains functions to retrieve information about Google 
Cloud Platform projects. Specifically, it provides functions to retrieve 
KMS keys and IAM policies in a project. The functions take in the project 
name or ID and the user's credentials as arguments and return a list of 
dictionaries containing information about the resources in the project.

"""

import logging
import sys
from typing import List, Dict, Any

from googleapiclient import discovery
from httplib2 import Credentials

def get_kms_keys(self, project_id: str,
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


def get_iam_policy(self, project_name: str,
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
