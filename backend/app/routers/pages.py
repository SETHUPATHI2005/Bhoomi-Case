"""HTML page-serving router — all GET routes that return a static HTML file."""
import pathlib

from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse

router = APIRouter(tags=["pages"])

BASE_DIR = pathlib.Path(__file__).resolve().parents[1]  # → backend/app/
STATIC = BASE_DIR / "static"


@router.get("/health")
async def health():
    """Health check — used by Docker and load balancers."""
    return JSONResponse(content={"status": "ok", "version": "1.0.0"})


@router.get("/")
async def landing():
    return FileResponse(STATIC / "landing.html")


@router.get("/search")
async def search_page():
    return FileResponse(STATIC / "index.html")


@router.get("/login")
async def login_page():
    return FileResponse(STATIC / "login.html")


@router.get("/auth")
async def auth_page():
    return FileResponse(STATIC / "auth.html")


@router.get("/register")
async def register_page():
    return FileResponse(STATIC / "register.html")


@router.get("/dashboard")
async def dashboard_page():
    return FileResponse(STATIC / "dashboard.html")


@router.get("/admin-login")
async def admin_login_page():
    """Admin login page (was previously missing from main.py)."""
    return FileResponse(STATIC / "admin-login.html")


@router.get("/admin")
async def admin_page():
    return FileResponse(STATIC / "admin.html")


@router.get("/forgot-password")
async def forgot_password_page():
    return FileResponse(STATIC / "forgot-password.html")


@router.get("/verify-email")
async def verify_email_page():
    return FileResponse(STATIC / "verify-email.html")


@router.get("/reset-password")
async def reset_password_page():
    return FileResponse(STATIC / "reset-password.html")
