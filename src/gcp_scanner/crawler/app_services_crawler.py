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


class AppServicesCrawler(ICrawler):
  '''Handle crawling of App Services data.'''

  async def crawl(self, project_name: str, service: discovery.Resource) -> Dict[str, Any]:
    '''Retrieve a list of AppEngine instances available in the project.

    Args:
      project_name: A name of a project to query info about.
      service: A resource object for interacting with the AppEngine API.

    Returns:
      A list of resource objects representing the crawled data.
    '''

    logging.info("Retrieving app services")
    app_services = dict()
    try:
      request = service.apps().get(appsId=project_name)
      response = await request.execute()
      if response.get("name", None) is not None:
        app_services["default_app"] = (response["name"],
                                      response["defaultHostname"],
                                      response["servingStatus"])

      request = service.apps().services().list(appsId=project_name)

      app_services["services"] = list()
      while request is not None:
        response = request.execute()
        app_services["services"] = response.get("services", [])
        request = service.apps().services().list_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to retrieve App services for project %s", project_name)
      logging.info(sys.exc_info())
    return app_services
