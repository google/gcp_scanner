import logging
import sys
from typing import List, Any

from googleapiclient import discovery
from httplib2 import Credentials

class RepoResourceMeta:
  def __init__(self):
    pass

  def list_sourcerepo(
      self,project_id: str, credentials: Credentials) -> List[Any]:
    """Retrieve a list of cloud source repositories enabled in the project.

    Args:
      project_id: An id of a project to query info about.
      credentials: An google.oauth2.credentials.Credentials object.

    Returns:
      A list of cloud source repositories in the project.
    """

    logging.info("Retrieving cloud source repositories %s", project_id)
    list_of_repos = list()
    service = discovery.build("sourcerepo", "v1", credentials=credentials)

    request = service.projects().repos().list(
      name="projects/" + project_id,
      pageSize=500
    )
    try:
      while request is not None:
        response = request.execute()
        list_of_repos.append(response.get("repos", None))

        request = service.projects().repos().list_next(
          previous_request=request,
          previous_response=response
        )
    except Exception:
      logging.info("Failed to retrieve source repos for project %s", project_id)
      logging.info(sys.exc_info())

    return list_of_repos