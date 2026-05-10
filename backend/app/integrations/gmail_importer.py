from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.gmail_account import get_gmail_account_by_user_id, upsert_gmail_account_tokens
from app.integrations.gmail import GmailClient
from app.integrations.gmail_mappers import map_linkedin_email


LINKEDIN_GMAIL_QUERY = "from:(linkedin.com OR linkedin) OR subject:(LinkedIn)"


async def get_gmail_oauth_url() -> dict:
    client = GmailClient()
    try:
        state = client.generate_state()
        url = client.build_oauth_url(state)
        return {"oauth_url": url, "state": state}
    finally:
        await client.close()


async def exchange_gmail_oauth_code(db: AsyncSession, user_id: int, code: str) -> dict:
    client = GmailClient()
    try:
        token_payload = await client.exchange_code_for_tokens(code)
        access_token = token_payload.get("access_token")
        if not access_token:
            raise ValueError("Google token response did not include access token")

        refresh_token = token_payload.get("refresh_token")
        token_type = token_payload.get("token_type")
        scope = token_payload.get("scope")
        expires_at = client.compute_expires_at(token_payload.get("expires_in"))
        email = await client.get_profile_email(access_token)

        account = await upsert_gmail_account_tokens(
            db=db,
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=token_type,
            expires_at=expires_at,
            scope=scope,
            email=email,
        )
        return {
            "connected": True,
            "email": account.email,
            "expires_at": account.expires_at.isoformat() if account.expires_at else None,
        }
    finally:
        await client.close()


async def get_linkedin_email_preview(db: AsyncSession, user_id: int, limit: int = 20) -> dict:
    account = await get_gmail_account_by_user_id(db, user_id)
    if not account:
        return {"connected": False, "emails_found": 0, "results": []}

    client = GmailClient()
    try:
        access_token = account.access_token
        expires_at = account.expires_at
        now = datetime.now(tz=timezone.utc)
        should_refresh = (
            account.refresh_token is not None
            and expires_at is not None
            and expires_at.replace(tzinfo=timezone.utc) <= now
        )
        if should_refresh:
            refresh_payload = await client.refresh_access_token(account.refresh_token)
            refreshed_access_token = refresh_payload.get("access_token")
            if refreshed_access_token:
                access_token = refreshed_access_token
                account = await upsert_gmail_account_tokens(
                    db=db,
                    user_id=user_id,
                    access_token=refreshed_access_token,
                    refresh_token=account.refresh_token,
                    token_type=refresh_payload.get("token_type") or account.token_type,
                    expires_at=client.compute_expires_at(refresh_payload.get("expires_in")),
                    scope=refresh_payload.get("scope") or account.scope,
                    email=account.email,
                )

        messages_data = await client.list_messages(
            access_token=access_token,
            limit=limit,
            query=LINKEDIN_GMAIL_QUERY,
        )
        message_refs = messages_data.get("messages", [])
        mapped_messages: list[dict] = []
        for message_ref in message_refs:
            message_id = message_ref.get("id")
            if not message_id:
                continue
            message = await client.get_message(access_token=access_token, message_id=message_id)
            mapped_messages.append(map_linkedin_email(message))

        return {
            "connected": True,
            "email": account.email,
            "expires_at": account.expires_at.isoformat() if account.expires_at else None,
            "emails_found": len(mapped_messages),
            "results": mapped_messages,
        }
    finally:
        await client.close()
