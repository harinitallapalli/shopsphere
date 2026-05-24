from typing import Optional

from pydantic import BaseModel, Field


class CartItemPayload(BaseModel):
    id: Optional[int] = None
    product_id: Optional[int] = None
    name: str
    price: float
    description: Optional[str] = ""
    category: Optional[str] = "Uncategorized"
    image_url: Optional[str] = ""
    rating: Optional[float] = 4.5
    reviews: Optional[int] = 100
    discount: Optional[str] = "10% OFF"
    stock: Optional[int] = 20
    quantity: int = Field(default=1, ge=1)


class RemoveCartPayload(BaseModel):
    index: int = Field(ge=0)


class PlaceOrderPayload(BaseModel):
    shipping_address: Optional[str] = None


class PayPayload(BaseModel):
    order_id: Optional[int] = None
    payment_method: str = "upi"
    upi_id: Optional[str] = None
    card_number: Optional[str] = None
    card_name: Optional[str] = None
    expiry: Optional[str] = None
    cvv: Optional[str] = None
    card_last4: Optional[str] = None
    wallet_provider: Optional[str] = None
    emi_months: Optional[int] = None
