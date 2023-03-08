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

import collections
import json
import logging
import io
import sys
from typing import List, Dict, Any, Tuple

from google.cloud import container_v1
import googleapiclient
from googleapiclient import discovery
from httplib2 import Credentials
import requests
from requests.auth import HTTPBasicAuth

from crawlers import *

def infinite_defaultdict():
  """Initalize infinite default.

  Returns:
    DefaultDict
  """
  return collections.defaultdict(infinite_defaultdict)
