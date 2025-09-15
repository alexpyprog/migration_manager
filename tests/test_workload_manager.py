import pytest
from uuid import uuid4
from app.models.models import Workload, MountPoint, Credentials
from app.managers import WorkloadManager


@pytest.fixture
def workload_mgr():
    return WorkloadManager()


def test_create_and_get_workload(workload_mgr):
    all_wls = workload_mgr.list()
    for wl in all_wls:
        workload_mgr.delete(wl.ip)
    all_wls = workload_mgr.list()
    assert len(all_wls) == 0
    w = Workload(
        id=str(uuid4()),
        ip="192.168.1.10",
        credentials=Credentials(username="user", password="password123", domain="domain.local"),
        storage=[MountPoint(name="C:\\", total_size=1024)]
    )
    workload_mgr.create(w)
    fetched = workload_mgr.get(w.ip)
    assert fetched.ip == w.ip
