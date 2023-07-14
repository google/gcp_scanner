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


class CloudResourceManagerProjectInfoCrawler(ICrawler):
  '''Handle crawling of Cloud Resource Manager Project Info data.'''

  def crawl(self, project_name: str, service: discovery.Resource,
            config: Dict[str, Union[bool, str]] = None) -> Dict[str, Any]:
    '''Retrieve information about specific project.

    Args:
      project_name: Name of project to request info about
      service: A resource object for interacting with the Cloud Source API.
      config: Configuration options for the crawler (Optional).

    Returns:
      A list of resource objects representing the crawled data.
    '''

    project_info = None
    logging.info("Retrieving info about: %s", project_name)

    try:
      request = service.projects().get(projectId=project_name)
      response = request.execute()
      if "projectNumber" in response:
        project_info = response

    except Exception:
      logging.info("Failed to enumerate projects")
      logging.info(sys.exc_info())

    return project_info
