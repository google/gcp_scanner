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

from gcp_scanner.client.dns_client import DNSClient


class ClientFactory:
  """Factory class for getting generating SVG."""

  @classmethod
  def get_client(cls, name):
    """Returns the appropriate client."""

    if name == "compute":
      return DNSClient()

    logging.error("Client not supported.")
    return None
