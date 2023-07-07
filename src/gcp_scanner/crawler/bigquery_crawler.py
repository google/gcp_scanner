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


class BigQueryCrawler(ICrawler):
  '''Handle crawling of BigQuery data.'''

  async def crawl(self, project_id: str,
                  service: discovery.Resource) -> Dict[str, List[Dict[str, Any]]]:
    '''Retrieve a list of BigQuery datasets available in the project.

    Args:
      project_id: A name of a project to query info about.
      service: A resource object for interacting with the BigQuery API.

    Returns:
      A list of resource objects representing the crawled data.
    '''

    logging.info("Retrieving BigQuery Datasets")
    bq_datasets = dict()
    try:
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
    logging.info("Exiting BigQuery Datasets")
    return bq_datasets


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
