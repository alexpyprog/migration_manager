from typing import List, Optional

from app.models import Workload
from app.storage.storage import Repository


class WorkloadManager:
    def __init__(self):
        self.repo = Repository("workloads", Workload, key="ip")

    def create(self, workload: Workload) -> None:
        self.repo.add(workload)

    def list(self) -> List[Workload]:
        return self.repo.list()

    def get(self, ip: str) -> Optional[Workload]:
        return self.repo.get(ip)

    def get_by_id(self, wl_id: str) -> Optional[Workload]:
        self.repo.key = 'id'
        wl = self.repo.get(wl_id)
        self.repo.key = 'ip'
        return wl

    def update(self, ip: str, update: dict) -> None:
        self.repo.update(ip, update)

    def delete(self, ip: str) -> None:
        self.repo.delete(ip)
