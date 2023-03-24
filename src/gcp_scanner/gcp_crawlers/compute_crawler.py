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

"""This module provides a class to retrieve information about various Compute
Engine resources available in a Google Cloud Platform project.
"""

import logging
import sys
from typing import List, Dict, Any

from googleapiclient import discovery


class GCPComputeResources:
  """A class that retrieves information about various Compute Engine
  resources available in a Google Cloud Platform project.
  """

  def __init__(self, project_name: str, service: discovery.Resource):
    self.project_name = project_name
    self.service = service

  def get_compute_instances_names(self) -> List[Dict[str, Any]]:
    """Retrieve a list of Compute VMs available in the project.

    Returns:
      A list of instance objects.
    """
    logging.info("Retrieving list of Compute Instances")
    instances_result = list()
    try:
      request = self.service.instances().aggregatedList(project=self.project_name)
      while request is not None:
        response = request.execute()
        if response.get("items", None) is not None:
          instances_result = [instance
                              for _, instances_scoped_list in response["items"].items()
                              for instance in instances_scoped_list.get("instances", [])]
        request = self.service.instances().aggregatedList_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.exception("Failed to enumerate compute instances in %s", 
                        self.project_name)
      logging.info(sys.exc_info())
    return instances_result

  def get_compute_images_names(self) -> List[Dict[str, Any]]:
    """Retrieve a list of Compute images available in the project.

    Returns:
      A list of image objects.
    """
    logging.info("Retrieving list of Compute Image names")
    images_result = list()
    try:
      request = self.service.images().list(project=self.project_name)
      while request is not None:
        response = request.execute()
        images_result = response.get("items", [])
        request = self.service.images().list_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.exception("Failed to enumerate compute images in %s", self.project_name)
      logging.info(sys.exc_info())
    return images_result

  def get_compute_disks_names(self) -> List[Dict[str, Any]]:
    """Retrieve a list of Compute disks available in the project.

    Returns:
      A list of disk objects.
    """
    logging.info("Retrieving list of Compute Disk names")
    disk_names_list = list()
    try:
      request = self.service.disks().aggregatedList(project=self.project_name)
      while request is not None:
        response = request.execute()
        if response.get("items", None) is not None:
          disk_names_list = [disk
                             for _, disks_scoped_list in response["items"].items()
                             for disk in disks_scoped_list.get("disks", [])]
        request = self.service.disks().aggregatedList_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.exception("Failed to enumerate compute disks in %s", self.project_name)
      logging.info(sys.exc_info())
    return disk_names_list

  def get_compute_snapshots(self) -> List[Dict[str, Any]]:
    """Retrieve a list of Compute snapshots available in the project.

    Returns:
      A list of snapshot objects.
    """
    logging.info("Retrieving Compute Snapshots")
    snapshots_list = list()
    try:
      request = self.service.snapshots().list(project=self.project_name)
      while request is not None:
        response = request.execute()
        snapshots_list = response.get("items", [])
        request = self.service.snapshots().list_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.exception("Failed to get compute snapshots in %s", self.project_name)
      logging.info(sys.exc_info())
    return snapshots_list
