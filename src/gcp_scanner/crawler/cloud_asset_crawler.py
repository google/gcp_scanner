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
from typing import List, Dict, Any, Union

from googleapiclient import discovery

from gcp_scanner.crawler.interface_crawler import ICrawler


class CloudAssetCrawler(ICrawler):
  """Handle crawling of Cloud Asset data."""

  def crawl(self, project_id: str, service: discovery.Resource,
            config: Dict[str, Union[bool, str]] = None) -> Dict[str, List[Dict[str, Any]]]:
    """Retrieve a list of Cloud Assets available in the project.

    Args:
      project_id: A name of a project to query info about.
      service: A resource object for interacting with the Cloud Assets API.
      config: Configuration options for the crawler (Optional).

    Returns:
      A list of objects representing the crawled data.
    """

    logging.info("Retrieving CloudAssets.")
    assets_list = list()
    try:
      request = service.assets().list(
        parent=f"projects/{project_id}")
      while request is not None:
        response = request.execute()
        assets_list.extend(response.get("assets", []))
        request = service.assets().list_next(
          previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to retrieve CloudAsset for project %s", project_id)
      logging.info(sys.exc_info())

    return assets_list
    
