"""REST API for Mininet."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mininet3.api.routes import core_v1, topology_v1

app = FastAPI(
    title="Mininet",
    description="Mininet Network Simulation REST API.",
    version="0.0.1",
)
# Allow CORS generic discovery.
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Register routes.
app.include_router(core_v1.Router, prefix='/core')
app.include_router(topology_v1.Router, prefix='/topology')


@app.get('/')
async def heartbeat() -> str:
    """Provide a simple heartbeat mechanism for the API."""
    return 'OK'
