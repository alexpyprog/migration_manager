from uuid import uuid4

import pytest

from app.entities.migration_entity import MigrationEntity
from app.managers.migration_manager import MigrationManager
from app.managers.workload_manager import WorkloadManager
from app.models.models import Workload, MountPoint, Migration, MigrationTarget, Credentials, CloudTypes, MigrationState


@pytest.fixture
def migration_mgr():
    return MigrationManager()


@pytest.fixture
def workload_mgr():
    return WorkloadManager()


@pytest.mark.asyncio
async def test_run_success(migration_mgr, workload_mgr):
    source = Workload(
        id=str(uuid4()),
        ip="192.168.1.20",
        credentials=Credentials(username="user", password="password123", domain="domain.local"),
        storage=[MountPoint(name="C:\\", total_size=1024)]
    )
    migration = Migration(
        id=str(uuid4()),
        selected_mountpoints=["C:\\"],
        source_id=source.id,
        migration_target=MigrationTarget(
            cloud_type=CloudTypes.aws,
            cloud_credentials=Credentials(username="clouduser", password="cloudpass123", domain="cloud.local"),
            target_vm=source
        )
    )
    entity = MigrationEntity(migration, source)
    result = await entity.run(minutes=0.001)
    assert result.state == MigrationState.SUCCESS
    assert len(result.migration_target.target_vm.storage) == 1
    migration_mgr.delete(migration.id)
    workload_mgr.delete(source.ip)


@pytest.mark.asyncio
async def test_run_error():
    # создаём исходный workload
    source = Workload(
        id=str(uuid4()),
        ip="192.168.1.1",
        credentials=Credentials(
            username="clouduser",
            password="cloudpass123",
            domain="cloud.local"
        ),
        storage=[MountPoint(name="C:\\", total_size=1024)]
    )

    # создаём миграцию, где C:\ не выбран
    migration = Migration(
        id=str(uuid4()),
        selected_mountpoints=["E:\\"],
        source_id=source.id,
        migration_target=MigrationTarget(
            cloud_type=CloudTypes.aws,
            cloud_credentials=Credentials(username="clouduser", password="cloudpass123", domain="cloud.local"),
            target_vm=source
        )
    )

    # создаём MigrationEntity и запускаем
    entity = MigrationEntity(migration, source)
    result = await entity.run(minutes=0.001)

    # проверяем состояние
    assert result.state == MigrationState.ERROR
    assert result.error_message == "C:\\ present but not selected"

    # target_vm.storage при ошибке не должен изменяться
    assert result.migration_target.target_vm.storage == source.storage
