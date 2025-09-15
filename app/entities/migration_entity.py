import asyncio

from app.core.settings import settings
from app.models.models import Migration, MigrationState, Workload


class MigrationEntity:
    def __init__(self, migration: Migration, source: Workload):
        self.migration = migration
        self.source = source

    async def run(self, minutes: float = settings.default_migration_sleep_minutes):
        # бизнес-правила: C:\ должен быть выбран
        source_mps = {mp.name for mp in self.source.storage}
        if "C:\\" in source_mps and "C:\\" not in set(self.migration.selected_mountpoints):
            self.migration.state = MigrationState.ERROR
            self.migration.error_message = "C:\\ present but not selected"
            return self.migration

        # запускаем миграцию
        self.migration.state = MigrationState.RUNNING
        await asyncio.sleep(minutes * 60)

        # копируем только выбранные тома
        selected = set(self.migration.selected_mountpoints)
        filtered = [mp for mp in self.source.storage if mp.name in selected]
        target_vm = self.migration.migration_target.target_vm.model_copy(update={"storage": filtered})

        # успешное завершение
        self.migration = self.migration.model_copy(update={
            "state": MigrationState.SUCCESS,
            "migration_target": self.migration.migration_target.model_copy(update={"target_vm": target_vm})
        })
        return self.migration
