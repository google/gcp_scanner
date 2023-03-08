import logging
import sys
from typing import List, Dict, Any, Tuple

from google.cloud import container_v1
import requests
from requests.auth import HTTPBasicAuth

class GKEResourceMeta:
  def __init__(self):
    pass

  def get_gke_clusters(
      self,project_name: str, gke_client: container_v1.services.cluster_manager.client
      .ClusterManagerClient
  ) -> List[Tuple[str, str]]:
    """Retrieve a list of GKE clusters available in the project.

    Args:
      project_name: A name of a project to query info about.
      gke_client: I do not know TBD.

    Returns:
      A list of GKE clusters in the project.
    """

    logging.info("Retrieving list of GKE clusters")
    parent = f"projects/{project_name}/locations/-"
    try:
      clusters = gke_client.list_clusters(parent=parent)
      return [(cluster.name, cluster.description)
        for cluster in clusters.clusters]
    except Exception:
      logging.info("Failed to retrieve cluster list for project %s", project_name)
      logging.info(sys.exc_info())
      return []


  def get_gke_images(
      self,project_name: str, access_token: str) -> Dict[str, Any]:
    """Retrieve a list of GKE images available in the project.

    Args:
      project_name: A name of a project to query info about.
      access_token: An Oauth2 token with permissions to query list of gke images.

    Returns:
      A gke images JSON object for each accessible zone.
    """

    images = dict()
    logging.info("Retrieving list of GKE images")
    project_name = project_name.replace(":", "/")
    regions = ["", "us.", "eu.", "asia."]
    for region in regions:
      gcr_url = f"https://{region}gcr.io/v2/{project_name}/tags/list"
      try:
        res = requests.get(
            gcr_url, auth=HTTPBasicAuth("oauth2accesstoken", access_token))
        if not res.ok:
          logging.info("Failed to retrieve gcr images list. Status code: %d",
                      res.status_code)
          continue
        images[region.replace(".", "")] = res.json()
      except Exception:
        logging.info("Failed to retrieve gke images for project %s", project_name)
        logging.info(sys.exc_info())

    return images