import secrets
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

import httpx

from app.core.config import settings


class GmailClient:
    def __init__(self):
        self.auth_base_url = settings.google_auth_base_url
        self.token_url = settings.google_token_url
        self.gmail_api_base_url = settings.google_gmail_api_base_url
        self.client = httpx.AsyncClient(timeout=30.0)

    @staticmethod
    def generate_state() -> str:
        return secrets.token_urlsafe(24)

    def build_oauth_url(self, state: str) -> str:
        if not settings.google_client_id or not settings.google_redirect_uri:
            raise ValueError("Google OAuth credentials are not configured")

        query = urlencode(
            {
                "client_id": settings.google_client_id,
                "redirect_uri": settings.google_redirect_uri,
                "response_type": "code",
                "scope": " ".join(settings.google_oauth_scopes),
                "access_type": "offline",
                "prompt": "consent",
                "state": state,
                "include_granted_scopes": "true",
            }
        )
        return f"{self.auth_base_url}?{query}"

    async def exchange_code_for_tokens(self, code: str) -> dict:
        if not settings.google_client_id or not settings.google_client_secret or not settings.google_redirect_uri:
            raise ValueError("Google OAuth credentials are not configured")

        response = await self.client.post(
            self.token_url,
            data={
                "code": code,
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "redirect_uri": settings.google_redirect_uri,
                "grant_type": "authorization_code",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        return response.json()

    async def refresh_access_token(self, refresh_token: str) -> dict:
        if not settings.google_client_id or not settings.google_client_secret:
            raise ValueError("Google OAuth credentials are not configured")

        response = await self.client.post(
            self.token_url,
            data={
                "refresh_token": refresh_token,
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "grant_type": "refresh_token",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        return response.json()

    async def get_profile_email(self, access_token: str) -> str | None:
        response = await self.client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        response.raise_for_status()
        data = response.json()
        return data.get("email")

    async def list_messages(self, access_token: str, limit: int = 20, query: str | None = None) -> dict:
        params = {"maxResults": limit}
        if query:
            params["q"] = query

        response = await self.client.get(
            f"{self.gmail_api_base_url}/users/me/messages",
            params=params,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        response.raise_for_status()
        return response.json()

    async def get_message(self, access_token: str, message_id: str) -> dict:
        response = await self.client.get(
            f"{self.gmail_api_base_url}/users/me/messages/{message_id}",
            params={"format": "metadata", "metadataHeaders": ["From", "Subject", "Message-ID"]},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def compute_expires_at(expires_in_seconds: int | None) -> datetime | None:
        if not expires_in_seconds:
            return None
        return datetime.now(tz=timezone.utc) + timedelta(seconds=expires_in_seconds)

    async def close(self):
        await self.client.aclose()
