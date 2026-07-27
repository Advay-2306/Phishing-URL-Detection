"""Username/password admin auth with JWT.

The admin signs in at `POST /api/login` with credentials configured via env
vars and receives a short-lived JWT. Protected endpoints (e.g. `/api/logs`)
require it as `Authorization: Bearer <token>`.

Config (environment variables):
  ADMIN_USERNAME   : admin login name (default "admin")
  ADMIN_PASSWORD   : admin password (default "admin" — CHANGE this!)
  JWT_SECRET       : key used to sign tokens (CHANGE this in production!)
  JWT_EXPIRE_HOURS : token lifetime in hours (default 12)
"""
import os
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

_bearer = HTTPBearer(auto_error=False)
_ALGORITHM = "HS256"


def _admin_username() -> str:
    return os.getenv("ADMIN_USERNAME", "admin")


def _admin_password() -> str:
    return os.getenv("ADMIN_PASSWORD", "admin")


def _jwt_secret() -> str:
    return os.getenv("JWT_SECRET", "dev-insecure-secret-change-me")


def _expire_hours() -> int:
    try:
        return int(os.getenv("JWT_EXPIRE_HOURS", "12"))
    except ValueError:
        return 12


def authenticate(username: str, password: str) -> bool:
    """Constant-time check of submitted credentials against env config."""
    user_ok = secrets.compare_digest(username or "", _admin_username())
    pass_ok = secrets.compare_digest(password or "", _admin_password())
    return user_ok and pass_ok


def create_token(username: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "role": "admin",
        "iat": now,
        "exp": now + timedelta(hours=_expire_hours()),
    }
    return jwt.encode(payload, _jwt_secret(), algorithm=_ALGORITHM)


def require_admin(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
) -> dict:
    """FastAPI dependency: allow only requests carrying a valid admin JWT."""
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin sign-in required.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(
            credentials.credentials, _jwt_secret(), algorithms=[_ALGORITHM]
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired. Please sign in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": payload.get("sub"), "role": payload.get("role")}
