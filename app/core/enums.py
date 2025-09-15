from enum import Enum


class MigrationState(str, Enum):
    NOT_STARTED = "not_started"
    RUNNING = "running"
    ERROR = "error"
    SUCCESS = "success"


class CloudTypes(str, Enum):
    aws = "aws"
    azure = "azure"
    vsphere = "vsphere"
    vcloud = "vcloud"