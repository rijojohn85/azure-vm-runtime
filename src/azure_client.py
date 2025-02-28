from typing import Dict, List
from datetime import datetime, timezone, timedelta
import os
from azure.identity import ManagedIdentityCredential, DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from src.log_vm_report import log_vm_report

def get_all_vms()->Dict[str,str]:
    """
    Fetch all Vms and their associated resource groups from Azure
    Retruns:
    Dict[str,str]: A dictionary where keys are VMs and the values are resource groups
    """
    sub_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    if not sub_id:
        raise ValueError("Set AZURE_SUBSCRIPTION_ID environment variable")
    if os.environ.get("AZURE_USE_MANAGED_IDENTITY", "false").lower() == "true":
        credential = ManagedIdentityCredential()
    else:
        credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, sub_id)
    vms = compute_client.virtual_machines.list_all()
    vm_dict = {}
    for vm in vms:
        array = vm.id.split("/")
        resource_group = array[4]
        vm_name = array[-1]
        statuses = compute_client.virtual_machines.instance_view(resource_group, vm_name).statuses
        running_time = datetime.now(timezone.utc) - statuses[0].time
        if statuses[1].code == "PowerState/running":
            vm_dict[vm_name] = {"resource_group": resource_group, "status": statuses[1].code, "running_time": running_time}


    return vm_dict

def filter_vms_by_runtime(vm_dict: Dict[str, Dict[str, str]], threshold: timedelta) -> Dict[str, Dict[str, str]]:
    """
    Filter VMs by running time
    Args:
    vm_dict(Dict[str, Dict[str, str]]): A dictionary where keys are VMs and values are dictionaries containing resource group, status and running time
    Returns:
    Dict[str, Dict[str, str]]: A dictionary where keys are VMs and values are dictionaries containing resource group, status and running time
    """
    return {vm: vm_info for vm, vm_info in vm_dict.items() if vm_info["running_time"] > threshold}

if __name__ == "__main__":
    vm_dict = get_all_vms()
    filtered_vms = filter_vms_by_runtime(vm_dict, timedelta(hours=24))
    log_vm_report(vm_dict)