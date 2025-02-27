from typing import Dict, List
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

def get_all_vms()->Dict[str,str]:
    """
    Fetch all Vms and their associated resource groups from Azure
    Retruns:
    Dict[str,str]: A dictionary where keys are VMs and the values are resource groups
    """
    sub_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, "your_subscription_id")