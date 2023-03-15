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

import googleapiclient
from httplib2 import Credentials

class ProjectInfoCrawler:
  def fetch_project_info(self, project_name: str,
                        credentials: Credentials) -> Dict[str, Any]:
    """Retrieve information about specific project.

    Args:
      project_name: Name of project to request info about
      credentials: An google.oauth2.credentials.Credentials object.

    Returns:
      Project info object or None.
    """
    project_info = None
    logging.info("Retrieving info about: %s", project_name)

    try:
      service = googleapiclient.discovery.build(
          "cloudresourcemanager",
          "v1",
          credentials=credentials,
          cache_discovery=False)
      request = service.projects().get(projectId=project_name)
      response = request.execute()
      if "projectNumber" in response:
        project_info = response

    except Exception:
      logging.info("Failed to enumerate projects")
      logging.info(sys.exc_info())

    return project_info


  def get_project_list(self, 
                         credentials: Credentials) -> List[Dict[str, Any]]:
    """Retrieve a list of projects accessible by credentials provided.

    Args:
      credentials: An google.oauth2.credentials.Credentials object.

    Returns:
      A list of Project objects from cloudresourcemanager RestAPI.
    """

    logging.info("Retrieving projects list")
    project_list = list()
    try:
      service = googleapiclient.discovery.build(
          "cloudresourcemanager",
          "v1",
          credentials=credentials,
          cache_discovery=False)
      request = service.projects().list()
      while request is not None:
        response = request.execute()
        project_list = response.get("projects",[])
        request = service.projects().list_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to enumerate projects")
      logging.info(sys.exc_info())
    return project_list