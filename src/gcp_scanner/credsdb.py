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
from typing import List, Dict, Tuple, Optional, Mapping, Union

from google.cloud.iam_credentials_v1.services.iam_credentials.client import IAMCredentialsClient
from google.oauth2 import credentials
from google.oauth2 import service_account
from httplib2 import Credentials
import requests

# Set search places for finding credentials file
credentials_db_search_places = ["/home/", "/root/"]


def credentials_from_token(access_token: str, refresh_token: Optional[str],
                           token_uri: Optional[str], client_id: Optional[str],
                           client_secret: Optional[str],
                           scopes_user: Optional[str]) -> Credentials:
  """
  Create Credentials instance from tokens
  """
  return credentials.Credentials(access_token, refresh_token=refresh_token,
                                 token_uri=token_uri, client_id=client_id,
                                 client_secret=client_secret,
                                 scopes=scopes_user)


def get_creds_from_file(file_path: str) -> Tuple[str, Credentials]:
  """
  Retrieve Credentials instance from a service account json file.
  """

  logging.info("Retrieving credentials from %s", file_path)
  creds = service_account.Credentials.from_service_account_file(file_path)
  return creds.service_account_email, creds


def get_creds_from_json(parsed_keyfile: Mapping[str, str]) -> Credentials:
  """
  Retrieve Credentials instance from parsed service account info.
  """

  return service_account.Credentials.from_service_account_info(
      parsed_keyfile)


def get_creds_from_metadata() -> Tuple[Optional[str], Optional[Credentials]]:
  """Retrieves a Credentials instance from compute instance metadata.

  Returns:
      Tuple[Optional[str], Optional[Credentials]]:
          A tuple containing the email associated with the
          credentials and the constructed credentials.
  """

  # Print a message to indicate that we are
  # retrieving the access token from instance metadata
  print("Retrieving access token from instance metadata")

  # Define the URLs that we need to
  # access to get the token, scopes, and email
  token_url = "http://metadata.google.internal/computeMetadata/v1/" \
              "instance/service-accounts/default/token"
  scope_url = "http://metadata.google.internal/computeMetadata/v1/" \
              "instance/service-accounts/default/scopes"
  email_url = "http://metadata.google.internal/computeMetadata/v1/" \
              "instance/service-accounts/default/email"

  # Set the headers for the requests
  headers = {"Metadata-Flavor": "Google"}

  try:
    # Make the request to get the access token
    res = requests.get(token_url, headers=headers)

    # Check if the response was successful
    if not res.ok:
      logging.error("Failed to retrieve instance token. "
                    "Status code %d", res.status_code)
      token_url = None

      return None, None

    # Parse the JSON response and get the access token
    token = res.json()["access_token"]

    # Make the request to get the instance scopes
    res = requests.get(scope_url, headers=headers)

    # Check if the response was successful
    if not res.ok:
      logging.error("Failed to retrieve instance scopes. "
                    "Status code %d", res.status_code)
      return None, None

    # Get the instance scopes from the response
    instance_scopes = res.content.decode("utf-8")

    # Make the request to get the instance email
    res = requests.get(email_url, headers=headers)

        # Check if the response was successful
    if not res.ok:
      logging.error("Failed to retrieve instance email. "
                    "Status code %d", res.status_code)
      return None, None

    # Get the instance email from the response
    email = res.content.decode("utf-8")

  except ImportError:
    # Log an error message if any exception occurred
    logging.error("Failed to retrieve instance metadata")
    logging.error(sys.exc_info()[1])
    return None, None

    # Print a message to indicate that
    # we have successfully retrieved the instance metadata
    print("Successfully retrieved instance metadata")

  # Log the length of the access token, instance email, and instance scopes
  logging.info("Access token length: %d", len(token))
  logging.info("Instance email: %s", email)
  logging.info("Instance scopes: %s", instance_scopes)

  # Return the email and credentials
  # constructed from the token and instance scopes
  return email, credentials_from_token(
      token, None, None, None, None, instance_scopes)


def get_creds_from_data(
        access_token: str, parsed_keyfile: Dict[str, str]) -> Credentials:
  """Creates a Credentials instance from parsed service account info.

  The function currently supports two types of credentials.
  Service account key in json format and user account with refresh token.

  Args:
      access_token: An Oauth2 access token. It can be None.
      parsed_keyfile: The service account info in Google format.

  Returns:
      google.auth.service_account.Credentials: The constructed credentials.
  """

  # Initialize the variable to None
  creds = None

  # Check if the parsed_keyfile contains "refresh_token"
  if "refresh_token" in parsed_keyfile:
    logging.info("Identified user credentials in gcloud profile")
    # this is user account credentials with refresh token
    creds = credentials_from_token(
        access_token,
        parsed_keyfile["refresh_token"],
        parsed_keyfile["token_uri"],
        parsed_keyfile["client_id"],
        parsed_keyfile["client_secret"],
        parsed_keyfile["scopes"]
    )
  # Check if the parsed_keyfile contains "private_key"
  elif "private_key" in parsed_keyfile:
    logging.info(
        "Identified service account key credentials in gcloud profile")
    # this is a service account key with private key
    creds = get_creds_from_json(parsed_keyfile)
  else:
    logging.error("unknown type of credentials")

    # Return the constructed credentials
  return creds


