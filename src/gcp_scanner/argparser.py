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


"""This Module can be imported to parse command line arguments.

"""

import argparse
import logging

def parse_arguments():
  """A function for parsing arguments using the argparse library.
  """

  # Creating the argument parser
  parser = argparse.ArgumentParser(
  prog='scanner.py',
  description='GCP Scanner',
  usage='python3 %(prog)s -o folder_to_save_results -g -')

  # Adding arguments
  required_named = parser.add_argument_group('Required parameters')
  required_named.add_argument(
    '-o',
    required=True,
    dest='output',
    default='scan_db',
    help='Path to output directory')

  parser.add_argument(
    '-k',
    '--sa_key_path',
    default=None,
    dest='key_path',
    help='Path to directory with SA keys in json format')
  parser.add_argument(
    '-g',
    '--gcloud_profile_path',
    default=None,
    dest='gcloud_profile_path',
    help='Path to directory with gcloud profile. Specify -\
    to search for credentials in default gcloud config path'
  )
  parser.add_argument(
    '-m',
    default=False,
    dest='use_metadata',
    action='store_true',
    help='Extract credentials from GCE instance metadata')
  parser.add_argument(
    '-at',
    default=None,
    dest='access_token_files',
    help='A list of comma separated files with access token and OAuth scopes.\
TTL limited. A token and scopes should be stored in JSON format.')
  parser.add_argument(
    '-rt',
    default=None,
    dest='refresh_token_files',
    help='A list of comma separated files with refresh_token, client_id,\
token_uri and client_secret stored in JSON format.'
)
  parser.add_argument(
    '-s', default=None, dest='key_name', help='Name of individual SA to scan')
  parser.add_argument(
    '-p',
    default=None,
    dest='target_project',
    help='Name of individual project to scan')
  parser.add_argument(
    '-f',
    default=None,
    dest='force_projects',
    help='Comma separated list of project names to include in the scan')
  parser.add_argument(
    '-c',
    '--config',
    default=None,
    dest='config_path',
    help='A path to config file with a set of specific resources to scan.')
  parser.add_argument(
    '-l',
    '--logging',
    default='WARNING',
    dest='log_level',
    choices=('INFO', 'WARNING', 'ERROR'),
    help='Set logging level (INFO, WARNING, ERROR)')

  # Parsing arguments
  args = parser.parse_args()

  if not args.key_path and not args.gcloud_profile_path \
  and not args.use_metadata and not args.access_token_files\
  and not args.refresh_token_files:
    logging.error(
        'Please select at least one option to begin scan\
-k/--sa_key_path,-g/--gcloud_profile_path, -m, -rt, -at'
    )

  return args
