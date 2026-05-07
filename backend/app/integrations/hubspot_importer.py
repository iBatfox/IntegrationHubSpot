from decimal import Decimal
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations.hubspot_mappers import map_contact, map_company, map_deal
from app.models.company import Company
from app.models.contact import Contact
from app.models.deal import Deal


def _normalized_value(value):
    if isinstance(value, Decimal):
        return value
    if value is None:
        return None
    try:
        return Decimal(str(value))
    except Exception:
        return value


def _fields_differ(existing, mapped: dict, compare_fields: list[str]) -> list[str]:
    diffs: list[str] = []
    for field in compare_fields:
        local = getattr(existing, field, None)
        remote = mapped.get(field)
        if isinstance(local, Decimal):
            local = _normalized_value(local)
            remote = _normalized_value(remote)
        if local != remote:
            diffs.append(field)
    return diffs


def _is_non_empty(value):
    return value is not None and value != ""


async def get_mapped_contacts(limit: int) -> dict:
    from app.integrations.hubspot import HubSpotClient

    client = HubSpotClient()
    try:
        result = await client.get_contacts(limit=limit)
        mapped = [map_contact(obj) for obj in result.get("results", [])]
        return {"results": mapped}
    finally:
        await client.close()


async def get_mapped_companies(limit: int) -> dict:
    from app.integrations.hubspot import HubSpotClient

    client = HubSpotClient()
    try:
        result = await client.get_companies(limit=limit)
        mapped = [map_company(obj) for obj in result.get("results", [])]
        return {"results": mapped}
    finally:
        await client.close()


async def get_mapped_deals(limit: int) -> dict:
    from app.integrations.hubspot import HubSpotClient

    client = HubSpotClient()
    try:
        result = await client.get_deals(limit=limit)
        mapped = [map_deal(obj) for obj in result.get("results", [])]
        return {"results": mapped}
    finally:
        await client.close()


async def dry_run_contacts(db: AsyncSession, limit: int) -> dict:
    from app.integrations.hubspot import HubSpotClient
    client = HubSpotClient()
    try:
        result = await client.get_contacts(limit=limit)
        mapped = [map_contact(obj) for obj in result.get("results", [])]
        items = await _dry_run_items(
            db,
            mapped,
            Contact,
            ["first_name", "last_name", "email", "phone", "hubspot_id", "source"],
        )
        summary = {
            "total": len(items),
            "to_create": sum(1 for item in items if item["action"] == "create"),
            "to_update": sum(1 for item in items if item["action"] == "update"),
            "to_skip": sum(1 for item in items if item["action"] == "skip"),
        }
        return {"summary": summary, "items": items}
    finally:
        await client.close()


async def dry_run_companies(db: AsyncSession, limit: int) -> dict:
    from app.integrations.hubspot import HubSpotClient
    client = HubSpotClient()
    try:
        result = await client.get_companies(limit=limit)
        mapped = [map_company(obj) for obj in result.get("results", [])]
        items = await _dry_run_items(
            db,
            mapped,
            Company,
            ["name", "website", "industry", "hubspot_id", "source"],
        )
        summary = {
            "total": len(items),
            "to_create": sum(1 for item in items if item["action"] == "create"),
            "to_update": sum(1 for item in items if item["action"] == "update"),
            "to_skip": sum(1 for item in items if item["action"] == "skip"),
        }
        return {"summary": summary, "items": items}
    finally:
        await client.close()


async def dry_run_deals(db: AsyncSession, limit: int) -> dict:
    from app.integrations.hubspot import HubSpotClient
    client = HubSpotClient()
    try:
        result = await client.get_deals(limit=limit)
        mapped = [map_deal(obj) for obj in result.get("results", [])]
        items = await _dry_run_items(
            db,
            mapped,
            Deal,
            ["title", "amount", "stage", "status", "hubspot_id", "source"],
        )
        summary = {
            "total": len(items),
            "to_create": sum(1 for item in items if item["action"] == "create"),
            "to_update": sum(1 for item in items if item["action"] == "update"),
            "to_skip": sum(1 for item in items if item["action"] == "skip"),
        }
        return {"summary": summary, "items": items}
    finally:
        await client.close()


