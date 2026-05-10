from datetime import datetime, timezone


def _header_value(headers: list[dict], name: str) -> str | None:
    lower_name = name.lower()
    for header in headers:
        if str(header.get("name", "")).lower() == lower_name:
            return header.get("value")
    return None


def map_linkedin_email(message: dict) -> dict:
    payload = message.get("payload", {}) if isinstance(message, dict) else {}
    headers = payload.get("headers", []) if isinstance(payload, dict) else []
    internal_date_ms = message.get("internalDate")
    received_at = None
    if internal_date_ms:
        try:
            received_at = datetime.fromtimestamp(
                int(internal_date_ms) / 1000,
                tz=timezone.utc,
            ).isoformat()
        except (TypeError, ValueError):
            received_at = None

    return {
        "sender": _header_value(headers, "From"),
        "subject": _header_value(headers, "Subject"),
        "snippet": message.get("snippet"),
        "received_at": received_at,
        "thread_id": message.get("threadId"),
        "message_id": _header_value(headers, "Message-ID") or message.get("id"),
    }
