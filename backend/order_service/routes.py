from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from backend.shared.jwt_utils import get_current_user
from .database import (
    append_event_if_new,
    calculate_total,
    create_order_from_cart,
    fetch_cart_rows,
    get_db,
    get_latest_pending_order,
    get_order_events,
    init_db,
    order_to_detail,
    row_to_item,
    sync_delivery_status,
)
from .models import CartItemPayload, PayPayload, PlaceOrderPayload, RemoveCartPayload
from .delivery import build_live_tracking
from .payment import emi_breakdown, process_payment
from .tracking import STATUS_LABELS, build_timeline

router = APIRouter()
init_db()


@router.get("/")
def home():
    return {
        "service": "Order Service Running",
        "version": "3.0",
        "features": ["cart", "payments", "tracking", "delivery_pipeline"],
    }


@router.post("/add-to-cart")
@router.post("/cart/add")
def add_to_cart(item: CartItemPayload, username: str = Depends(get_current_user)):
    product_id = item.product_id or item.id
    conn = get_db()
    existing = conn.execute(
        "SELECT id, quantity FROM cart_items WHERE username = ? AND product_id = ? AND name = ?",
        (username, product_id, item.name),
    ).fetchone()

    if existing:
        conn.execute(
            "UPDATE cart_items SET quantity = quantity + ? WHERE id = ?",
            (item.quantity, existing["id"]),
        )
    else:
        conn.execute(
            """
            INSERT INTO cart_items (
                username, product_id, name, price, description, category,
                image_url, rating, reviews, discount, stock, quantity, added_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                username, product_id, item.name, item.price, item.description,
                item.category, item.image_url, item.rating, item.reviews,
                item.discount, item.stock, item.quantity, datetime.utcnow().isoformat(),
            ),
        )

    conn.commit()
    cart = fetch_cart_rows(conn, username)
    conn.close()
    return {
        "message": "Item added to cart",
        "success": True,
        "items": [row_to_item(row) for row in cart],
        "total": calculate_total(cart),
    }


@router.get("/cart")
def get_cart(username: str = Depends(get_current_user)):
    conn = get_db()
    rows = fetch_cart_rows(conn, username)
    conn.close()
    return [row_to_item(row) for row in rows]


@router.delete("/cart/{item_index}")
@router.post("/remove-from-cart")
def remove_from_cart(
    item_index: Optional[int] = None,
    payload: Optional[RemoveCartPayload] = None,
    username: str = Depends(get_current_user),
):
    index = item_index if item_index is not None else (payload.index if payload else None)
    if index is None:
        raise HTTPException(status_code=400, detail="Item index is required")

    conn = get_db()
    rows = fetch_cart_rows(conn, username)
    if index < 0 or index >= len(rows):
        conn.close()
        raise HTTPException(status_code=404, detail="Cart item not found")

    conn.execute("DELETE FROM cart_items WHERE id = ?", (rows[index]["id"],))
    conn.commit()
    updated = fetch_cart_rows(conn, username)
    conn.close()
    return {
        "message": "Item removed from cart",
        "items": [row_to_item(row) for row in updated],
        "total": calculate_total(updated),
    }


@router.post("/clear-cart")
def clear_cart(username: str = Depends(get_current_user)):
    conn = get_db()
    conn.execute("DELETE FROM cart_items WHERE username = ?", (username,))
    conn.commit()
    conn.close()
    return {"message": "Cart cleared", "success": True}


@router.post("/place-order")
def place_order(
    payload: Optional[PlaceOrderPayload] = None,
    username: str = Depends(get_current_user),
):
    conn = get_db()
    rows = fetch_cart_rows(conn, username)
    if not rows:
        conn.close()
        raise HTTPException(status_code=400, detail="Cart is empty")

    address = payload.shipping_address if payload else None
    detail = create_order_from_cart(conn, username, rows, address)
    conn.close()
    return {
        "message": "Order placed — complete payment to confirm",
        "success": True,
        **detail,
    }


@router.get("/payment/emi-options")
def emi_options(amount: float, username: str = Depends(get_current_user)):
    if amount < 3000:
        raise HTTPException(status_code=400, detail="EMI available for orders above ₹3,000")
    return {
        "amount": amount,
        "options": [
            emi_breakdown(amount, 3),
            emi_breakdown(amount, 6),
            emi_breakdown(amount, 12),
        ],
    }


@router.post("/pay")
def pay(payload: Optional[PayPayload] = None, username: str = Depends(get_current_user)):
    conn = get_db()
    method = (payload.payment_method if payload else None) or "upi"
    details = payload.model_dump(exclude_none=True) if payload else {}

    if payload and payload.order_id:
        order = conn.execute(
            "SELECT * FROM orders WHERE id = ? AND username = ?",
            (payload.order_id, username),
        ).fetchone()
    else:
        order = get_latest_pending_order(conn, username)

    if not order:
        conn.close()
        raise HTTPException(status_code=404, detail="No pending order found to pay")

    result = process_payment(conn, order, method, details)
    if not result.get("success"):
        conn.close()
        raise HTTPException(status_code=400, detail=result.get("message", "Payment failed"))

    order = conn.execute("SELECT * FROM orders WHERE id = ?", (order["id"],)).fetchone()
    detail = order_to_detail(conn, order)
    conn.commit()
    conn.close()
    return {**result, **detail}


@router.get("/orders/{order_id}/live-tracking")
def live_tracking(order_id: int, username: str = Depends(get_current_user)):
    conn = get_db()
    order = conn.execute(
        "SELECT * FROM orders WHERE id = ? AND username = ?", (order_id, username)
    ).fetchone()
    if not order:
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found")
    detail = order_to_detail(conn, order)
    conn.commit()
    conn.close()
    return build_live_tracking(detail)


@router.get("/orders")
def get_orders(username: str = Depends(get_current_user)):
    conn = get_db()
    order_rows = conn.execute(
        "SELECT * FROM orders WHERE username = ? ORDER BY id DESC", (username,)
    ).fetchall()

    result = []
    for order in order_rows:
        items = conn.execute(
            "SELECT * FROM order_items WHERE order_id = ? ORDER BY id", (order["id"],)
        ).fetchall()
        result.append([row_to_item(item) for item in items])

    conn.close()
    return result


@router.get("/orders/detail")
def get_orders_detail(username: str = Depends(get_current_user)):
    conn = get_db()
    order_rows = conn.execute(
        "SELECT * FROM orders WHERE username = ? ORDER BY id DESC", (username,)
    ).fetchall()
    result = [order_to_detail(conn, o) for o in order_rows]
    conn.commit()
    conn.close()
    return result


@router.get("/orders/overview")
def orders_overview(username: str = Depends(get_current_user)):
    """Amazon-style account overview: counts + recent orders."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM orders WHERE username = ? ORDER BY id DESC", (username,)
    ).fetchall()

    details = []
    counts = {
        "total_orders": 0,
        "pending_payment": 0,
        "active_deliveries": 0,
        "delivered": 0,
        "cancelled": 0,
    }

    for order in rows:
        detail = order_to_detail(conn, order)
        details.append(detail)
        counts["total_orders"] += 1
        if detail["payment_status"] == "pending":
            counts["pending_payment"] += 1
        elif detail["is_delivered"]:
            counts["delivered"] += 1
        elif detail["status"] == "cancelled":
            counts["cancelled"] += 1
        elif detail["payment_status"] == "paid":
            counts["active_deliveries"] += 1

    conn.commit()
    conn.close()
    return {
        "username": username,
        "summary": counts,
        "recent_orders": details[:10],
        "pipeline_stages": list(STATUS_LABELS.keys()),
    }


