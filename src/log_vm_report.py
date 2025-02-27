import logging
from typing import Dict

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def log_vm_report(vm_dict: Dict[str, Dict[str, str]])-> None:
    """
    Log the VM report
    Args:
    vm_dict(Dict[str, Dict[str, str]]): A dictionary where keys are VMs and values are dictionaries containing resource group, status and running time
    """
    if not vm_dict:
        logging.info("No Running VMs found")
        return
    for vm, vm_info in vm_dict.items():
        logging.info(f"VM: {vm}")
        logging.info(f"Resource Group: {vm_info['resource_group']}")
        logging.info(f"Status: {vm_info['status']}")
        logging.info(f"Running Time: {vm_info['running_time']}")
        logging.info("\n")