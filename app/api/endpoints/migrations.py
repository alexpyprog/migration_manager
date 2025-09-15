from uuid import UUID

from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from app.core.enums import MigrationState
from app.entities.migration_entity import MigrationEntity
from app.managers import MigrationManager, WorkloadManager
from app.models import *

migration_mgr = MigrationManager()
workload_mgr = WorkloadManager()
migration_router = APIRouter(
    tags=["Migration"],
)


@migration_router.get("/migrations")
def list_migrations():
    return migration_mgr.list()


@migration_router.post("/migrations")
def create_migration(migration: Migration):
    try:
        migration_mgr.create(migration)
        return migration
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@migration_router.get("/migrations/{mid}")
def get_migration(mid: UUID):
    m = migration_mgr.get(mid)
    if not m:
        raise HTTPException(status_code=404, detail="Migration not found")
    return m


@migration_router.put("/migrations/{mid}")
def update_migration(mid: UUID, update: dict):
    try:
        migration_mgr.update(mid, update)
        return migration_mgr.get(mid)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@migration_router.delete("/migrations/{mid}")
def delete_migration(mid: UUID):
    try:
        migration_mgr.delete(mid)
        return {"detail": "deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@migration_router.post("/migrations/{mid}/run")
async def run_migration(mid: UUID, minutes: float = 0.01):
    migration = migration_mgr.get(mid)
    if not migration:
        raise HTTPException(status_code=404, detail="Migration not found")

    source = workload_mgr.get_by_id(migration.source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source workload not found")

    entity = MigrationEntity(migration, source)
    result = await entity.run(minutes=minutes)

    # Обновляем в хранилище
    migration_mgr.update(mid, result.model_dump())
    if result.state == MigrationState.ERROR:
        raise HTTPException(status_code=400, detail=result.error_message)

    return result