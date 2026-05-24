import re
from datetime import datetime
from typing import Any, Optional

from .delivery import assign_partner
from .tracking import (
    STATUS_LABELS,
    estimated_delivery_date,
    generate_payment_id,
    status_event_copy,
)

ALLOWED_METHODS = {"card", "upi", "cod", "wallet", "emi"}


def validate_upi(upi_id: Optional[str]) -> Optional[str]:
    if not upi_id or not upi_id.strip():
        return "UPI ID is required"
    pattern = r"^[a-zA-Z0-9._-]{2,}@[a-zA-Z]{2,}$"
    if not re.match(pattern, upi_id.strip()):
        return "Invalid UPI ID (e.g. name@paytm, name@ybl)"
    return None


def validate_card(
    card_number: Optional[str],
    card_name: Optional[str],
    expiry: Optional[str],
    cvv: Optional[str],
) -> Optional[str]:
    if not card_number or len(re.sub(r"\D", "", card_number)) < 13:
        return "Valid card number is required"
    if not card_name or len(card_name.strip()) < 2:
        return "Name on card is required"
    if not expiry or not re.match(r"^(0[1-9]|1[0-2])\/\d{2}$", expiry.strip()):
        return "Expiry must be MM/YY"
    if not cvv or not re.match(r"^\d{3,4}$", cvv.strip()):
        return "CVV must be 3 or 4 digits"
    return None


def validate_wallet(wallet_provider: Optional[str]) -> Optional[str]:
    allowed = {"phonepe", "paytm", "amazonpay", "googlepay"}
    if not wallet_provider or wallet_provider.lower() not in allowed:
        return "Select a wallet (PhonePe, Paytm, Amazon Pay, Google Pay)"
    return None


def validate_emi(months: Optional[int], amount: float) -> Optional[str]:
    if months not in (3, 6, 12):
        return "EMI tenure must be 3, 6, or 12 months"
    if amount < 3000:
        return "EMI available for orders above ₹3,000"
    return None


def validate_payment_details(method: str, amount: float, details: dict) -> Optional[str]:
    if method not in ALLOWED_METHODS:
        return f"Payment method '{method}' is not supported"
    if amount <= 0:
        return "Invalid order amount"
    if method == "cod" and amount > 50000:
        return "Cash on delivery is not available for orders above ₹50,000"

    if method == "upi":
        return validate_upi(details.get("upi_id"))
    if method == "card":
        return validate_card(
            details.get("card_number"),
            details.get("card_name"),
            details.get("expiry"),
            details.get("cvv"),
        )
    if method == "wallet":
        return validate_wallet(details.get("wallet_provider"))
    if method == "emi":
        return validate_emi(details.get("emi_months"), amount)
    return None


def emi_breakdown(total: float, months: int) -> dict:
    monthly = round(total / months, 2)
    return {
        "emi_months": months,
        "monthly_amount": monthly,
        "total": total,
        "interest_note": "0% demo EMI — no extra charges",
    }


def process_payment(conn, order_row, method: str = "upi", details: Optional[dict] = None) -> dict:
    details = details or {}
    order_id = order_row["id"]
    total = order_row["total"]

    error = validate_payment_details(method, total, details)
    if error:
        return {"success": False, "message": error}

    payment_status = order_row["payment_status"] if "payment_status" in order_row.keys() else "pending"
    if payment_status == "paid":
        return {
            "success": True,
            "message": "Already paid",
            "order_id": order_id,
            "payment_status": "paid",
            "status": order_row["status"],
        }

    paid_at = datetime.utcnow().isoformat()
    payment_id = generate_payment_id()
    eta = estimated_delivery_date()
    partner = assign_partner()

    emi_months = details.get("emi_months") if method == "emi" else None
    wallet_provider = details.get("wallet_provider") if method == "wallet" else None
    upi_id = details.get("upi_id") if method == "upi" else None
    card_last4 = None
    if method == "card" and details.get("card_number"):
        digits = re.sub(r"\D", "", details["card_number"])
        card_last4 = digits[-4:] if len(digits) >= 4 else "****"

    conn.execute(
        """
        UPDATE orders SET
            payment_status = 'paid',
            status = 'confirmed',
            payment_method = ?,
            payment_id = ?,
            paid_at = ?,
            estimated_delivery = ?,
            delivery_partner_name = ?,
            delivery_partner_phone = ?,
            delivery_vehicle = ?,
            emi_months = ?,
            wallet_provider = ?,
            upi_id = ?,
            card_last4 = ?
        WHERE id = ?
        """,
        (
            method,
            payment_id,
            paid_at,
            eta,
            partner["name"],
            partner["phone"],
            partner["vehicle"],
            emi_months,
            wallet_provider,
            upi_id,
            card_last4,
            order_id,
        ),
    )

    msg, loc = status_event_copy("confirmed")
    conn.execute(
        """
        INSERT INTO order_events (order_id, status, title, message, location, event_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (order_id, "confirmed", STATUS_LABELS["confirmed"], msg, loc, paid_at),
    )
    conn.commit()

    result: dict[str, Any] = {
        "success": True,
        "message": "Payment successful",
        "order_id": order_id,
        "payment_id": payment_id,
        "payment_method": method,
        "payment_status": "paid",
        "status": "confirmed",
        "status_label": STATUS_LABELS["confirmed"],
        "paid_at": paid_at,
        "estimated_delivery": eta,
        "amount_paid": total,
        "delivery_partner": partner,
    }
    if method == "emi" and emi_months:
        result["emi"] = emi_breakdown(total, int(emi_months))
    return result
