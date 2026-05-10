import logging

import httpx
from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user
from app.core.database import get_db
from app.integrations.hubspot import HubSpotClient
from app.integrations.gmail_importer import (
    exchange_gmail_oauth_code,
    get_gmail_oauth_url,
    get_linkedin_email_preview,
)
from app.integrations.hubspot_importer import (
    dry_run_contacts,
    dry_run_companies,
    dry_run_deals,
    get_mapped_contacts,
    get_mapped_companies,
    get_mapped_deals,
    import_contacts,
    import_companies,
)
from app.models.user import User


logger = logging.getLogger(__name__)
router = APIRouter()


def _map_hubspot_error(error: httpx.HTTPStatusError) -> HTTPException:
    status_code = error.response.status_code
    if status_code == 401:
        detail = "Unauthorized: invalid HubSpot credentials"
    elif status_code == 403:
        detail = "Forbidden: HubSpot access denied"
    elif status_code == 404:
        detail = "Not found: HubSpot resource not available"
    elif status_code == 429:
        detail = "Too many requests: HubSpot rate limit exceeded"
    elif 400 <= status_code < 500:
        detail = f"HubSpot client error ({status_code})"
    else:
        detail = f"HubSpot service error ({status_code})"

    return HTTPException(status_code=status_code, detail=detail)


def _map_network_error(error: Exception) -> HTTPException:
    logger.error("HubSpot network error: %s", str(error))
    return HTTPException(
        status_code=502,
        detail="Bad Gateway: unable to reach HubSpot service",
    )


def _map_google_error(error: httpx.HTTPStatusError) -> HTTPException:
    status_code = error.response.status_code
    if status_code == 400:
        detail = "Bad Request: invalid Google OAuth request"
    elif status_code == 401:
        detail = "Unauthorized: invalid or expired Google token"
    elif status_code == 403:
        detail = "Forbidden: Google access denied"
    elif status_code == 429:
        detail = "Too many requests: Google rate limit exceeded"
    elif 400 <= status_code < 500:
        detail = f"Google client error ({status_code})"
    else:
        detail = f"Google service error ({status_code})"
    return HTTPException(status_code=status_code, detail=detail)


@router.get("/gmail/oauth/url")
async def get_gmail_oauth_connect_url(current_user: User = Depends(get_current_active_user)):
    try:
        return await get_gmail_oauth_url()
    except httpx.HTTPStatusError as e:
        raise _map_google_error(e)
    except httpx.RequestError as e:
        raise _map_network_error(e)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error("Unexpected Gmail error: %s", str(e))
        raise HTTPException(
            status_code=502,
            detail="Bad Gateway: unexpected error communicating with Gmail",
        )


