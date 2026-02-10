"""顾客 Pydantic 模式"""
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime


class CustomerBase(BaseModel):
    """顾客基础模式"""
    name: str
    phone: Optional[str] = None
    wechat_id: Optional[str] = None
    level: str = "bronze"
    balance: Decimal = Decimal("0.00")
    points: int = 0


class CustomerCreate(CustomerBase):
    """创建顾客"""
    pass


class CustomerUpdate(BaseModel):
    """更新顾客"""
    name: Optional[str] = None
    phone: Optional[str] = None
    wechat_id: Optional[str] = None
    level: Optional[str] = None
    balance: Optional[Decimal] = None
    points: Optional[int] = None


class CustomerResponse(CustomerBase):
    """顾客响应模式"""
    id: int
    total_consumption: Decimal
    orders_count: int
    last_consumption_time: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CustomerDetailResponse(CustomerResponse):
    """顾客详情响应"""
    valid_cards: int
    membership_start_date: Optional[datetime] = None
    total_points: int
