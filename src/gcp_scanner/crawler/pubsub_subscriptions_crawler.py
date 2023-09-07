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
from typing import Dict, Any, Union

from googleapiclient import discovery

from gcp_scanner.crawler.interface_crawler import ICrawler


class PubSubSubscriptionsCrawler(ICrawler):
  '''Handle crawling of PubSub Subscriptions data.'''

  def crawl(self, project_id: str, service: discovery.Resource,
            config: Dict[str, Union[bool, str]] = None) -> Dict[str, Any]:
    '''Retrieve a list of PubSub subscriptions available in the project.

    Args:
      project_id: A name of a project to query info about.
      service: A resource object for interacting with the PubSub API.
      config: Configuration options for the crawler (Optional).

    Returns:
      A list of resource objects representing the crawled data.
    '''

    logging.info("Retrieving PubSub Subscriptions")
    pubsubs_list = list()
    try:

      request = service.projects().subscriptions().list(
        project=f"projects/{project_id}")
      while request is not None:
        response = request.execute()
        pubsubs_list = response.get("subscriptions", [])
        request = service.projects().subscriptions().list_next(
          previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to get PubSubs for project %s", project_id)
      logging.info(sys.exc_info())
    return pubsubs_list
