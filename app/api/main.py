import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints.migrations import migration_router
from app.api.endpoints.workloads import workload_router
from app.core.settings import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    # allow_credentials=settings.allow_credentials,
    allow_methods=settings.allow_methods,
    allow_headers=settings.allow_headers,
)

app.include_router(migration_router)
app.include_router(workload_router)

if __name__ == '__main__':
    uvicorn.run(app=app)
