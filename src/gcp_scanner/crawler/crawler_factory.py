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

from src.gcp_scanner.crawler.app_services_crawler import AppServicesCrawler
from src.gcp_scanner.crawler.compute_disks_crawler import ComputeDisksCrawler
from src.gcp_scanner.crawler.compute_firewall_rules_crawler import ComputeFirewallRulesCrawler
from src.gcp_scanner.crawler.compute_images_crawler import ComputeImagesCrawler
from src.gcp_scanner.crawler.compute_instances_crawler import ComputeInstancesCrawler
from src.gcp_scanner.crawler.compute_snapshots_crawler import ComputeSnapshotsCrawler
from src.gcp_scanner.crawler.compute_static_ips_crawler import ComputeStaticIPsCrawler
from src.gcp_scanner.crawler.compute_subnets_crawler import ComputeSubnetsCrawler
from src.gcp_scanner.crawler.machine_images_crawler import ComputeMachineImagesCrawler


service_crawler_map = {
  "app_services": AppServicesCrawler(),
  "compute_disks": ComputeDisksCrawler(),
  "compute_images": ComputeImagesCrawler(),
  "compute_instances": ComputeInstancesCrawler(),
  "compute_snapshots": ComputeSnapshotsCrawler(),
  "firewall_rules": ComputeFirewallRulesCrawler(),
  "machine_images": ComputeMachineImagesCrawler(),
  "static_ips": ComputeStaticIPsCrawler(),
  "subnets": ComputeSubnetsCrawler(),
}

class CrawlerFactory:
  """Factory class for creating crawlers."""

  @classmethod
  def create_crawler(cls, name):
    """Returns the appropriate crawler."""
    if name in service_crawler_map:
      return service_crawler_map[name]

    logging.error("Crawler not supported.")
    return None
