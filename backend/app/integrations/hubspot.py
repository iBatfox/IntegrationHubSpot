import logging

import httpx

from app.core.config import settings


class HubSpotClient:
    """Minimal HubSpot API client for HTTP communication only."""

    def __init__(self):
        self.base_url = settings.hubspot_base_url
        self.headers = {"Authorization": f"Bearer {settings.hubspot_access_token}"}
        self.client = httpx.AsyncClient(headers=self.headers, timeout=30.0)
        self.logger = logging.getLogger(__name__)

    async def get_contacts(self, limit: int = 10) -> dict:
        """Fetch contacts from HubSpot CRM API."""
        url = f"{self.base_url}/crm/v3/objects/contacts"
        params = {"limit": limit}
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            self.logger.info(f"Successfully fetched {len(data.get('results', []))} contacts")
            return data
        except httpx.HTTPStatusError as e:
            self.logger.error(f"HTTP error fetching contacts: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            self.logger.error(f"Error fetching contacts: {str(e)}")
            raise

    async def get_companies(self, limit: int = 10) -> dict:
        """Fetch companies from HubSpot CRM API."""
        url = f"{self.base_url}/crm/v3/objects/companies"
        params = {"limit": limit}
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            self.logger.info(f"Successfully fetched {len(data.get('results', []))} companies")
            return data
        except httpx.HTTPStatusError as e:
            self.logger.error(f"HTTP error fetching companies: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            self.logger.error(f"Error fetching companies: {str(e)}")
            raise

    async def get_deals(self, limit: int = 10) -> dict:
        """Fetch deals from HubSpot CRM API."""
        url = f"{self.base_url}/crm/v3/objects/deals"
        params = {"limit": limit}
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            self.logger.info(f"Successfully fetched {len(data.get('results', []))} deals")
            return data
        except httpx.HTTPStatusError as e:
            self.logger.error(f"HTTP error fetching deals: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            self.logger.error(f"Error fetching deals: {str(e)}")
            raise

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()