import pytest
from typing import Dict
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone, timedelta
from src.azure_client import get_all_vms


@pytest.fixture
def mock_compute_client():
    """Fixture to mock the Azure ComputeManagementClient."""
    with patch("src.azure_client.ComputeManagementClient") as mock_compute_client:
        yield mock_compute_client
def test_get_all_vms(mock_compute_client)-> None:
    """Test get all VMs"""
    mock_vm1 = MagicMock()
    mock_vm1.name = "vm1"
    mock_vm1.id = "subscriptions/123/resourceGroups/providers/rg1/Microsoft.Compute/virtualMachines/vm1"

    mock_vm2 = MagicMock()
    mock_vm2.name = "vm2"
    mock_vm2.id = "subscriptions/123/resourceGroups/providers/rg2/Microsoft.Compute/virtualMachines/vm2"

    mock_vm1_statuses = [MagicMock(code="ProvisioningState/successful", time=datetime(2024, 2,26,10,0,0,tzinfo=timezone.utc)), MagicMock(code="PowerState/running")]
    mock_vm2_statuses = [MagicMock(code="ProvisioningState/successful", time=datetime(2024, 2,26,9,0,0,tzinfo=timezone.utc)), MagicMock(code="PowerState/stopped")]
    def mock_instance_view(resource_group, vm_name):
        if vm_name == "vm1":
            return MagicMock(statuses=mock_vm1_statuses)
        elif vm_name == "vm2":
            return MagicMock(statuses=mock_vm2_statuses)
    mock_compute_client.return_value.virtual_machines.list_all.return_value = [mock_vm1, mock_vm2]
    mock_compute_client.return_value.virtual_machines.instance_view.side_effect = mock_instance_view


    vm_dict: Dict[str,str] = get_all_vms()
    assert "vm1" in vm_dict
    assert "vm2" not in vm_dict
    assert vm_dict["vm1"]["resource_group"] == "rg1"
    assert vm_dict["vm1"]["status"] == "PowerState/running"
    assert isinstance(vm_dict["vm1"]["running_time"], timedelta) # This is a timedelta object
