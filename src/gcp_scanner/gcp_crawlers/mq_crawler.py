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


"""This module contains a function to retrieve a list of PubSub 
subscriptions available in a Google Cloud project.

"""

import logging
import sys
from typing import List, Dict, Any

from googleapiclient import discovery
from httplib2 import Credentials


def get_pubsub_subscriptions(self, project_id: str,
                            credentials: Credentials) -> List[Dict[str, Any]]:
  """Retrieve a list of PubSub subscriptions available in the project.

  Args:
    project_id: A name of a project to query info about.
    credentials: An google.oauth2.credentials.Credentials object.

  Returns:
    A list of PubSub subscriptions in the project.
  """

  logging.info("Retrieving PubSub Subscriptions")
  pubsub_list = list()
  try:
    service = discovery.build(
        "pubsub", "v1", credentials=credentials, cache_discovery=False)

    request = service.projects().subscriptions().list(
        project=f"projects/{project_id}")
    while request is not None:
      response = request.execute()
      pubsub_list = response.get("subscriptions", [])
      request = service.projects().subscriptions().list_next(
          previous_request=request, previous_response=response)
  except Exception:
    logging.info("Failed to get PubSubs for project %s", project_id)
    logging.info(sys.exc_info())
  return pubsub_list
