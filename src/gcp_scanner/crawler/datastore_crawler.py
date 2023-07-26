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


class DatastoreCrawler(ICrawler):
  """Handle crawling of cloud datastore data."""

  def crawl(self, project_id: str, service: discovery.Resource,
            config: Dict[str, Union[bool, str]] = None) -> Dict[str, List[Dict[str, Any]]]:
    """Retrieve a list of datastore kinds available in the project.

    Args:
      project_id: A name of a project to query info about.
      service: A resource object for interacting with the Firestore API.
      config: Configuration options for the crawler (Optional).

    Returns:
      A list of objects representing the crawled data.
    """

    logging.info("Retrieving Datastore entities.")
    datastore_kinds = dict()
    query = {
      "query": {
        "kind": [{"name": "__kind__"}]
      }
    }
    try:
      request = service.projects().runQuery(projectId=project_id, body=query)
      if request is not None:
        response = request.execute()
        entity_results = response.get("batch", {}).get("entityResults", [])
        datastore_kinds['kinds'] = [entity["entity"]["key"]["path"][0]["name"] for entity in entity_results]
    except Exception:
      logging.info("Failed to retrieve datastore entities for project %s", project_id)
      logging.info(sys.exc_info())
    return datastore_kinds
