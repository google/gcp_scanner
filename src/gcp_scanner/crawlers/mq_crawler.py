import logging
import sys
from typing import List, Dict, Any

from googleapiclient import discovery
from httplib2 import Credentials

class MQResourceMeta:
  def __init__(self):
    pass

  def get_pubsub_subscriptions(self,project_id: str,
                              credentials: Credentials) -> List[Dict[str, Any]]:
    """Retrieve a list of PubSub subscriptions available in the project.

    Args:
      project_id: A name of a project to query info about.
      credentials: An google.oauth2.credentials.Credentials object.

    Returns:
      A list of PubSub subscriptions in the project.
    """

    logging.info("Retrieving PubSub Subscriptions")
    pubsubs_list = list()
    try:
      service = discovery.build(
          "pubsub", "v1", credentials=credentials, cache_discovery=False)

      request = service.projects().subscriptions().list(
          project=f"projects/{project_id}")
      while request is not None:
        response = request.execute()
        pubsubs_list = response.get("subscriptions", [])
        request = service.projects().subscriptions().list_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to get PubSubs for project %s", project_id)
      logging.info(sys.exc_info())
    return pubsubs_list