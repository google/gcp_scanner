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


class ComputeDisksCrawler(ICrawler):
  """Handle crawling of compute disks data."""

  def crawl(self, project_name: str, service: discovery.Resource,
            config: Dict[str, Union[bool, str]] = None) -> List[Dict[str, Any]]:
    """Retrieve a list of Compute disks available in the project.

     Args:
         project_name: The name of the project to query information about.
         service: A resource object for interacting with the GCP API.
         config: Configuration options for the crawler (Optional).

     Returns:
         A list of resource objects representing the crawled data.
     """
    logging.info("Retrieving list of Compute Disk names")
    disk_names_list = list()
    try:
      request = service.disks().aggregatedList(project=project_name)
      while request is not None:
        response = request.execute()
        if response.get("items", None) is not None:
          disk_names_list = [
            disk for _, disks_scoped_list in response["items"].items()
            for disk in disks_scoped_list.get("disks", [])
          ]
        request = service.disks().aggregatedList_next(
          previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to enumerate compute disks in the %s", project_name)
      logging.info(sys.exc_info())

    return disk_names_list
