# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""The module to query GCP resources via RestAPI.

"""

import logging
import sys
from typing import List, Dict, Any

from googleapiclient import discovery
from httplib2 import Credentials

class ServerlessCrawler:
  def __get_cloudfunctions(self, project_id: str,
                        credentials: Credentials) -> List[Dict[str, Any]]:
    """Retrieve a list of CloudFunctions available in the project.

    Args:
      project_id: A name of a project to query info about.
      credentials: An google.oauth2.credentials.Credentials object.

    Returns:
      A list of CloudFunctions in the project.
    """

    logging.info("Retrieving CloudFunctions")
    functions_list = list()
    service = discovery.build(
        "cloudfunctions", "v1", credentials=credentials, cache_discovery=False)
    try:
      request = service.projects().locations().functions().list(
          parent=f"projects/{project_id}/locations/-")
      while request is not None:
        response = request.execute()
        functions_list = response.get("functions", [])
        request = service.projects().locations().functions().list_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to retrieve CloudFunctions for project %s", project_id)
      logging.info(sys.exc_info())

    return functions_list

  def __get_app_services(self, project_name: str,
                      credentials: Credentials) -> Dict[str, Any]:
    """Retrieve a list of AppEngine instances available in the project.

    Args:
      project_name: A name of a project to query info about.
      credentials: An google.oauth2.credentials.Credentials object.

    Returns:
      A dict representing default apps and services available in the project.
    """

    app_client = discovery.build(
        "appengine", "v1", credentials=credentials, cache_discovery=False)

    logging.info("Retrieving app services")
    app_services = dict()
    try:
      request = app_client.apps().get(appsId=project_name)
      response = request.execute()
      if response.get("name", None) is not None:
        app_services["default_app"] = (response["name"],
                                      response["defaultHostname"],
                                      response["servingStatus"])

      request = app_client.apps().services().list(appsId=project_name)

      app_services["services"] = list()
      while request is not None:
        response = request.execute()
        app_services["services"] = response.get("services", [])
        request = app_client.apps().services().list_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to retrieve App services for project %s", project_name)
      logging.info(sys.exc_info())
    return app_services