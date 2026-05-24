import random
import string
from datetime import datetime, timedelta
from typing import Any, Optional

# Amazon-style delivery pipeline
DELIVERY_STATUSES = [
    "placed",
    "confirmed",
    "packed",
    "shipped",
    "out_for_delivery",
    "delivered",
]

STATUS_LABELS = {
    "placed": "Order Placed",
    "confirmed": "Confirmed",
    "packed": "Packed",
    "shipped": "Shipped",
    "out_for_delivery": "Out for Delivery",
    "delivered": "Delivered",
    "cancelled": "Cancelled",
}

# Minutes after payment before each stage (demo-friendly)
STAGE_DELAYS_MINUTES = {
    "confirmed": 0,
    "packed": 1,
    "shipped": 3,
    "out_for_delivery": 6,
    "delivered": 10,
}


def generate_tracking_number() -> str:
    suffix = "".join(random.choices(string.digits, k=10))
    return f"SS{suffix}IN"


def generate_payment_id() -> str:
    return "PAY" + "".join(random.choices(string.ascii_uppercase + string.digits, k=12))


def estimated_delivery_date(from_dt: Optional[datetime] = None) -> str:
    base = from_dt or datetime.utcnow()
    return (base + timedelta(days=5)).isoformat()


def delivery_progress(status: str) -> int:
    if status not in DELIVERY_STATUSES:
        return 0
    idx = DELIVERY_STATUSES.index(status)
    return int((idx / (len(DELIVERY_STATUSES) - 1)) * 100)


def target_status_after_payment(paid_at_iso: Optional[str]) -> str:
    """Advance delivery status over time after payment (demo simulation)."""
    if not paid_at_iso:
        return "placed"

    try:
        paid_at = datetime.fromisoformat(paid_at_iso)
    except ValueError:
        return "confirmed"

    elapsed_min = (datetime.utcnow() - paid_at).total_seconds() / 60
    current = "confirmed"
    for stage in ("packed", "shipped", "out_for_delivery", "delivered"):
        if elapsed_min >= STAGE_DELAYS_MINUTES[stage]:
            current = stage
    return current


def status_event_copy(status: str, location: str = "ShopSphere Fulfillment") -> tuple[str, str]:
    messages = {
        "placed": ("We received your order", location),
        "confirmed": ("Payment confirmed — preparing your items", location),
        "packed": ("Items packed and ready to ship", f"{location} — Packing"),
        "shipped": ("Package handed to courier", "Regional Hub"),
        "out_for_delivery": ("Courier is on the way", "Local Delivery Hub"),
        "delivered": ("Delivered successfully", "Your address"),
        "cancelled": ("Order cancelled", location),
    }
    title = STATUS_LABELS.get(status, status.title())
    message, loc = messages.get(status, (title, location))
    return message, loc


def build_timeline(events: list) -> list[dict[str, Any]]:
    return [
        {
            "status": e["status"],
            "title": STATUS_LABELS.get(e["status"], e["status"]),
            "message": e["message"],
            "location": e["location"],
            "event_at": e["event_at"],
            "completed": True,
        }
        for e in events
    ]
