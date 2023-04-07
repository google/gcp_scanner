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


"""Command-Line Argument Parser

"""

import argparse
import logging


# Define a function to create an argument parser using the argparse module
def arg_parser():
  """Creates an argument parser using the `argparse` module and defines
  several command-line arguments.

  Args:
    None

  Returns:
    argparse.Namespace: A namespace object containing the parsed command-line
    arguments.
  """
  # Create a new parser object
  parser = argparse.ArgumentParser(
    prog='scanner.py',  # program name
    description='GCP Scanner',  # description
    usage='python3 %(prog)s -o folder_to_save_results -g -'
  )

  # Define a required argument group
  required_named = parser.add_argument_group('Required parameters')
  # Add a required argument to the group
  required_named.add_argument(
    '-o',  # short option name
    '--output-dir',  # long option name
    required=True,
    dest='output',
    default='scan_db',
    help='Path to output directory'
  )

  # Add command line arguments to the parser object
  parser.add_argument(
    '-k',
    '--sa-key-path',
    default=None,  # Default value if option is not specified
    dest='key_path',
    help='Path to directory with SA keys in json format'  # Help message
  )
  parser.add_argument(
    '-g',
    '--gcloud-profile-path',
    default=None,
    dest='gcloud_profile_path',
    help='Path to directory with gcloud profile. Specify - to search for\
    credentials in default gcloud config path'
  )
  parser.add_argument(
    '-m',
    '--use-metadata',
    default=False,
    dest='use_metadata',
    action='store_true',
    help='Extract credentials from GCE instance metadata'
  )
  parser.add_argument(
    '-at',
    '--access-token-files',
    default=None,
    dest='access_token_files',
    help='A list of comma separated files with access token and OAuth scopes\
    TTL limited. A token and scopes should be stored in JSON format.'
  )
  parser.add_argument(
    '-rt',
    '--refresh-token-files',
    default=None,
    dest='refresh_token_files',
    help='A list of comma separated files with refresh_token, client_id,\
      token_uri and client_secret stored in JSON format.'
  )

  parser.add_argument(
    '-s',
    '--service-account',
    default=None,
    dest='key_name',
    help='Name of individual SA to scan')
  parser.add_argument(
    '-p',
    '--project',
    default=None,
    dest='target_project',
    help='Name of individual project to scan')
  parser.add_argument(
    '-f',
    '--force-projects',
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
    choices=('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'),
    help='Set logging level (INFO, WARNING, ERROR)')
  parser.add_argument(
    '-lf',
    '--log-file',
    default=None,
    dest='log_file',
    help='Save logs to the path specified rather than displaying in\
  console')

  # Parse the command line arguments
  args: argparse.Namespace = parser.parse_args()

  # Check if none of the necessary options are selected
  if not args.key_path and not args.gcloud_profile_path \
      and not args.use_metadata and not args.access_token_files\
          and not args.refresh_token_files:

      # If none of the options are selected, log an error message
    logging.error(
        'Please select at least one option to begin scan\
  -k/--sa-key-path,-g/--gcloud-profile-path, -m, -rt, -at')

  # Return the parsed command line arguments
  return args
