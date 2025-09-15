from typing import List, Optional

from app.models import Migration
from app.storage.storage import Repository


class MigrationManager:
    def __init__(self):
        self.repo = Repository("migrations", Migration, key="id")

    def create(self, migration: Migration) -> None:
        self.repo.add(migration)

    def list(self) -> List[Migration]:
        return self.repo.list()

    def get(self, mid: str) -> Optional[Migration]:
        return self.repo.get(str(mid))

    def update(self, mid: str, update: dict) -> None:
        self.repo.update(str(mid), update)

    def delete(self, mid: str) -> None:
        self.repo.delete(str(mid))
