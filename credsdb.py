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


"""The module to handle GCP credentials.

"""

import collections
import datetime
import json
import logging
import os
import sqlite3
import sys
from typing import List, Dict, Tuple, Optional, Mapping

from google.cloud.iam_credentials_v1.services.iam_credentials.client import IAMCredentialsClient
from google.oauth2 import credentials
from google.oauth2 import service_account
from httplib2 import Credentials
import requests

# Permissions to request for Access Token
scopes = "https://www.googleapis.com/auth/cloud-platform"

expires_in = 3600  # Expires in 1 hour

credentials_db_search_places = ["/home/", "/root/"]


def credentials_from_token(access_token: str, refresh_token: Optional[str],
                           token_uri: Optional[str], client_id: Optional[str],
                           client_secret: Optional[str],
                           scopes_user: Optional[str]) -> Credentials:
  return credentials.Credentials(
      access_token,
      refresh_token=refresh_token,
      token_uri=token_uri,
      client_id=client_id,
      client_secret=client_secret,
      scopes=scopes_user)


def get_creds_from_file(file_path: str) -> Tuple[str, Credentials]:
  """Creates a Credentials instance from a service account json file.

  Args:
    file_path: The path to the service account json file.

  Returns:
    str: An email address associated with a service account.
    google.auth.service_account.Credentials: The constructed credentials.
  """

  logging.info("Retrieving credentials from %s", file_path)
  creds = service_account.Credentials.from_service_account_file(file_path)
  return creds.service_account_email, creds


def get_creds_from_json(parsed_keyfile: Mapping[str, str]) -> Credentials:
  """Creates a Credentials instance from parsed service account info..

  Args:
    parsed_keyfile: The service account info in Google format.

  Returns:
    google.auth.service_account.Credentials: The constructed credentials.
  """

  return service_account.Credentials.from_service_account_info(parsed_keyfile)


def get_creds_from_metadata() -> Tuple[Optional[str], Optional[Credentials]]:
  """Retrieves a Credentials instance from compute instance metadata.

  Returns:
    str: An email associated with credentials.
    google.auth.service_account.Credentials: The constructed credentials.
  """

  print("Retrieving access token from instance metadata")

  token_url = "http://metadata.google.internal/computeMetadata/v1/instance/\
service-accounts/default/token"
  scope_url = "http://metadata.google.internal/computeMetadata/v1/instance/\
service-accounts/default/scopes"
  email_url = "http://metadata.google.internal/computeMetadata/v1/instance/\
service-accounts/default/email"
  headers = {"Metadata-Flavor": "Google"}
  try:
    res = requests.get(token_url, headers=headers)
    if not res.ok:
      print("Failed to retrieve instance token. Status code", res.status_code)
      return None, None
    token = res.json()["access_token"]

    res = requests.get(scope_url, headers=headers)
    if not res.ok:
      print("Failed to retrieve instance scopes. Status code", res.status_code)
      return None, None
    instance_scopes = res.content.decode("utf-8")

    res = requests.get(email_url, headers=headers)
    if not res.ok:
      print("Failed to retrieve instance email. Status code", res.status_code)
      return None, None
    email = res.content.decode("utf-8")

  except Exception:
    print("Failed to retrieve instance metadata")
    print(sys.exc_info()[1])
    return None, None

  print("Successfully retrieved instance metadata")
  print("Access token length: %d" % len(token), "Instance email: %s" % email,
        "Instance scopes: %s" % scopes)
  return email, credentials_from_token(token, None, None, None, None,
                                       instance_scopes)


def get_creds_from_data(access_token: str,
                        parsed_keyfile: Dict[str, str]) -> Credentials:
  """Creates a Credentials instance from parsed service account info.

  The function currently supports two types of credentials.  Service account key
  in json format and user account with refresh token.

  Args:
    access_token: An Oauth2 access token. It can be None.
    parsed_keyfile: The service account info in Google format.

  Returns:
    google.auth.service_account.Credentials: The constructed credentials.
  """
  creds = None
  if "refresh_token" in parsed_keyfile:
    logging.info("Identified user credentials in gcloud profile")
    # this is user account credentials with refresh token
    creds = credentials_from_token(access_token,
                                   parsed_keyfile["refresh_token"],
                                   parsed_keyfile["token_uri"],
                                   parsed_keyfile["client_id"],
                                   parsed_keyfile["client_secret"],
                                   parsed_keyfile["scopes"])
  elif "private_key" in parsed_keyfile:
    logging.info("Identified service account key credentials in gcloud profile")
    # this is a service account key with private key
    creds = get_creds_from_json(parsed_keyfile)
  else:
    logging.info("unknown type of credentials")

  return creds


