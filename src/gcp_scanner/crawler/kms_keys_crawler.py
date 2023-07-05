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


class KMSKeysCrawler(ICrawler):
  '''Handle crawling of KMS Keys data.'''

  async def crawl(self, project_id: str, service: discovery.Resource) -> List[Dict[str, Any]]:
    '''Retrieve a list of KMS Keys available in the project.

    Args:
      project_id: A name of a project to query info about.
      service: A resource object for interacting with KMS API.

    Returns:
      A list of resource objects representing the crawled data.
    '''

    logging.info("Retrieving KMS keys")
    kms_keys_list = list()
    try:
      # list all possible locations
      locations_list = list()
      request = service.projects().locations().list(name=f"projects/{project_id}")
      while request is not None:
        response = await request.execute()
        for location in response.get("locations", []):
          locations_list.append(location["locationId"])
        request = service.projects().locations().list_next(
            previous_request=request, previous_response=response)

      for location_id in locations_list:
        request_loc = service.projects().locations().keyRings().list(
            parent=f"projects/{project_id}/locations/{location_id}")
        while request_loc is not None:
          response_loc = request_loc.execute()
          for keyring in response_loc.get("keyRings", []):
            request = service.projects().locations().keyRings().cryptoKeys().list(
                parent=keyring["name"])
            while request is not None:
              response = request.execute()
              for key in response.get("cryptoKeys", []):
                kms_keys_list.append(key)

              request = service.projects().locations().keyRings().cryptoKeys(
              ).list_next(
                  previous_request=request, previous_response=response)

          request_loc = service.projects().locations().keyRings().list_next(
              previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to retrieve KMS keys for project %s", project_id)
      logging.info(sys.exc_info())
    return kms_keys_list
