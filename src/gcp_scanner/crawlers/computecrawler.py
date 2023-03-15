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

class ComputeCrawler:
  def get_compute_instances_names(
      self, project_name: str, 
      service: discovery.Resource) -> List[Dict[str, Any]]:
    """Retrieve a list of Compute VMs available in the project.

    Args:
      project_name: A name of a project to query info about.
      service: A resource object for interacting with the Compute API.

    Returns:
      A list of instance objects.
    """

    logging.info("Retrieving list of Compute Instances")
    images_result = list()
    try:
      request = service.instances().aggregatedList(project=project_name)
      while request is not None:
        response = request.execute()
        if response.get("items", None) is not None:
          images_result = [instance
            for _, instances_scoped_list in response["items"].items()
            for instance in instances_scoped_list.get("instances",[])]
        request = service.instances().aggregatedList_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to enumerate compute instances in the %s",
                  project_name)
      logging.info(sys.exc_info())
    return images_result


  def get_compute_images_names(
      self, project_name: str, 
      service: discovery.Resource) -> List[Dict[str, Any]]:
    """Retrieve a list of Compute images available in the project.

    Args:
      project_name: A name of a project to query info about.
      service: A resource object for interacting with the Compute API.

    Returns:
      A list of image objects.
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


  def get_compute_disks_names(
      self, project_name: str, 
      service: discovery.Resource) -> List[Dict[str, Any]]:
    """Retrieve a list of Compute disks available in the project.

    Args:
      project_name: A name of a project to query info about.
      service: A resource object for interacting with the Compute API.

    Returns:
      A list of disk objects.
    """

    logging.info("Retrieving list of Compute Disk names")
    disk_names_list = list()
    try:
      request = service.disks().aggregatedList(project=project_name)
      while request is not None:
        response = request.execute()
        if response.get("items", None) is not None:
          disk_names_list = [disk
            for _, disks_scoped_list in response["items"].items()
            for disk in disks_scoped_list.get("disks", [])]
        request = service.disks().aggregatedList_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to enumerate compute disks in the %s", project_name)
      logging.info(sys.exc_info())

    return disk_names_list

  def get_compute_snapshots(self, project_name: str,
                            service: discovery.Resource) -> List[Dict[str, Any]]:
    """Retrieve a list of Compute snapshots available in the project.

    Args:
      project_name: A name of a project to query info about.
      service: A resource object for interacting with the Compute API.

    Returns:
      A list of snapshot objects.
    """

    logging.info("Retrieving Compute Snapshots")
    snapshots_list = list()
    try:
      request = service.snapshots().list(project=project_name)
      while request is not None:
        response = request.execute()
        snapshots_list = response.get("items", [])
        request = service.snapshots().list_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to get compute snapshots in the %s", project_name)
      logging.info(sys.exc_info())

    return snapshots_list