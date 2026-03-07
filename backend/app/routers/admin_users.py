"""Admin user management router — /api/v1/admin/users/* endpoints."""
import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from app.dependencies import verify_admin
from app.services.user_service import (
    find_user_by_username,
    hash_password,
    load_users,
    save_users,
)

router = APIRouter(tags=["admin-users"])
logger = logging.getLogger("router.admin_users")


@router.get("")
async def list_all_users(admin_id: str = Depends(verify_admin)):
    """List all registered users (passwords excluded)."""
    try:
        users = load_users()
        safe = [{k: v for k, v in u.items() if k != "password"} for u in users]
        return JSONResponse(content={"count": len(safe), "users": safe})
    except Exception as e:
        logger.error(f"List users error: {e}")
        raise HTTPException(status_code=500, detail="Failed to list users")


@router.get("/{username}")
async def get_user_details(username: str, admin_id: str = Depends(verify_admin)):
    """Get detailed user information (password excluded)."""
    try:
        user = find_user_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return JSONResponse(content={k: v for k, v in user.items() if k != "password"})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get user details error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch user details")


@router.post("/{username}/verify")
async def verify_user(username: str, admin_id: str = Depends(verify_admin)):
    """Approve/verify a user account."""
    try:
        users = load_users()
        idx = next((i for i, u in enumerate(users) if u.get("username") == username), None)
        if idx is None:
            raise HTTPException(status_code=404, detail="User not found")
        users[idx].update({"verified": True, "verified_at": datetime.now().isoformat(), "verified_by": admin_id})
        save_users(users)
        logger.info(f"Admin {admin_id} verified user: {username}")
        return JSONResponse(content={"status": "ok", "message": f"User {username} verified successfully"})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Verify user error: {e}")
        raise HTTPException(status_code=500, detail="Verification failed")


@router.post("/{username}/reject")
async def reject_user(username: str, admin_id: str = Depends(verify_admin)):
    """Reject/disapprove a user account."""
    try:
        users = load_users()
        idx = next((i for i, u in enumerate(users) if u.get("username") == username), None)
        if idx is None:
            raise HTTPException(status_code=404, detail="User not found")
        users[idx].update({"verified": False, "rejected_at": datetime.now().isoformat(), "rejected_by": admin_id})
        save_users(users)
        logger.info(f"Admin {admin_id} rejected user: {username}")
        return JSONResponse(content={"status": "ok", "message": f"User {username} rejected"})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Reject user error: {e}")
        raise HTTPException(status_code=500, detail="Rejection failed")


@router.post("/{username}/reset-password")
async def reset_user_password(username: str, request: Request, admin_id: str = Depends(verify_admin)):
    """Reset a user's password (admin only)."""
    try:
        payload = await request.json()
        new_password = str(payload.get("password", ""))
        if not new_password or len(new_password) < 6:
            raise HTTPException(status_code=400, detail="Password must be 6+ characters")

        users = load_users()
        idx = next((i for i, u in enumerate(users) if u.get("username") == username), None)
        if idx is None:
            raise HTTPException(status_code=404, detail="User not found")
        users[idx].update({
            "password": hash_password(new_password),
            "password_reset_at": datetime.now().isoformat(),
            "password_reset_by": admin_id,
        })
        save_users(users)
        logger.info(f"Admin {admin_id} reset password for: {username}")
        return JSONResponse(content={"status": "ok", "message": f"Password reset for {username} successfully"})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Reset password error: {e}")
        raise HTTPException(status_code=500, detail="Password reset failed")


@router.delete("/{username}")
async def delete_user(username: str, admin_id: str = Depends(verify_admin)):
    """Permanently delete a user account."""
    try:
        users = load_users()
        idx = next((i for i, u in enumerate(users) if u.get("username") == username), None)
        if idx is None:
            raise HTTPException(status_code=404, detail="User not found")
        users.pop(idx)
        save_users(users)
        logger.info(f"Admin {admin_id} deleted user: {username}")
        return JSONResponse(content={"status": "ok", "message": f"User {username} deleted successfully"})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete user error: {e}")
        raise HTTPException(status_code=500, detail="User deletion failed")
