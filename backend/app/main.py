from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import logging
import pathlib
import os

from app.routers import auth, cases, admin_users, admin_cases, pages
from app.core.config import get_settings

# Configuration
settings = get_settings()
app = FastAPI(title=settings.app_name, debug=settings.debug)

# Configure logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger("app.main")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
BASE_DIR = pathlib.Path(__file__).parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Mount uploads directory for serving documents
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    from app.services.user_service import create_demo_user
    create_demo_user()
    logger.info(f"{settings.app_name} v1.0.0 started")

# Include Routers
# NOTE: pages.router should typically be included first if it has catch-all or default routes
app.include_router(pages.router)
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(cases.router, prefix="/api/v1")
app.include_router(admin_users.router, prefix="/api/v1/admin/users")
app.include_router(admin_cases.router, prefix="/api/v1/admin")

logger.info("Including routers: pages, auth, cases, admin_users, admin_cases")
