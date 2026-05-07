from typing import Any


def _properties(obj: dict) -> dict:
    return obj.get("properties", {}) if isinstance(obj, dict) else {}


def map_contact(hubspot_obj: dict) -> dict:
    props = _properties(hubspot_obj)
    return {
        "first_name": props.get("firstname"),
        "last_name": props.get("lastname"),
        "email": props.get("email"),
        "phone": props.get("phone"),
        "hubspot_id": hubspot_obj.get("id"),
        "source": "hubspot",
    }


def map_company(hubspot_obj: dict) -> dict:
    props = _properties(hubspot_obj)
    return {
        "name": props.get("name"),
        "website": props.get("website"),
        "industry": props.get("industry"),
        "hubspot_id": hubspot_obj.get("id"),
        "source": "hubspot",
    }


def map_deal(hubspot_obj: dict) -> dict:
    props = _properties(hubspot_obj)
    pipeline_value = props.get("pipeline")
    closed_status = "closed" if props.get("closedate") else None
    status = pipeline_value or closed_status
    return {
        "title": props.get("dealname"),
        "amount": props.get("amount"),
        "stage": props.get("dealstage"),
        "status": status,
        "hubspot_id": hubspot_obj.get("id"),
        "source": "hubspot",
    }
