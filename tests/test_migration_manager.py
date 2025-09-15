from uuid import uuid4

import pytest

from app.managers import MigrationManager
from app.models.models import Migration, Workload, MigrationTarget, Credentials, CloudTypes, MountPoint


@pytest.fixture
def migration_mgr():
    return MigrationManager()


@pytest.fixture
def source_workload():
    return Workload(
        id=str(uuid4()),
        ip="192.168.1.100",
        credentials=Credentials(username="user", password="password123", domain="domain.local"),
        storage=[MountPoint(name="C:\\", total_size=1024)]
    )


@pytest.fixture
def migration_obj(source_workload):
    return Migration(
        id=str(uuid4()),
        selected_mountpoints=["C:\\"],
        source_id=source_workload.id,
        migration_target=MigrationTarget(
            cloud_type=CloudTypes.aws,
            cloud_credentials=Credentials(username="clouduser", password="cloudpass123", domain="cloud.local"),
            target_vm=source_workload
        )
    )


def test_create_and_get_migration(migration_mgr, migration_obj):
    migration_mgr.create(migration_obj)
    fetched = migration_mgr.get(migration_obj.id)
    assert fetched.id == migration_obj.id
    assert fetched.source_id == migration_obj.source_id


def test_update_migration_state(migration_mgr, migration_obj):
    migration_mgr.create(migration_obj)
    migration_mgr.update(migration_obj.id, {"state": "running"})
    fetched = migration_mgr.get(migration_obj.id)
    assert fetched.state == "running"


def test_delete_migration(migration_mgr, migration_obj):
    migration_mgr.create(migration_obj)
    migration_mgr.delete(migration_obj.id)
    fetched = migration_mgr.get(migration_obj.id)
    assert fetched is None


def test_list_migrations(migration_mgr, migration_obj):
    all_migrations = migration_mgr.list()
    for migration in all_migrations:
        migration_mgr.delete(migration.id)
    migration_mgr.create(migration_obj)
    all_migrations = migration_mgr.list()
    assert len(all_migrations) == 1
    assert all_migrations[0].id == migration_obj.id
