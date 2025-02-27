import pytest
from datetime import timedelta

from src.azure_client import filter_vms_by_runtime

def test_filter_vms_by_runtime()->None:
    """Test Filter VMs by runtime"""
    vm_dict = {
        "vm1": {"resource_group": "rg1", "status": "PowerState/running", "running_time": timedelta(days=1)},
        "vm2": {"resource_group": "rg2", "status": "PowerState/running", "running_time": timedelta(days=2)},
        "vm3": {"resource_group": "rg3", "status": "PowerState/running", "running_time": timedelta(days=3)}
    }
    threshold = timedelta(hours=24)

    filtered_vms = filter_vms_by_runtime(vm_dict, threshold)
    assert "vm1" not in filtered_vms
    assert "vm2" in filtered_vms
    assert "vm3" in filtered_vms
    assert len(filtered_vms) == 2

