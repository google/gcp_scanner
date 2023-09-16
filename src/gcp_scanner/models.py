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


"""The module with SpiderContext query model.

"""

import queue
from typing import List, Tuple

from httplib2 import Credentials


class SpiderContext:
  """A simple class to initialize the context with a list of root SAs
  """

  def __init__(self, sa_tuples: List[Tuple[str, Credentials, List[str]]]):
    """Initialize the context with a list of the root service accounts.

    Args:
      sa_tuples: [(sa_name, sa_object, chain_so_far)]
    """

    self.service_account_queue = queue.Queue()
    for sa_tuple in sa_tuples:
      self.service_account_queue.put(sa_tuple)

  def __repr__(self) -> str:
    return f"{list(self.service_account_queue.queue)}"


class ProjectInfo:
  """A simple class to store project scan configration.
  """

  def __init__(
    self,
    project,
    sa_results,
    out_dir,
    scan_config,
    light_scan,
    target_project,
    scan_time_suffix,
    sa_name,
    credentials,
    chain_so_far,
    resource_worker_count
  ):
    self.project = project
    self.sa_results = sa_results
    self.out_dir = out_dir
    self.scan_config = scan_config
    self.light_scan = light_scan
    self.target_project = target_project
    self.scan_time_suffix = scan_time_suffix
    self.sa_name = sa_name
    self.credentials = credentials
    self.chain_so_far = chain_so_far
    self.resource_worker_count = resource_worker_count
