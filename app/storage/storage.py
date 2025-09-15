import json
from typing import Any, Optional, Type, TypeVar

from pydantic import BaseModel

from app.core.settings import settings

T = TypeVar("T", bound=BaseModel)


class Repository:
    def __init__(self, entity: str, model: Type[T], key: str):
        """
        :param entity: имя сущности (например "workloads")
        :param model: Pydantic-модель
        :param key: уникальное поле (например "ip" для Workload)
        """
        self.entity = entity
        self.model = model
        self.key = key
        self.data_dir = settings.data_dir
        self.data_dir.mkdir(exist_ok=True)
        self.file = self.data_dir / f"{entity}.json"

    def _load(self) -> list[dict[str, Any]]:
        if not self.file.exists():
            return []
        with self.file.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, items: list[dict[str, Any]]) -> None:
        with self.file.open("w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)

    def list(self) -> list[T]:
        return [self.model.model_validate(obj) for obj in self._load()]

    def get(self, value: Any) -> Optional[T]:
        for obj in self._load():
            if obj.get(self.key) == value:
                return self.model.model_validate(obj)
        return None

    def add(self, item: T) -> None:
        items = self._load()
        if any(obj.get(self.key) == getattr(item, self.key) for obj in items):
            raise ValueError(
                f"{self.entity} with {self.key}={getattr(item, self.key)} already exists"
            )
        items.append(item.model_dump())
        self._save(items)

    def update(self, value: Any, update: dict[str, Any]) -> None:
        items = self._load()
        updated = False
        for obj in items:
            if obj.get(self.key) == value:
                if self.key in update and update[self.key] != obj[self.key]:
                    raise ValueError(f"{self.key} cannot be changed")
                obj.update(update)
                updated = True
                break
        if not updated:
            raise ValueError(f"{self.entity} with {self.key}={value} not found")
        self._save(items)

    def delete(self, value: Any) -> None:
        items = self._load()
        new_items = [obj for obj in items if obj.get(self.key) != value]
        self._save(new_items)
