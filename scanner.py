#!/usr/bin/env python3

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

import logging
from time import perf_counter, process_time

from src.gcp_scanner import scanner

start_perf_counter = perf_counter()
start_process_time = process_time()
scanner.main()
end_perf_counter = perf_counter()
end_process_time = process_time()
elapsed_perf_counter = end_perf_counter - start_perf_counter
elapsed_process_time = end_process_time - start_process_time
logging.info("Elapsed time (CPU bound): %.6fs", elapsed_perf_counter)
logging.info("Elapsed time (not CPU bound): %.6fs", elapsed_process_time)