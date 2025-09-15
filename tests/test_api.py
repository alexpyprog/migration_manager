import uuid

import pytest
from httpx import AsyncClient, ASGITransport

from app.api.main import app


@pytest.mark.asyncio
async def test_workload_crud_and_migration():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        # CREATE workload
        resp = await ac.post("/workloads", json={
            "id": str(uuid.uuid4()),
            "ip": "192.168.1.50",
            "credentials": {
                "username": "user",
                "password": "password123",
                "domain": "domain.local"
            },
            "storage": [
                {
                    "name": "C:\\",
                    "total_size": 1024
                }
            ]
        })
        assert resp.status_code == 200
        workload = resp.json()
        workload_id = workload["id"]

        # CREATE migration
        resp = await ac.post("/migrations", json={
            "selected_mountpoints": ["C:\\"],
            "source_id": workload_id,
            "migration_target": {
                "cloud_type": "aws",
                "cloud_credentials": {"username": "clouduser", "password": "cloudpass123", "domain": "cloud.local"},
                "target_vm": {
                    "id": workload_id,
                    "ip": "192.168.1.50",
                    "credentials": {"username": "user", "password": "password123", "domain": "domain.local"},
                    "storage": [{"name": "C:\\", "total_size": 1024}]
                }
            }
        })
        assert resp.status_code == 200
        migration_id = resp.json()["id"]

        # RUN migration
        resp = await ac.post(f"/migrations/{migration_id}/run", params={"minutes": 0.001})
        assert resp.status_code == 200
        result = resp.json()
        assert result["state"] == "success"

        # GET migration
        resp = await ac.get(f"/migrations/{migration_id}")
        assert resp.status_code == 200
        assert resp.json()["id"] == migration_id
