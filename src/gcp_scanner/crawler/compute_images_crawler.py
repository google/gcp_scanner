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

from src.gcp_scanner.crawler.interface_crawler import ICrawler


class ComputeImagesCrawler(ICrawler):
  """Handle crawling of compute images data."""

  def crawl(self, project_name: str, service: discovery.Resource) -> List[Dict[str, Any]]:
    """Retrieve a list of Compute images available in the project.

   Args:
       project_name: The name of the project to query information about.
       service: A resource object for interacting with the GCP API.

   Returns:
       A list of resource objects representing the crawled data.
   """

    logging.info("Retrieving list of Compute Image names")
    images_result = list()
    try:
      request = service.images().list(project=project_name)
      while request is not None:
        response = request.execute()
        images_result = response.get("items", [])
        request = service.images().list_next(
          previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to enumerate compute images in the %s", project_name)
      logging.info(sys.exc_info())
    return images_result