def find_creds(explicit_path: Optional[str] = None) -> List[str]:
  """
  The function searches the disk and returns
  a list of files with GCP credentials.

  Args:
      explicit_path: An explicit path on disk to search.
      If None, the function searches in
      standard locations where gcloud profiles are usually located.

  Returns:
      list: The list of files with GCP credentials.
  """

  logging.info("Searching for credentials on disk")
  list_of_creds_files = []

  # Create a list of search paths to scan for credentials.db
  search_paths = []
  if explicit_path is not None and explicit_path != "-":
    search_paths.append(explicit_path)
  else:
    credentials_db_search_places.append(os.getenv("HOME") + "/")
    for dir_path in credentials_db_search_places:
      if not os.access(dir_path, os.R_OK):
        continue
      for subdir_name in os.listdir(dir_path):
        full_path = os.path.join(dir_path, subdir_name, "gcloud")
        search_paths.append(full_path)

    # Scan each search path for credentials.db
    # and add them to the list_of_creds_files
  for dir_path in search_paths:
    print(f"Scanning {dir_path} for credentials.db")
    full_path = os.path.join(dir_path, "credentials.db")
    if os.path.exists(full_path) and os.access(full_path, os.R_OK):
      print(f"Identified accessible gcloud config profile {full_path}")
      list_of_creds_files.append(full_path)

  print(f"Identified {len(list_of_creds_files)} credential DBs")
  return list_of_creds_files


def get_access_tokens_dict(path_to_creds_db: str) -> Dict[str, str]:
  """
  The function searches and extracts OAuth2
  access_tokens from a SQLite3 database.

  Args:
      path_to_creds_db: A path to SQLite3 database with gcloud access tokens.

  Returns:
      dict: The dictionary of account names and corresponding tokens.
  """

  access_tokens_dict = dict()

  # Replace credentials.db with access_tokens.db
  # to get the path to access tokens database
  access_tokens_path = path_to_creds_db.replace("credentials.db",
                                                "access_tokens.db")

  # Check if the access tokens database exists and can be read
  if os.path.exists(access_tokens_path) and os.access(access_tokens_path,
                                                      os.R_OK):

    # If the access tokens database exists and can be read, connect to it
    logging.info("Identified access tokens DB in %s", access_tokens_path)
    conn = sqlite3.connect(access_tokens_path)
    cursor = conn.execute("SELECT account_id, access_token,"
                          "token_expiry FROM access_tokens")

    # Fetch all rows from the access tokens database
    rows = cursor.fetchall()

    # Iterate over each row
    for row in rows:
      associated_account = row[0]
      token = row[1]
      expiration_date = row[2]

      # Omit milliseconds from the expiration date
      expiration_date = expiration_date.split(".")[0]

      # Convert the expiration date to a datetime object
      token_time_obj = datetime.datetime.strptime(
          expiration_date, "%Y-%m-%d %H:%M:%S")

      # Check if the token has expired
      if datetime.datetime.now() > token_time_obj:
        logging.info("Token for %s expired", associated_account)
        continue

            # Add the associated account and
            # token to the access tokens dictionary
      access_tokens_dict[associated_account] = token

  return access_tokens_dict


def extract_creds(path_to_creds_db: str) -> List[
        Tuple[str, str, str]]:
  """
  The function extracts refresh and associated access
  tokens from sqlite3 DBs.

  Args:
      path_to_creds_db (str): A path to sqlite3 DB
      with gcloud refresh tokens.

  Returns:
      List of tuples: (account name, refresh token, access token).
  """
  # Log that we are opening the database
  logging.info("Opening %s DB", path_to_creds_db)

  # Create a named tuple for service accounts
  SA = collections.namedtuple("SA", "account_name, creds, token")

  # Initialize an empty list for the results
  res = list()

  # Connect to the database
  conn = sqlite3.connect(path_to_creds_db)
  # Select account_id and value from the credentials table
  cursor = conn.execute("SELECT account_id, value FROM credentials")
  rows = cursor.fetchall()

  # Check if the database is empty
  if len(rows) <= 0:
    logging.error("Empty database")
    return None

  # We also want to check for access_tokens to avoid unnecessary refreshing
  access_tokens = get_access_tokens_dict(path_to_creds_db)

  # Loop through the rows
  for row in rows:
    access_token = None

    # Check if the access token exists and is valid
    if access_tokens.get(row[0], None) is not None:
      logging.info("Found valid access token for %s", row[0])
      access_token = access_tokens[row[0]]

    # Append the account name, credentials, and access
    # token to the results list
  res.append(SA(row[0], row[1], access_token))

  # Print the number of identified credential entries
  print(f"Identified {len(res)} credential entries")

  # Return the results list
  return res


