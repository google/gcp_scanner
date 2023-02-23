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

"""The module to generate test file for GCP Scanner.

"""

import datetime
import filecmp
import json
import os
import shutil
import sqlite3

from . import crawl
from . import credsdb
from . import scanner

PROJECT_NAME = "test-gcp-scanner"

_, self.credentials = credsdb.get_creds_from_metadata()
self.compute_client = scanner.compute_client_for_credentials(
      self.credentials,
    )

res = crawl.get_sql_instances(PROJECT_NAME, self.credentials)
output = json.dumps(res, indent=2, sort_keys=False)
print(output)




