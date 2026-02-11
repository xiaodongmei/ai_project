"""服务项目 Pydantic 模式"""
from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal
from datetime import datetime


class ServiceCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    display_order: int = 0


class ServiceCategoryCreate(ServiceCategoryBase):
    pass


class ServiceCategoryResponse(ServiceCategoryBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class ServiceItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    duration_minutes: int = Field(default=60, ge=1)
    price: Decimal
    member_price: Optional[Decimal] = None
    required_station_type: Optional[str] = None


class ServiceItemCreate(ServiceItemBase):
    cost_price: Optional[Decimal] = None
    required_skill_tags: Optional[str] = None
    materials_cost: Decimal = Decimal("0.00")
    materials_description: Optional[str] = None
    image_url: Optional[str] = None


class ServiceItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    duration_minutes: Optional[int] = None
    price: Optional[Decimal] = None
    member_price: Optional[Decimal] = None
    cost_price: Optional[Decimal] = None
    required_skill_tags: Optional[str] = None
    required_station_type: Optional[str] = None
    materials_cost: Optional[Decimal] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None


class ServiceItemResponse(ServiceItemBase):
    id: int
    cost_price: Optional[Decimal] = None
    required_skill_tags: Optional[str] = None
    materials_cost: Decimal
    image_url: Optional[str] = None
    display_order: int
    is_active: bool
    is_featured: bool
    sales_count: int
    rating: Decimal
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
