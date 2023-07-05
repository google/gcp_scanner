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


class CloudResourceManagerProjectListCrawler(ICrawler):
  '''Handle crawling of Cloud Resource Manager Project List data.'''

  async def crawl(self, service: discovery.Resource) -> List[Dict[str, Any]]:
    '''Retrieve a list of projects accessible by credentials provided.

    Args:
      service: A resource object for interacting with the Cloud Source API.

    Returns:
      A list of resource objects representing the crawled data.
    '''

    logging.info("Retrieving projects list")
    project_list = list()
    try:
      request = service.projects().list()
      while request is not None:
        response = await request.execute()
        project_list = response.get("projects",[])
        request = service.projects().list_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to enumerate projects")
      logging.info(sys.exc_info())
    return project_list
