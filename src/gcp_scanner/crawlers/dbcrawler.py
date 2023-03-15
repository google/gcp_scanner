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

class DBCrawler:
  def get_sql_instances(self, project_name: str,
                        credentials: Credentials) -> List[Dict[str, Any]]:
    """Retrieve a list of SQL instances available in the project.

    Args:
      project_name: A name of a project to query info about.
      credentials: An google.oauth2.credentials.Credentials object.

    Returns:
      A list of sql instances in the project.
    """

    logging.info("Retrieving CloudSQL Instances")
    sql_instances_list = list()
    try:
      service = discovery.build(
          "sqladmin", "v1beta4", credentials=credentials, cache_discovery=False)

      request = service.instances().list(project=project_name)
      while request is not None:
        response = request.execute()
        sql_instances_list = response.get("items", [])
        request = service.instances().list_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to get SQL instances for project %s", project_name)
      logging.info(sys.exc_info())

    return sql_instances_list

  def get_bq_tables(self, project_id: str, dataset_id: str,
                    bq_service: discovery.Resource) -> List[Dict[str, Any]]:
    """Retrieve a list of BigQuery tables available in the dataset.

    Args:
      project_id: A name of a project to query info about.
      dataset_id: A name of dataset to query data from.
      bq_service: I do not know.

    Returns:
      A list of BigQuery tables in the dataset.
    """

    logging.info("Retrieving BigQuery Tables for dataset %s", dataset_id)
    list_of_tables = list()
    try:
      request = bq_service.tables().list(
          projectId=project_id, datasetId=dataset_id)
      while request is not None:
        response = request.execute()
        list_of_tables = response.get("tables", [])
        request = bq_service.tables().list_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to retrieve BQ tables for dataset %s", dataset_id)
      logging.info(sys.exc_info())
    return list_of_tables

  def get_bq(self, project_id: str,
            credentials: Credentials) -> Dict[str, List[Dict[str, Any]]]:
    """Retrieve a list of BigQuery datasets available in the project.

    Args:
      project_id: A name of a project to query info about.
      credentials: An google.oauth2.credentials.Credentials object.

    Returns:
      A dictionary of BigQuery dataset and corresponding tables.
    """

    logging.info("Retrieving BigQuery Datasets")
    bq_datasets = dict()
    try:
      service = discovery.build(
          "bigquery", "v2", credentials=credentials, cache_discovery=False)

      request = service.datasets().list(projectId=project_id)
      while request is not None:
        response = request.execute()

        for dataset in response.get("datasets", []):
          dataset_id = dataset["datasetReference"]["datasetId"]
          bq_datasets[dataset_id] = self.get_bq_tables(project_id,dataset_id, service)

        request = service.datasets().list_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to retrieve BQ datasets for project %s", project_id)
      logging.info(sys.exc_info())
    return bq_datasets

  def get_bigtable_instances(self, project_id: str,
                            credentials: Credentials) -> List[Dict[str, Any]]:
    """Retrieve a list of BigTable instances available in the project.

    Args:
      project_id: A name of a project to query info about.
      credentials: An google.oauth2.credentials.Credentials object.

    Returns:
      A list of BigTable instances in the project.
    """

    logging.info("Retrieving bigtable instances")
    bigtable_instances_list = list()
    try:
      service = discovery.build(
          "bigtableadmin", "v2", credentials=credentials, cache_discovery=False)

      request = service.projects().instances().list(
          parent=f"projects/{project_id}")
      while request is not None:
        response = request.execute()
        bigtable_instances_list = response.get("instances", [])
        request = service.projects().instances().list_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to retrieve BigTable instances for project %s",
                  project_id)
      logging.info(sys.exc_info())
    return bigtable_instances_list

  def get_spanner_instances(self, project_id: str,
                            credentials: Credentials) -> List[Dict[str, Any]]:
    """Retrieve a list of Spanner instances available in the project.

    Args:
      project_id: A name of a project to query info about.
      credentials: An google.oauth2.credentials.Credentials object.

    Returns:
      A list of Spanner instances in the project.
    """

    logging.info("Retrieving spanner instances")
    spanner_instances_list = list()
    try:
      service = discovery.build(
          "spanner", "v1", credentials=credentials, cache_discovery=False)

      request = service.projects().instances().list(
          parent=f"projects/{project_id}")
      while request is not None:
        response = request.execute()
        spanner_instances_list = response.get("instances", [])
        request = service.projects().instances().list_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to retrieve Spanner instances for project %s",
                  project_id)
      logging.info(sys.exc_info())
    return spanner_instances_list