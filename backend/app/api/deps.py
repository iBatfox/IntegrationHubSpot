from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from app.core.security import decode_access_token
from app.core.database import get_db
from app.crud.user import get_user_by_email
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    try:
        payload = decode_access_token(token)
        email: str | None = payload.get("sub")
        if email is None:
            raise ValueError
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    # Placeholder for future active checks (e.g., is_active flag)
    return current_user


async def get_current_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    if getattr(current_user, "role", None) != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient privileges",
        )
    return current_user
