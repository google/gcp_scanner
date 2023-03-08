import logging
import sys
from typing import List, Dict, Any

from googleapiclient import discovery
from httplib2 import Credentials

class NetworkResourceMeta:
  def __init__(self):
    pass

  def get_static_ips(project_name: str,
                    service: discovery.Resource) -> List[Dict[str, Any]]:
    """Retrieve a list of static IPs available in the project.

    Args:
      project_name: A name of a project to query info about.
      service: A resource object for interacting with the Compute API.

    Returns:
      A list of static IPs in the project.
    """

    logging.info("Retrieving Static IPs")

    ips_list = list()
    try:
      request = service.addresses().aggregatedList(project=project_name)
      while request is not None:
        response = request.execute()
        ips_list = [{name: addresses_scoped_list}
          for name, addresses_scoped_list in response["items"].items()
          if addresses_scoped_list.get("addresses", None) is not None]
        request = service.addresses().aggregatedList_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to get static IPs in the %s", project_name)
      logging.info(sys.exc_info())

    return ips_list

  def get_subnets(self,project_name: str,
                  compute_client: discovery.Resource) -> List[Dict[str, Any]]:
    """Retrieve a list of subnets available in the project.

    Args:
      project_name: A name of a project to query info about.
      compute_client: A resource object for interacting with the Compute API.

    Returns:
      A list of subnets in the project.
    """

    logging.info("Retrieving Subnets")
    subnets_list = list()
    try:
      request = compute_client.subnetworks().aggregatedList(project=project_name)
      while request is not None:
        response = request.execute()
        if response.get("items", None) is not None:
          subnets_list = list(response["items"].items())
        request = compute_client.subnetworks().aggregatedList_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to get subnets in the %s", project_name)
      logging.info(sys.exc_info())

    return subnets_list


  def get_firewall_rules(
      self,project_name: str,
      compute_client: discovery.Resource) -> List[Dict[str, Any]]:
    """Retrieve a list of firewall rules in the project.

    Args:
      project_name: A name of a project to query info about.
      compute_client: A resource object for interacting with the Compute API.

    Returns:
      A list of firewall rules in the project.
    """

    logging.info("Retrieving Firewall Rules")
    firewall_rules_list = list()
    try:
      request = compute_client.firewalls().list(project=project_name)
      while request is not None:
        response = request.execute()
        firewall_rules_list=[(firewall["name"],)
          for firewall in response.get("items",[])]
        request = compute_client.firewalls().list_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to get firewall rules in the %s", project_name)
      logging.info(sys.exc_info())
    return firewall_rules_list
  
  def get_managed_zones(self,project_name: str,
                        credentials: Credentials) -> List[Dict[str, Any]]:
    """Retrieve a list of DNS zones available in the project.

    Args:
      project_name: A name of a project to query info about.
      credentials: An google.oauth2.credentials.Credentials object.

    Returns:
      A list of DNS zones in the project.
    """

    logging.info("Retrieving DNS Managed Zones")
    zones_list = list()

    try:
      service = discovery.build(
          "dns", "v1", credentials=credentials, cache_discovery=False)

      request = service.managedZones().list(project=project_name)
      while request is not None:
        response = request.execute()
        zones_list = response.get("managedZones",[])
        request = service.managedZones().list_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to enumerate DNS zones for project %s", project_name)
      logging.info(sys.exc_info())

    return zones_list

  def get_endpoints(self,project_id: str,
                    credentials: Credentials) -> List[Dict[str, Any]]:
    """Retrieve a list of Endpoints available in the project.

    Args:
      project_id: A name of a project to query info about.
      credentials: An google.oauth2.credentials.Credentials object.

    Returns:
      A list of Endpoints in the project.
    """

    logging.info("Retrieving info about endpoints")
    endpoints_list = list()
    try:
      service = discovery.build(
          "servicemanagement",
          "v1",
          credentials=credentials,
          cache_discovery=False)

      request = service.services().list(producerProjectId=project_id)
      while request is not None:
        response = request.execute()
        endpoints_list = response.get("services", [])
        request = service.services().list_next(
            previous_request=request, previous_response=response)
    except Exception:
      logging.info("Failed to retrieve endpoints list for project %s", project_id)
      logging.info(sys.exc_info())
    return endpoints_list