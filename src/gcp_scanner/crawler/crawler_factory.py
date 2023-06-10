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

from gcp_scanner.crawler.compute_disks_crawler import ComputeDisksCrawler
from gcp_scanner.crawler.compute_images_crawler import ComputeImagesCrawler
from gcp_scanner.crawler.compute_instances_crawler import ComputeInstancesCrawler
from gcp_scanner.crawler.compute_snapshots_crawler import ComputeSnapshotsCrawler
from gcp_scanner.crawler.compute_static_ips_crawler import ComputeStaticIPsCrawler
from gcp_scanner.crawler.machine_images_crawler import ComputeMachineImagesCrawler


class CrawlerFactory:
  """Factory class for creating crawlers."""

  @classmethod
  def create_crawler(cls, name):
    """Returns the appropriate crawler."""

    if name == "compute_instances":
      return ComputeInstancesCrawler()
    if name == "compute_images":
      return ComputeImagesCrawler()
    if name == "machine_images":
      return ComputeMachineImagesCrawler()
    if name == "compute_disks":
      return ComputeDisksCrawler()
    if name == "static_ips":
      return ComputeStaticIPsCrawler()
    if name == "compute_snapshots":
      return ComputeSnapshotsCrawler()

    logging.error("Crawler not supported.")
    return None
