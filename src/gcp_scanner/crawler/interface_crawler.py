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

from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List, Union

from googleapiclient import discovery


class ICrawler(metaclass=ABCMeta):
  """Interface for Crawler Classes.

  This interface defines the contract for crawler classes that are used to crawl resource data
  of a given project using the Google Cloud Platform (GCP) API.

  """

  @staticmethod
  @abstractmethod
  def crawl(project_name: str, service: discovery.Resource,
            config: Dict[str, Union[bool, str]] = None) -> List[Dict[str, Any]]:
    """Crawl resource data of the given project.

    This method retrieves resource data of the specified project using the provided GCP API service
    and returns a list of resource objects.

    Args:
        project_name: The name of the project to query information about.
        service: A resource object for interacting with the GCP API.
        config: Configuration options for the crawler (Optional).

    Returns:
        A list of resource objects representing the crawled data.

    Raises:
        NotImplementedError: If a child class does not implement this method.

    """

    raise NotImplementedError("Child class must implement the crawl() method.")