async def import_contacts(db: AsyncSession, limit: int) -> dict:
    from app.integrations.hubspot import HubSpotClient
    client = HubSpotClient()
    try:
        result = await client.get_contacts(limit=limit)
        mapped = [map_contact(obj) for obj in result.get("results", [])]
        summary = await _import_items(
            db,
            mapped,
            Contact,
            ["first_name", "last_name"],
            ["first_name", "last_name", "email", "phone"],
        )
        summary["total"] = len(mapped)
        return {"summary": summary}
    finally:
        await client.close()


async def import_companies(db: AsyncSession, limit: int) -> dict:
    from app.integrations.hubspot import HubSpotClient
    client = HubSpotClient()
    try:
        result = await client.get_companies(limit=limit)
        mapped = [map_company(obj) for obj in result.get("results", [])]
        summary = await _import_items(
            db,
            mapped,
            Company,
            ["name"],
            ["name", "website", "industry"],
        )
        summary["total"] = len(mapped)
        return {"summary": summary}
    finally:
        await client.close()


async def _dry_run_items(
    db: AsyncSession,
    mapped_objects: list[dict],
    model,
    compare_fields: list[str],
) -> list[dict]:
    items: list[dict] = []
    for mapped in mapped_objects:
        hubspot_id = mapped.get("hubspot_id")
        mapped_fields = sorted(mapped.keys())
        if not hubspot_id:
            items.append(
                {
                    "action": "create",
                    "hubspot_id": None,
                    "reason": "missing HubSpot ID",
                    "mapped_fields": mapped_fields,
                }
            )
            continue

        statement = select(model).where(model.hubspot_id == hubspot_id)
        result = await db.execute(statement)
        existing_obj = result.scalars().first()

        if not existing_obj:
            items.append(
                {
                    "action": "create",
                    "hubspot_id": hubspot_id,
                    "reason": "no local record found",
                    "mapped_fields": mapped_fields,
                }
            )
            continue

        diffs = _fields_differ(existing_obj, mapped, compare_fields)
        if diffs:
            items.append(
                {
                    "action": "update",
                    "hubspot_id": hubspot_id,
                    "reason": f"fields differ: {', '.join(diffs)}",
                    "mapped_fields": mapped_fields,
                }
            )
        else:
            items.append(
                {
                    "action": "skip",
                    "hubspot_id": hubspot_id,
                    "reason": "record already up to date",
                    "mapped_fields": mapped_fields,
                }
            )
    return items


async def _import_items(
    db: AsyncSession,
    mapped_objects: list[dict],
    model,
    required_fields: list[str],
    update_fields: list[str],
) -> dict[str, int]:
    created = 0
    updated = 0
    skipped = 0
    errors = 0
    now = datetime.utcnow()

    for mapped in mapped_objects:
        hubspot_id = mapped.get("hubspot_id")
        if not hubspot_id:
            errors += 1
            continue

        # Check required fields
        missing_required = [f for f in required_fields if not _is_non_empty(mapped.get(f))]
        if missing_required:
            errors += 1
            continue

        # Find existing
        statement = select(model).where(model.hubspot_id == hubspot_id)
        result = await db.execute(statement)
        existing = result.scalars().first()

        if existing:
            # Update only non-empty fields
            for field in update_fields:
                mapped_value = mapped.get(field)
                if _is_non_empty(mapped_value):
                    setattr(existing, field, mapped_value)
            existing.source = "hubspot"
            existing.last_synced_at = now
            updated += 1
        else:
            # Create new
            create_data = {k: v for k, v in mapped.items() if k in update_fields + required_fields + ["hubspot_id", "source"]}
            create_data["source"] = "hubspot"
            create_data["last_synced_at"] = now
            new_obj = model(**create_data)
            db.add(new_obj)
            created += 1

    await db.commit()
    return {"created": created, "updated": updated, "skipped": skipped, "errors": errors}