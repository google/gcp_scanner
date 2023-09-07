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

from googleapiclient import discovery
from httplib2 import Credentials

from .interface_client import IClient


class IAMClient(IClient):
  """IAMClient class."""

  def get_service(self, credentials: Credentials) -> discovery.Resource:
    """Get discovery service for iam resource.

    Args:
      credentials: An google.oauth2.credentials.Credentials object.

    Returns:
      An object of discovery.Resource
    """
    return discovery.build(
      "iam",
      "v1",
      credentials=credentials,
      cache_discovery=False,
    )
