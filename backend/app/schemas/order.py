"""订单 Pydantic 模式"""
from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from datetime import datetime


class OrderItemBase(BaseModel):
    """订单项目基础模式"""
    product_id: int
    quantity: int
    unit_price: Decimal


class OrderItemResponse(OrderItemBase):
    """订单项目响应"""
    id: int
    item_total: Decimal
    product_name: str
    product_image: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    """订单基础模式"""
    customer_id: int
    order_type: str
    total_amount: Decimal
    actual_amount: Decimal


class OrderCreate(OrderBase):
    """创建订单"""
    payment_method: Optional[str] = None
    items: List[OrderItemBase] = []


class OrderResponse(OrderBase):
    """订单响应模式"""
    id: int
    order_no: str
    status: str
    discount_amount: Decimal
    paid_amount: Decimal
    payment_method: Optional[str] = None
    created_at: datetime
    completed_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class OrderDetailResponse(OrderResponse):
    """订单详情响应"""
    items: List[OrderItemResponse]


class OrderListResponse(BaseModel):
    """订单列表响应"""
    id: int
    order_no: str
    customer_id: int
    status: str
    actual_amount: Decimal
    order_type: str
    payment_method: Optional[str] = None
    created_at: datetime
    completed_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class OrderStatistics(BaseModel):
    """订单统计"""
    total_orders: int
    completed_orders: int
    cancelled_orders: int
    total_revenue: Decimal
    average_order_amount: Decimal
