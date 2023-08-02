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


import json
import logging
import multiprocessing
import os
from datetime import datetime

from src.gcp_scanner import arguments
from src.gcp_scanner import models
from src.gcp_scanner import scanner
from src.gcp_scanner.client.client_factory import ClientFactory
from src.gcp_scanner.crawler.crawler_factory import CrawlerFactory 

if __name__ == "__main__":
  logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
  logging.getLogger('googleapiclient.http').setLevel(logging.ERROR)

  args = arguments.arg_parser()

  logging.basicConfig(level=getattr(logging, args.log_level.upper(), None),
                      format='%(asctime)s - %(levelname)s - %(message)s',
                      datefmt='%Y-%m-%d %H:%M:%S',
                      filename=args.log_file, filemode='a')

  force_projects_list = list()
  if args.force_projects:
    force_projects_list = args.force_projects.split(',')

  sa_tuples = scanner.get_sa_tuples(args)

  scan_config = None
  if args.config_path is not None:
    with open(args.config_path, 'r', encoding='utf-8') as f:
      scan_config = json.load(f)

  # Generate current timestamp to append to the filename
  scan_time_suffix = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

  context = models.SpiderContext(sa_tuples)

  project_queue = multiprocessing.Queue()
  processed_sas = set()
  while not context.service_account_queue.empty():
    # Get a new candidate service account / token
    sa_name, credentials, chain_so_far = context.service_account_queue.get()
    if sa_name in processed_sas:
      continue

    # Don't process this service account again
    processed_sas.add(sa_name)

    logging.info('>> current service account: %s', sa_name)
    sa_results = scanner.infinite_defaultdict()
    # Log the chain we used to get here (even if we have no privs)
    sa_results['service_account_chain'] = chain_so_far
    sa_results['current_service_account'] = sa_name
    # Add token scopes in the result
    sa_results['token_scopes'] = credentials.scopes

    project_list = CrawlerFactory.create_crawler(
      'project_list',
    ).crawl(
      ClientFactory.get_client('cloudresourcemanager').get_service(credentials),
    )

    if len(project_list) <= 0:
      logging.info('Unable to list projects accessible from service account')

    if force_projects_list:
      for force_project_id in force_projects_list:
        res = CrawlerFactory.create_crawler(
          'project_info',
        ).crawl(
          force_project_id,
          ClientFactory.get_client('cloudresourcemanager').get_service(
            credentials,
          ),
        )
        if res:
          project_list.append(res)
        else:
          # force object creation anyway
          project_list.append({'projectId': force_project_id,
                               'projectNumber': 'N/A'})
          
    # Enumerate projects accessible by SA
    for project in project_list:
      project_obj = models.ProjectInfo(
        project,
        sa_results, 
        args.output,
        scan_config,
        args.light_scan,
        args.target_project,
        scan_time_suffix,
        sa_name,
        credentials,
        chain_so_far
      )
      project_queue.put(project_obj)

  pool = multiprocessing.Pool(processes=min(int(args.worker_count), os.cpu_count()))

  while not project_queue.empty():
    pool.apply_async(scanner.get_resources, args=(project_queue.get(),))

  pool.close()
  pool.join()
