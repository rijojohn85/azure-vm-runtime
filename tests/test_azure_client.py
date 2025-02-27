import pytest
from typing import List, Dict
from unittest.mock import patch, MagicMock
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
    mock_vm1.resource_group = "rg1"

    mock_vm2 = MagicMock()
    mock_vm2.name = "vm2"
    mock_vm2.resource_group = "rg2"

    mock_compute_client.return_value.virtual_machines.list.return_value = [mock_vm1, mock_vm2]

    vm_dict: Dict[str,str] = get_all_vms()
    assert vm_dict == [{"name": "vm1", "resource_group": "rg1"}, {"name": "vm2", "resource_group": "rg2"}]
