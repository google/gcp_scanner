import logging
import sys
from typing import List, Dict, Any, Tuple

import googleapiclient
from googleapiclient import discovery
from httplib2 import Credentials

class ProjectResourceMeta:
  def __init__(self):
    pass

  def fetch_project_info(self,project_name: str,
                        credentials: Credentials) -> Dict[str, Any]:
    """Retrieve information about specific project.

    Args:
      project_name: Name of project to request info about
      credentials: An google.oauth2.credentials.Credentials object.

    Returns:
      Project info object or None.
    """
    project_info = None
    logging.info("Retrieving info about: %s", project_name)

    try:
      service = googleapiclient.discovery.build(
          "cloudresourcemanager",
          "v1",
          credentials=credentials,
          cache_discovery=False)
      request = service.projects().get(projectId=project_name)
      response = request.execute()
      if "projectNumber" in response:
        project_info = response

    except Exception:
      logging.info("Failed to enumerate projects")
      logging.info(sys.exc_info())

    return project_info


  def get_project_list(self,credentials: Credentials) -> List[Dict[str, Any]]:
    """Retrieve a list of projects accessible by credentials provided.

    Args:
      credentials: An google.oauth2.credentials.Credentials object.

    Returns:
      A list of Project objects from cloudresourcemanager RestAPI.
    """

    logging.info("Retrieving projects list")
    project_list = list()
    try:
      service = googleapiclient.discovery.build(
          "cloudresourcemanager",
          "v1",
          credentials=credentials,
          cache_discovery=False)
      request = service.projects().list()
      while request is not None:
        response = request.execute()
        project_list = response.get("projects",[])
        request = service.projects().list_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to enumerate projects")
      logging.info(sys.exc_info())
    return project_list

  def get_service_accounts(self,project_name: str,
                          credentials: Credentials) -> List[Tuple[str, str]]:
    """Retrieve a list of service accounts managed in the project.

    Args:
      project_name: A name of a project to query info about.
      credentials: An google.oauth2.credentials.Credentials object.

    Returns:
      A list of service accounts managed in the project.
    """

    logging.info("Retrieving SA list %s", project_name)
    service_accounts = []
    service = discovery.build(
        "iam", "v1", credentials=credentials, cache_discovery=False)

    name = f"projects/{project_name}"

    try:
      request = service.projects().serviceAccounts().list(name=name)
      while request is not None:
        response = request.execute()
        service_accounts = [(service_account["email"],
          service_account.get("description",""))
          for service_account in response.get("accounts",[])]

        request = service.projects().serviceAccounts().list_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to retrieve SA list for project %s", project_name)
      logging.info(sys.exc_info())

    return service_accounts


  def list_services(
      self,project_id: str, credentials: Credentials) -> List[Any]:
    """Retrieve a list of services enabled in the project.

    Args:
      project_id: An id of a project to query info about.
      credentials: An google.oauth2.credentials.Credentials object.

    Returns:
      A list of service API objects enabled in the project.
    """

    logging.info("Retrieving services list %s", project_id)
    list_of_services = list()
    serviceusage = discovery.build("serviceusage", "v1", credentials=credentials)

    request = serviceusage.services().list(
        parent="projects/" + project_id, pageSize=200, filter="state:ENABLED")
    try:
      while request is not None:
        response = request.execute()
        list_of_services.append(response.get("services", None))

        request = serviceusage.services().list_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to retrieve services for project %s", project_id)
      logging.info(sys.exc_info())

    return list_of_services