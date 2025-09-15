from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from app.managers import WorkloadManager
from app.models import *

workload_mgr = WorkloadManager()
workload_router = APIRouter(
    tags=["Workload"],
)


@workload_router.get("/workloads")
def list_workloads():
    return workload_mgr.list()


@workload_router.post("/workloads")
def create_workload(workload: Workload):
    try:
        workload_mgr.create(workload)
        return workload
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@workload_router.get("/workloads/{ip}")
def get_workload(ip: str):
    w = workload_mgr.get(ip)
    if not w:
        raise HTTPException(status_code=404, detail="Workload not found")
    return w


@workload_router.put("/workloads/{ip}")
def update_workload(ip: str, update: dict):
    try:
        workload_mgr.update(ip, update)
        return workload_mgr.get(ip)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@workload_router.delete("/workloads/{ip}")
def delete_workload(ip: str):
    try:
        workload_mgr.delete(ip)
        return {"detail": "deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
