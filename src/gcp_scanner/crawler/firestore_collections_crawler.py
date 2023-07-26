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


class FirestoreCollectionsCrawler(ICrawler):
  """Handle crawling of Firestore data."""

  def crawl(self, project_id: str, service: discovery.Resource,
            config: Dict[str, Union[bool, str]] = None) -> Dict[str, List[Dict[str, Any]]]:
    """Retrieve a list of Firestore datasets available in the project.

    Args:
      project_id: A name of a project to query info about.
      service: A resource object for interacting with the Firestore API.
      config: Configuration options for the crawler (Optional).

    Returns:
      A list of resource objects representing the crawled data.
    """

    logging.info("Retrieving Firestore Databases")
    firestore_documents = dict()
    project_path = f"projects/{project_id}"
    try:
      request = service.projects().databases().list(parent=project_path)
      if request is not None:
        response = request.execute()
        for database in response.get('databases', []):
          db_name = database['name']
          firestore_documents[db_name] = self.get_firestore_collectionIds(
            db_name,
            service,
          )
    except Exception:
      logging.info("Failed to retrieve Firestore databases for project %s", project_id)
      logging.info(sys.exc_info())
    return firestore_documents

  def get_firestore_collectionIds(self, parent: str, service: discovery.Resource) -> List[Dict[str, Any]]:
    """Retrieve a list of Firestore collections available in the dataset.

    Args:
      parent: string, Required. The parent document. In the format: `projects/{project_id}/databases/{database_id}/documents/{document_path}`.
      service: A resource object for interacting with the Firestore API.

    Returns:
      A list of Firestore collection ids.
    """

    logging.info("Firestore documents for %s", parent)
    list_of_collections_ids = list()
    try:
      request = service.projects().databases().documents().listCollectionIds(
        parent=f"{parent}/documents/*/**"
      )
      request.uri = request.uri.replace('/*/**', '')
      while request is not None:
        response = request.execute()
        list_of_collections_ids.extend(response.get("collectionIds", None))
        request = service.projects().databases().documents().listCollectionIds_next(
          previous_request=request,
          previous_response=response,
        )
    except Exception as ex:
      logging.info("Failed to retrieve Firestore collections for %s", parent)
      logging.info(sys.exc_info())
    return list_of_collections_ids
