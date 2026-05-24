import random
from typing import Any

# Demo coordinates (Hyderabad area)
CUSTOMER_LOCATION = {"lat": 17.385, "lng": 78.4867, "label": "Your location"}
HUB_LOCATION = {"lat": 17.443, "lng": 78.391, "label": "ShopSphere Hub"}

DELIVERY_PARTNERS = [
    {"name": "Rahul Kumar", "phone": "9876543210", "vehicle": "Bike"},
    {"name": "Priya Sharma", "phone": "9123456780", "vehicle": "Scooter"},
    {"name": "Amit Verma", "phone": "9988776655", "vehicle": "Van"},
]


def assign_partner() -> dict:
    return random.choice(DELIVERY_PARTNERS)


def interpolate_position(progress_pct: float) -> dict[str, float]:
    """Move from hub toward customer based on delivery progress 0-100."""
    t = max(0.0, min(100.0, progress_pct)) / 100.0
    return {
        "lat": HUB_LOCATION["lat"] + (CUSTOMER_LOCATION["lat"] - HUB_LOCATION["lat"]) * t,
        "lng": HUB_LOCATION["lng"] + (CUSTOMER_LOCATION["lng"] - HUB_LOCATION["lng"]) * t,
    }


def build_live_tracking(order: dict) -> dict[str, Any]:
    progress = order.get("delivery_progress") or 0
    if order.get("is_delivered"):
        progress = 100
    current = interpolate_position(progress)
    partner = {
        "name": order.get("delivery_partner_name") or "Rahul Kumar",
        "phone": order.get("delivery_partner_phone") or "9876543210",
        "vehicle": order.get("delivery_vehicle") or "Bike",
    }
    return {
        "customer": CUSTOMER_LOCATION,
        "hub": HUB_LOCATION,
        "current_position": current,
        "route": [HUB_LOCATION, current, CUSTOMER_LOCATION],
        "delivery_partner": partner,
        "progress_percent": progress,
    }
