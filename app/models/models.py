from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from typing import List, Optional

from app.core.enums import CloudTypes, MigrationState


class Credentials(BaseModel):
    username: str = Field(..., min_length=1, description="Имя пользователя")
    password: str = Field(..., min_length=8, description="Пароль")
    domain: str = Field(..., min_length=1, description="Домен")


class MountPoint(BaseModel):
    name: str = Field(..., description="Имя точки монтирования, например 'C:\\'")
    total_size: int = Field(..., gt=0, description="Размер тома в байтах")


class Workload(BaseModel):
    id: str = Field(default=str(uuid4()))
    ip: str = Field(..., description="IP-адрес источника")
    credentials: Credentials
    storage: List[MountPoint]


class MigrationTarget(BaseModel):
    cloud_type: CloudTypes
    cloud_credentials: Credentials
    target_vm: Workload


class Migration(BaseModel):
    id: str = Field(default=str(uuid4()))
    selected_mountpoints: List[str]
    source_id: str = Field(default=str(uuid4()))
    migration_target: MigrationTarget
    state: MigrationState = MigrationState.NOT_STARTED
    error_message: Optional[str] = None