def get_account_creds_list(gcloud_profile_path: Optional[
        str] = None) -> List[List[Tuple[str, str, str]]]:
  """The function searches and extracts gcloud credentials from disk.

  Args:
      gcloud_profile_path: An explicit gcloud profile path on disk to
      search. If None, the function searches in standard locations where
      gcloud profiles are usually located.

  Returns:
      list: A list of tuples (account name, refresh token, access token).
  """
  accounts = list()  # initialize an empty list
  creds_file_list = find_creds(gcloud_profile_path)
  for creds_file in creds_file_list:
    res = extract_creds(creds_file)
    if res is not None:
      accounts.append(res)
  return accounts  # return the accounts list


def impersonate_sa(iam_client: IAMCredentialsClient,
                   target_account: str) -> Credentials:
  """
  The function is used to impersonate a service account.

  Args:
      iam_client (IAMCredentialsClient): The IAMCredentialsClient object.
      target_account (str): The name of the service account to impersonate.

  Returns:
      Credentials: The constructed credentials.
  """

  # Define the scopes for the service account
  scopes_sa = ["https://www.googleapis.com/auth/cloud-platform"]

  # Generate an access token for the service account
  intermediate_access_token = iam_client.generate_access_token(
      name=target_account,
      scope=scopes_sa,
      retry=None,
      # lifetime="43200"
  )

  # Use the access token to construct credentials
  return credentials_from_token(
      intermediate_access_token.access_token,
      None,
      None,
      None,
      None,
      scopes_sa
  )


def creds_from_access_token(access_token_file):
  """The function is used to obtain Google Auth
  Credentials from access token.

  Args:
      access_token_file: a path to a file with access token
      and scopes stored in JSON format. Example:
      {
          "access_token": "<token>",
          "scopes": [
              "https://www.googleapis.com/auth/devstorage.read_only",
              "https://www.googleapis.com/auth/logging.write",
              "https://www.googleapis.com/auth/monitoring.write",
              "https://www.googleapis.com/auth/servicecontrol",
              "https://www.googleapis.com/auth/service.management.readonly",
              "https://www.googleapis.com/auth/trace.append"
          ]
      }

  Returns:
      google.auth.service_account.Credentials: The constructed credentials.
  """

  # Load the access token and scopes from the specified file
  with open(access_token_file, encoding="utf-8") as f:
    creds_dict = json.load(f)

    # Check if user-defined scopes are provided
  user_scopes = creds_dict.get("scopes", None)
  if user_scopes is None:
        # Use default scopes if not provided
    user_scopes = ["https://www.googleapis.com/auth/cloud-platform"]

  # Construct credentials from the access token and scopes
  return credentials_from_token(
      creds_dict["access_token"],
      None,
      None,
      None,
      None,
      user_scopes
  )


def creds_from_refresh_token(refresh_token_file):
  """
  The function is used to obtain Google Auth Credentials from refresh token.

  Args:
  - refresh_token_file: a path to a file with refresh_token, client_id,
      client_secret, and token_uri stored in JSON format.
      Example:
          {
          "refresh_token": "<token>",
          "client_id": "id",
          "client_secret": "secret",
          scopes: [
              https://www.googleapis.com/auth/devstorage.read_only,
              https://www.googleapis.com/auth/logging.write,
              https://www.googleapis.com/auth/monitoring.write,
              https://www.googleapis.com/auth/servicecontrol,
              https://www.googleapis.com/auth/service.management.readonly,
              https://www.googleapis.com/auth/trace.append
          ]
          }

  Returns:
  - google.auth.service_account.Credentials: The constructed credentials.
  """

  # Open the refresh_token_file in utf-8 encoding
  # and load the contents to a dictionary
  with open(refresh_token_file, encoding="utf-8") as f:
    creds_dict = json.load(f)

  # Get the user-defined scopes from the refresh token dictionary
  user_scopes = get_scopes_from_refresh_token(creds_dict)

  # Construct and return a google.auth.service_account.Credentials object
  return credentials.Credentials(
      None,
      refresh_token=creds_dict["refresh_token"],
      token_uri=creds_dict["token_uri"],
      client_id=creds_dict["client_id"],
      client_secret=creds_dict["client_secret"],
      scopes=user_scopes,
  )


def get_scopes_from_refresh_token(context) -> Union[List[str], None]:
  """
  The function is used to obtain scopes from a refresh token.

  Args:
      context: a dictionary containing refresh token data
          Example:
          {
              "refresh_token": "<token>",
              "client_id": "id",
              "client_secret": "secret",
          }

  Returns:
      a list of scopes or None
  """

  # Obtain access token from the refresh token
  token_uri = "https://oauth2.googleapis.com/token"
  context["grant_type"] = "refresh_token"

  try:
    response = requests.post(token_uri, data=context, timeout=5)

    # prepare the scope string into a list
    raw = response.json().get("scope", None)
    return raw.split(" ") if raw else None

  except ImportError as ex:
    logging.error("Failed to retrieve access token from refresh token.")
    logging.debug("Token refresh exception", exc_info=ex)

  return None
