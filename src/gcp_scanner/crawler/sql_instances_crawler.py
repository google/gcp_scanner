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


class SQLInstancesCrawler(ICrawler):
  '''Handle crawling of SQL Instances data.'''

  async def crawl(self, project_name: str, service: discovery.Resource) -> Dict[str, Any]:
    '''Retrieve a list of SQL instances available in the project.

    Args:
      project_name: A name of a project to query info about.
      service: A resource object for interacting with the SQLAdmin API.

    Returns:
      A list of resource objects representing the crawled data.
    '''

    logging.info("Retrieving CloudSQL Instances")
    sql_instances_list = list()
    try:
      request = service.instances().list(project=project_name)
      while request is not None:
        response = request.execute()
        sql_instances_list = response.get("items", [])
        request = service.instances().list_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to get SQL instances for project %s", project_name)
      logging.info(sys.exc_info())
    logging.info("Exiting CloudSQL Instances")
    return sql_instances_list
