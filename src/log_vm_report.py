import logging
from typing import Dict
import aiohttp
import os

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

async def send_report_to_slack(vm_dict: Dict[str, Dict[str,str]])-> None:
    """
    Send the VM Report to a slack channel
    Args:
    vm_dict(Dict[str, Dict[str, str]]): A dictionary where keys are VMs and values are dictionaries containing resource group, status and running time
    """
    slack_webhook_url: str = os.environ.get("SLACK_WEBHOOK_URL")
    if not slack_webhook_url:
        logging.error("Slack Webhook URL not found, please enable it into the environment variables")
        return
    message: str=""
    if not vm_dict:
        message = "No Running VMs found"
    else:
        for vm, vm_info in vm_dict.items():
            message += f"VM: {vm}\n"
            message += f"Resource Group: {vm_info['resource_group']}\n"
            message += f"Status: {vm_info['status']}\n"
            message += f"Running Time: {vm_info['running_time']}\n\n"
            message += "--------------------------------------\n"
    logging.info("Sending report to slack")
    payload = {"text": message}

    async with aiohttp.ClientSession() as session:
        try:
            response = await session.post(slack_webhook_url, json=payload)
            # with session.post(slack_webhook_url, json=payload) as response:
            if response.status == 200:
                logging.info("Report sent to slack successfully")
            else:
                logging.error(f"Error sending report to slack, status code: {response.status}")
        except Exception as e:
            logging.error(f"Error sending report to slack: {str(e)}")