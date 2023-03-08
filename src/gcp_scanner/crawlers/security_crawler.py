import logging
import sys
from typing import List, Dict, Any

from googleapiclient import discovery
from httplib2 import Credentials

class SecurityResourceMeta:
  def __init__(self):
    pass

  def get_kms_keys(self,project_id: str,
                  credentials: Credentials) -> List[Dict[str, Any]]:
    """Retrieve a list of KMS keys available in the project.

    Args:
      project_id: A name of a project to query info about.
      credentials: An google.oauth2.credentials.Credentials object.

    Returns:
      A list of KMS keys in the project.
    """

    logging.info("Retrieving KMS keys")
    kms_keys_list = list()
    try:
      service = discovery.build(
          "cloudkms", "v1", credentials=credentials, cache_discovery=False)

      # list all possible locations
      locations_list = list()
      request = service.projects().locations().list(name=f"projects/{project_id}")
      while request is not None:
        response = request.execute()
        for location in response.get("locations", []):
          locations_list.append(location["locationId"])
        request = service.projects().locations().list_next(
            previous_request=request, previous_response=response)

      for location_id in locations_list:
        request_loc = service.projects().locations().keyRings().list(
            parent=f"projects/{project_id}/locations/{location_id}")
        while request_loc is not None:
          response_loc = request_loc.execute()
          for keyring in response_loc.get("keyRings", []):
            request = service.projects().locations().keyRings().cryptoKeys().list(
                parent=keyring["name"])
            while request is not None:
              response = request.execute()
              for key in response.get("cryptoKeys", []):
                kms_keys_list.append(key)

              request = service.projects().locations().keyRings().cryptoKeys(
              ).list_next(
                  previous_request=request, previous_response=response)

          request_loc = service.projects().locations().keyRings().list_next(
              previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to retrieve KMS keys for project %s", project_id)
      logging.info(sys.exc_info())
    return kms_keys_list

  def get_iam_policy(self,project_name: str,
                    credentials: Credentials) -> List[Dict[str, Any]]:
    """Retrieve an IAM Policy in the project.

    Args:
      project_name: A name of a project to query info about.
      credentials: An google.oauth2.credentials.Credentials object.

    Returns:
      An IAM policy enforced for the project.
    """

    logging.info("Retrieving IAM policy for %s", project_name)
    service = discovery.build(
        "cloudresourcemanager",
        "v1",
        credentials=credentials,
        cache_discovery=False)

    resource = project_name

    get_policy_options = {
        "requestedPolicyVersion": 3,
    }
    get_policy_options = {"options": {"requestedPolicyVersion": 3}}
    try:
      request = service.projects().getIamPolicy(
          resource=resource, body=get_policy_options)
      response = request.execute()
    except Exception:
      logging.info("Failed to get endpoints list for project %s", project_name)
      logging.info(sys.exc_info())
      return None

    if response.get("bindings", None) is not None:
      return response["bindings"]
    else:
      return None


  def get_associated_service_accounts(
      self,iam_policy: List[Dict[str, Any]]) -> List[str]:
    """Extract a list of unique SAs from IAM policy associated with project.

    Args:
      iam_policy: An IAM policy provided by get_iam_policy function.

    Returns:
      A list of service accounts represented as string
    """

    if not iam_policy:
      return []

    list_of_sas = list()
    for entry in iam_policy:
      for member in entry["members"]:
        if "deleted:" in member:
          continue
        account_name = None
        for element in member.split(":"):
          if "@" in element:
            account_name = element
            break
        if account_name and account_name not in list_of_sas:
          list_of_sas.append(account_name)

    return list_of_sas