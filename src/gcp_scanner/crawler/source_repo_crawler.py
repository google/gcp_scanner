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


class CloudSourceRepoCrawler(ICrawler):
  '''Handle crawling of Cloud Source Repo data.'''

  async def crawl(self, project_id: str, service: discovery.Resource) -> Dict[str, Any]:
    """Retrieve a list of cloud source repositories enabled in the project.

    Args:
    project_id: An id of a project to query info about.
    service: A resource object for interacting with the Source Repo API.

    Returns:
    A list of cloud source repositories in the project.
    """

    logging.info("Retrieving cloud source repositories %s", project_id)
    list_of_repos = list()

    request = service.projects().repos().list(
        name="projects/" + project_id,
        pageSize=500
  )
    try:
        while request is not None:
            response = await request.execute()
            list_of_repos.extend(response.get("repos", None))

            request = service.projects().repos().list_next(
            previous_request=request,
            previous_response=response
      )
    except Exception:
        logging.info("Failed to retrieve source repos for project %s", project_id)
        logging.info(sys.exc_info())
    return list_of_repos