@router.get("/orders/{order_id}")
def get_order(order_id: int, username: str = Depends(get_current_user)):
    conn = get_db()
    order = conn.execute(
        "SELECT * FROM orders WHERE id = ? AND username = ?", (order_id, username)
    ).fetchone()
    if not order:
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found")
    detail = order_to_detail(conn, order)
    conn.commit()
    conn.close()
    return detail


@router.get("/orders/{order_id}/track")
def track_order(order_id: int, username: str = Depends(get_current_user)):
    """Full tracking timeline (Amazon-style)."""
    conn = get_db()
    order = conn.execute(
        "SELECT * FROM orders WHERE id = ? AND username = ?", (order_id, username)
    ).fetchone()
    if not order:
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found")

    sync_delivery_status(conn, order)
    order = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    events = get_order_events(conn, order_id)
    conn.commit()
    conn.close()

    return {
        "order_id": order_id,
        "tracking_number": order["tracking_number"],
        "carrier": order["carrier"],
        "status": order["status"],
        "status_label": STATUS_LABELS.get(order["status"], order["status"]),
        "payment_status": order["payment_status"],
        "estimated_delivery": order["estimated_delivery"],
        "delivered_at": order["delivered_at"],
        "timeline": build_timeline([dict(e) for e in events]),
    }


@router.post("/orders/{order_id}/cancel")
def cancel_order(order_id: int, username: str = Depends(get_current_user)):
    conn = get_db()
    order = conn.execute(
        "SELECT * FROM orders WHERE id = ? AND username = ?", (order_id, username)
    ).fetchone()
    if not order:
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found")
    if order["status"] == "delivered":
        conn.close()
        raise HTTPException(status_code=400, detail="Cannot cancel a delivered order")
    if order["status"] in ("shipped", "out_for_delivery"):
        conn.close()
        raise HTTPException(status_code=400, detail="Order already shipped — contact support")

    now = datetime.utcnow().isoformat()
    conn.execute(
        "UPDATE orders SET status = 'cancelled', payment_status = 'refunded' WHERE id = ?",
        (order_id,),
    )
    append_event_if_new(conn, order_id, "cancelled", now)
    conn.commit()
    conn.close()
    return {"message": "Order cancelled", "order_id": order_id, "status": "cancelled"}
