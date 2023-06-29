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
import json
import logging
import sys
from typing import List, Dict, Any, Union, Tuple, TextIO

from googleapiclient import discovery, errors

from gcp_scanner.crawler.interface_crawler import ICrawler


class StorageBucketsCrawler(ICrawler):
  """Handle crawling of bucket names data."""

  def crawl(self, project_name: str, service: discovery.Resource,
            config: Dict[str, Union[bool, str]] = None) -> Dict[str, Tuple[Any, List[Any]]]:
    """Retrieve a list of buckets available in the project.

     Args:
         project_name: The name of the project to query information about.
         service: A resource object for interacting with the GCP API.
         config: Configuration options for the crawler (Optional).

     Returns:
         A list of resource objects representing the crawled data.
     """
    logging.info("Retrieving GCS Buckets")
    # prepare additional configs
    dump_fd = self._get_dump_file_dir(config=config)
    is_dump_iam_policies = self._get_is_dump_iam_policies(config=config)
    # output dict
    buckets_dict = dict()
    # Make an authenticated API request
    request = service.buckets().list(project=project_name)
    while request is not None:
      try:
        response = request.execute()
      except errors.HttpError:
        logging.info("Failed to list buckets in the %s", project_name)
        logging.info(sys.exc_info())
        break

      for bucket in response.get("items", []):
        buckets_dict[bucket["name"]] = bucket
        if is_dump_iam_policies is True:
          buckets_dict[bucket["name"]]["iam_policy"] = self._get_bucket_iam(bucket["name"], service)
        if dump_fd is not None:
          ret_fields = "nextPageToken,items(bucket,name,size,contentType, timeCreated)"
          req = service.objects().list(bucket=bucket["name"], fields=ret_fields)

          while req:
            try:
              resp = req.execute()
              for item in resp.get("items", []):
                dump_fd.write(json.dumps(item, indent=2, sort_keys=False))

              req = service.objects().list_next(req, resp)
            except errors.HttpError:
              logging.info("Failed to read the bucket %s", bucket["name"])
              logging.info(sys.exc_info())
              break

      request = service.buckets().list_next(
        previous_request=request, previous_response=response)
    if dump_fd is not None:
      dump_fd.close()
    return buckets_dict

  @classmethod
  def _get_bucket_iam(cls, bucket_name: str, service: discovery.Resource) -> List[Any]:
    """Retrieve IAM policies in the bucket.

    Args:
      bucket_name: A name of bucket to query info about.
      service: An authenticated API request.
    Returns:
      A list with bucket IAM policies.
    """

    logging.info("Retrieving GCS Bucket %s IAM Policy", bucket_name)
    bucket_iam_policies = list()
    request = service.buckets().getIamPolicy(bucket=bucket_name)
    try:
      response = request.execute()
    except errors.HttpError:
      logging.info("Failed to IAM Policy in the %s", bucket_name)
      logging.info(sys.exc_info())
      return []

    for bucket_iam_policy in response.get("bindings", []):
      bucket_iam_policies.append(bucket_iam_policy)

    return bucket_iam_policies

  @classmethod
  def _get_dump_file_dir(cls, config: Dict[str, Union[bool, str]]) -> TextIO | None:
    """Get the dump file directory based on the provided configuration.

    Args:
        config: Configuration dictionary with keys 'fetch_file_names' (bool) and 'gcs_output_path' (str).

    Returns:
        TextIO object for the dump file if 'fetch_file_names' is True and 'gcs_output_path' is provided. Otherwise, None.
    """
    dump_file_names = None
    if config is not None and config.get('fetch_file_names', False) is True:
      gcs_output_path = config.get('gcs_output_path', '')  # think a good fallback if gcs_output_path is not set
      dump_file_names = open(gcs_output_path, 'w', encoding='utf-8')
    return dump_file_names

  @classmethod
  def _get_is_dump_iam_policies(cls, config: Dict[str, Union[bool, str]]) -> bool:
    """Check if dumping IAM policies is enabled based on the provided configuration.

    Args:
        config: Configuration dictionary with a key 'fetch_buckets_iam' (bool) indicating whether to fetch IAM policies.

    Returns:
        True if 'fetch_buckets_iam' is True in the config. Otherwise, False.
    """
    if config is not None and config.get('fetch_buckets_iam', False) is True:
      return True
    return False