def find_creds(explicit_path: Optional[str] = None) -> List[str]:
  """The function search disk and returns a list of files with GCP credentials.

  Args:
    explicit_path: An explicit path on disk to search. If None, the function
      searches in standard locations where gcloud profiles are usually located.

  Returns:
    list: The list of files with GCP credentials.
  """

  logging.info("Searching for credentials on disk")
  list_of_creds_files = list()
  search_paths = list()
  if explicit_path is not None and explicit_path != "-":
    search_paths.append(explicit_path)
  else:
    for dir_path in credentials_db_search_places:
      if not os.access(dir_path, os.R_OK):
        continue
      for subdir_name in os.listdir(dir_path):
        full_path = dir_path + subdir_name + "/.config/gcloud/"
        search_paths.append(full_path)

  for dir_path in search_paths:
    print("Scanning %s for credentials.db" % dir_path)
    full_path = os.path.join(dir_path, "credentials.db")
    if os.path.exists(full_path) and os.access(full_path, os.R_OK):
      print("Identified accessible gcloud config profile %s" % full_path)
      list_of_creds_files.append(full_path)
  print("Identified %d credential DBs" % len(list_of_creds_files))
  return list_of_creds_files


def get_access_tokens_dict(path_to_creds_db: str) -> Dict[str, str]:
  """The function search and extract Oauth2 access_tokens from sqlite3 DB.

  Args:
    path_to_creds_db: A path to sqllite3 DB with gcloud access tokens.

  Returns:
    dict: The dictionary of account names and corresponding tokens.
  """

  access_tokens_dict = dict()
  access_tokens_path = path_to_creds_db.replace("credentials.db",
                                                "access_tokens.db")
  if os.path.exists(access_tokens_path) and os.access(access_tokens_path,
                                                      os.R_OK):
    print("Identified access tokens DB in %s" % access_tokens_path)
    conn = sqlite3.connect(access_tokens_path)
    cursor = conn.execute(
        "SELECT account_id, access_token, token_expiry FROM access_tokens")
    rows = cursor.fetchall()
    for row in rows:
      associated_account = row[0]
      token = row[1]
      expiration_date = row[2]

      token_time_obj = datetime.datetime.strptime(expiration_date,
                                                  "%Y-%m-%d %H:%M:%S.%f")
      if datetime.datetime.now() > token_time_obj:
        print("Token for %s expired" % associated_account)
        continue

      access_tokens_dict[associated_account] = token

  return access_tokens_dict


def extract_creds(path_to_creds_db: str) -> List[Tuple[str, str, str]]:
  """The function extract refresh and associated access tokens from sqlite3 DBs.

  Args:
    path_to_creds_db: A path to sqllite3 DB with gcloud refresh tokens.

  Returns:
    list of tuples: (account name, refresh token, access token).
  """

  print("Opening %s DB" % path_to_creds_db)
  SA = collections.namedtuple("SA", "account_name, creds, token")

  res = list()
  conn = sqlite3.connect(path_to_creds_db)
  cursor = conn.execute("SELECT account_id, value FROM credentials")
  rows = cursor.fetchall()
  if len(rows) <= 0:
    print("Error: Empty database")
    return None
  # we also want to check for access_tokens to avoid unnecessary refreshing
  access_tokens = get_access_tokens_dict(path_to_creds_db)
  for row in rows:
    access_token = None
    if access_tokens.get(row[0], None) is not None:
      print("Found valid access token for %s" % row[0])
      access_token = access_tokens[row[0]]
    res.append(SA(row[0], row[1], access_token))
  print("Identified %d credential entries" % len(res))
  return res


def get_account_creds_list(
    gcloud_profile_path: Optional[str] = None
) -> List[List[Tuple[str, str, str]]]:
  """The function searches and extracts gcloud credentials from disk.

  Args:
    gcloud_profile_path: An explicit gcloud profile path on disk to search. If
      None, the function searches in standard locations where gcloud profiles
      are usually located.

  Returns:
    list: A list of tuples (account name, refresh token, access token).
  """

  accounts = list()
  creds_file_list = find_creds(gcloud_profile_path)
  for creds_file in creds_file_list:
    res = extract_creds(creds_file)
    if res is not None:
      accounts.append(res)
  return accounts


def impersonate_sa(iam_client: IAMCredentialsClient,
                   target_account: str) -> Credentials:
  """The function is used to impersonate SA.

  Args:
    iam_client: google.cloud.iam_credentials_v1.services.iam_credentials.
      client.IAMCredentialsClient object.
    target_account: Name of a service account to impersonate.

  Returns:
    google.auth.service_account.Credentials: The constructed credentials.
  """

  scopes_sa = ["https://www.googleapis.com/auth/cloud-platform"]
  intermediate_access_token = iam_client.generate_access_token(
      name=target_account, scope=scopes_sa, retry=None
      # lifetime = "43200"
  )

  return credentials_from_token(intermediate_access_token.access_token, None,
                                None, None, None, scopes_sa)


def creds_from_refresh_token(refresh_token_file):
  """The function is used to obtain Google Auth Credentials from refresh token.

  Args:
    refresh_token_file: a path to a file with refresh_token, client_id,
      client_secret, and token_uri stored in JSON format.

  Returns:
    google.auth.service_account.Credentials: The constructed credentials.
  """

  with open(refresh_token_file, encoding="utf-8") as f:
    creds_dict = json.load(f)

  return credentials.Credentials(
      None,
      refresh_token=creds_dict["refresh_token"],
      token_uri=creds_dict["token_uri"],
      client_id=creds_dict["client_id"],
      client_secret=creds_dict["client_secret"],
      scopes=["https://www.googleapis.com/auth/cloud-platform"])
