from typing import Dict, List
from datetime import datetime, timezone
import os
from azure.identity import DefaultAzureCredential
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

if __name__ == "__main__":
    vm_dict = get_all_vms()
    log_vm_report(vm_dict)