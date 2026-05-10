from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.gmail_account import GmailAccount


async def get_gmail_account_by_user_id(db: AsyncSession, user_id: int) -> GmailAccount | None:
    result = await db.execute(select(GmailAccount).where(GmailAccount.user_id == user_id))
    return result.scalars().first()


async def upsert_gmail_account_tokens(
    db: AsyncSession,
    user_id: int,
    access_token: str,
    refresh_token: str | None,
    token_type: str | None,
    expires_at: datetime | None,
    scope: str | None,
    email: str | None = None,
) -> GmailAccount:
    account = await get_gmail_account_by_user_id(db, user_id)
    if account is None:
        account = GmailAccount(
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=token_type,
            expires_at=expires_at,
            scope=scope,
            email=email,
        )
        db.add(account)
    else:
        account.access_token = access_token
        # Keep existing refresh token if Google does not return one.
        if refresh_token:
            account.refresh_token = refresh_token
        account.token_type = token_type
        account.expires_at = expires_at
        account.scope = scope
        if email:
            account.email = email

    await db.commit()
    await db.refresh(account)
    return account
