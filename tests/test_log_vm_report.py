import pytest
import logging

from unittest.mock import patch
from src.azure_client import log_vm_report

@pytest.fixture
def mock_logger():
    """Fixture to mock the logger."""
    with patch("logging.info") as mock_logger:
        yield mock_logger

def test_log_vm_report(mock_logger)->None:
    "Test that log_vm_report logs the correct message"
    mock_vm_report = {
         "vm1": {"resource_group": "rg1", "status": "PowerState/running", "running_time": "2:30:00"},
        "vm2": {"resource_group": "rg2", "status": "PowerState/running", "running_time": "5:15:00"},
    }
    log_vm_report(mock_vm_report)
    mock_logger.assert_any_call("VM: vm1")
    mock_logger.assert_any_call("Resource Group: rg1")
    mock_logger.assert_any_call("Status: PowerState/running")
    mock_logger.assert_any_call("Running Time: 2:30:00")
    mock_logger.assert_any_call("VM: vm2")
    mock_logger.assert_any_call("Resource Group: rg2")
    mock_logger.assert_any_call("Status: PowerState/running")
    mock_logger.assert_any_call("Running Time: 5:15:00")

def test_log_vm_no_vms_found(mock_logger)->None:
    "Test that log_vm_report logs the correct message when no VMs are found"
    mock_vm_report = {}
    log_vm_report(mock_vm_report)
    mock_logger.assert_called_with("No Running VMs found")