@router.get("/gmail/oauth/callback")
async def gmail_oauth_callback(
    code: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await exchange_gmail_oauth_code(db=db, user_id=current_user.id, code=code)
    except httpx.HTTPStatusError as e:
        raise _map_google_error(e)
    except httpx.RequestError as e:
        raise _map_network_error(e)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Unexpected Gmail error: %s", str(e))
        raise HTTPException(
            status_code=502,
            detail="Bad Gateway: unexpected error communicating with Gmail",
        )


@router.get("/gmail/linkedin-emails/preview")
async def preview_linkedin_emails(
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    try:
        return await get_linkedin_email_preview(db=db, user_id=current_user.id, limit=limit)
    except httpx.HTTPStatusError as e:
        raise _map_google_error(e)
    except httpx.RequestError as e:
        raise _map_network_error(e)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Unexpected Gmail error: %s", str(e))
        raise HTTPException(
            status_code=502,
            detail="Bad Gateway: unexpected error communicating with Gmail",
        )


@router.get("/hubspot/contacts")
async def get_hubspot_contacts(limit: int = Query(10, ge=1, le=100)):
    """Fetch contacts preview from HubSpot API."""
    client = HubSpotClient()
    try:
        return await client.get_contacts(limit=limit)
    except httpx.HTTPStatusError as e:
        raise _map_hubspot_error(e)
    except httpx.RequestError as e:
        raise _map_network_error(e)
    except Exception as e:
        logger.error("Unexpected HubSpot error: %s", str(e))
        raise HTTPException(
            status_code=502,
            detail="Bad Gateway: unexpected error communicating with HubSpot",
        )
    finally:
        await client.close()


@router.get("/hubspot/companies")
async def get_hubspot_companies(limit: int = Query(10, ge=1, le=100)):
    """Fetch companies preview from HubSpot API."""
    client = HubSpotClient()
    try:
        return await client.get_companies(limit=limit)
    except httpx.HTTPStatusError as e:
        raise _map_hubspot_error(e)
    except httpx.RequestError as e:
        raise _map_network_error(e)
    except Exception as e:
        logger.error("Unexpected HubSpot error: %s", str(e))
        raise HTTPException(
            status_code=502,
            detail="Bad Gateway: unexpected error communicating with HubSpot",
        )
    finally:
        await client.close()


@router.get("/hubspot/deals")
async def get_hubspot_deals(limit: int = Query(10, ge=1, le=100)):
    """Fetch deals preview from HubSpot API."""
    client = HubSpotClient()
    try:
        return await client.get_deals(limit=limit)
    except httpx.HTTPStatusError as e:
        raise _map_hubspot_error(e)
    except httpx.RequestError as e:
        raise _map_network_error(e)
    except Exception as e:
        logger.error("Unexpected HubSpot error: %s", str(e))
        raise HTTPException(
            status_code=502,
            detail="Bad Gateway: unexpected error communicating with HubSpot",
        )
    finally:
        await client.close()


@router.get("/hubspot/contacts/mapped")
async def get_hubspot_contacts_mapped(limit: int = Query(5, ge=1, le=100)):
    """Fetch mapped contacts preview from HubSpot API."""
    try:
        return await get_mapped_contacts(limit)
    except httpx.HTTPStatusError as e:
        raise _map_hubspot_error(e)
    except httpx.RequestError as e:
        raise _map_network_error(e)
    except Exception as e:
        logger.error("Unexpected HubSpot error: %s", str(e))
        raise HTTPException(
            status_code=502,
            detail="Bad Gateway: unexpected error communicating with HubSpot",
        )


@router.get("/hubspot/companies/mapped")
async def get_hubspot_companies_mapped(limit: int = Query(5, ge=1, le=100)):
    """Fetch mapped companies preview from HubSpot API."""
    try:
        return await get_mapped_companies(limit)
    except httpx.HTTPStatusError as e:
        raise _map_hubspot_error(e)
    except httpx.RequestError as e:
        raise _map_network_error(e)
    except Exception as e:
        logger.error("Unexpected HubSpot error: %s", str(e))
        raise HTTPException(
            status_code=502,
            detail="Bad Gateway: unexpected error communicating with HubSpot",
        )


@router.get("/hubspot/deals/mapped")
async def get_hubspot_deals_mapped(limit: int = Query(5, ge=1, le=100)):
    """Fetch mapped deals preview from HubSpot API."""
    try:
        return await get_mapped_deals(limit)
    except httpx.HTTPStatusError as e:
        raise _map_hubspot_error(e)
    except httpx.RequestError as e:
        raise _map_network_error(e)
    except Exception as e:
        logger.error("Unexpected HubSpot error: %s", str(e))
        raise HTTPException(
            status_code=502,
            detail="Bad Gateway: unexpected error communicating with HubSpot",
        )


@router.get("/hubspot/contacts/dry-run")
async def get_hubspot_contacts_dry_run(
    limit: int = Query(5, ge=1, le=100), db: AsyncSession = Depends(get_db)
):
    """Show dry-run preview of local contact sync from HubSpot."""
    try:
        return await dry_run_contacts(db, limit)
    except httpx.HTTPStatusError as e:
        raise _map_hubspot_error(e)
    except httpx.RequestError as e:
        raise _map_network_error(e)
    except Exception as e:
        logger.error("Unexpected HubSpot error: %s", str(e))
        raise HTTPException(
            status_code=502,
            detail="Bad Gateway: unexpected error communicating with HubSpot",
        )


@router.get("/hubspot/companies/dry-run")
async def get_hubspot_companies_dry_run(
    limit: int = Query(5, ge=1, le=100), db: AsyncSession = Depends(get_db)
):
    """Show dry-run preview of local company sync from HubSpot."""
    try:
        return await dry_run_companies(db, limit)
    except httpx.HTTPStatusError as e:
        raise _map_hubspot_error(e)
    except httpx.RequestError as e:
        raise _map_network_error(e)
    except Exception as e:
        logger.error("Unexpected HubSpot error: %s", str(e))
        raise HTTPException(
            status_code=502,
            detail="Bad Gateway: unexpected error communicating with HubSpot",
        )


@router.get("/hubspot/deals/dry-run")
async def get_hubspot_deals_dry_run(
    limit: int = Query(5, ge=1, le=100), db: AsyncSession = Depends(get_db)
):
    """Show dry-run preview of local deal sync from HubSpot."""
    try:
        return await dry_run_deals(db, limit)
    except httpx.HTTPStatusError as e:
        raise _map_hubspot_error(e)
    except httpx.RequestError as e:
        raise _map_network_error(e)
    except Exception as e:
        logger.error("Unexpected HubSpot error: %s", str(e))
        raise HTTPException(
            status_code=502,
            detail="Bad Gateway: unexpected error communicating with HubSpot",
        )


@router.post("/hubspot/contacts/import")
async def import_hubspot_contacts(
    limit: int = Query(5, ge=1, le=100), db: AsyncSession = Depends(get_db)
):
    """Import contacts from HubSpot into local CRM."""
    try:
        return await import_contacts(db, limit)
    except httpx.HTTPStatusError as e:
        raise _map_hubspot_error(e)
    except httpx.RequestError as e:
        raise _map_network_error(e)
    except Exception as e:
        logger.error("Unexpected HubSpot error: %s", str(e))
        raise HTTPException(
            status_code=502,
            detail="Bad Gateway: unexpected error communicating with HubSpot",
        )


@router.post("/hubspot/companies/import")
async def import_hubspot_companies(
    limit: int = Query(5, ge=1, le=100), db: AsyncSession = Depends(get_db)
):
    """Import companies from HubSpot into local CRM."""
    try:
        return await import_companies(db, limit)
    except httpx.HTTPStatusError as e:
        raise _map_hubspot_error(e)
    except httpx.RequestError as e:
        raise _map_network_error(e)
    except Exception as e:
        logger.error("Unexpected HubSpot error: %s", str(e))
        raise HTTPException(
            status_code=502,
            detail="Bad Gateway: unexpected error communicating with HubSpot",
        )