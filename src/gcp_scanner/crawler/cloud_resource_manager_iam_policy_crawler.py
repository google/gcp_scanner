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
import sys
from typing import List, Dict, Any

from googleapiclient import discovery

from gcp_scanner.crawler.interface_crawler import ICrawler


class CloudResourceManagerIAMPolicyCrawler(ICrawler):
  '''Handle crawling of Cloud Resource Manager IAM Policy data.'''

  def crawl(self, project_name: str, service: discovery.Resource) -> List[Dict[str, Any]]:
    '''Retrieve an IAM Policy in the project.

    Args:
      project_name: A name of a project to query info about.
      service: A resource object for interacting with the cloud source API.

    Returns:
      A list of resource objects representing the crawled data.
    '''

    logging.info("Retrieving IAM policy for %s", project_name)

    resource = project_name

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
