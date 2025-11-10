"""
Main FastAPI application entry point.
Orchestrates all automation services.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from backend.api import routes
from backend.services.orchestrator import AutomationOrchestrator
from backend.config.settings import get_settings

settings = get_settings()

# Global orchestrator instance
orchestrator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    global orchestrator
    # Startup
    orchestrator = AutomationOrchestrator()
    await orchestrator.initialize()
    
    yield
    
    # Shutdown
    if orchestrator:
        await orchestrator.shutdown()


app = FastAPI(
    title="Automated Dropshipping System",
    description="Fully automated dropshipping business platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes.router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "status": "running",
        "service": "Automated Dropshipping System",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

