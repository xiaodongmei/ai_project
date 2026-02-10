"""产品 Pydantic 模式"""
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime


class ProductCategoryResponse(BaseModel):
    """产品分类响应"""
    id: int
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    """产品基础模式"""
    name: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    member_price: Decimal
    non_member_price: Decimal
    cost_price: Decimal


class ProductCreate(ProductBase):
    """创建产品"""
    stock_quantity: int = 0


class ProductUpdate(BaseModel):
    """更新产品"""
    name: Optional[str] = None
    description: Optional[str] = None
    member_price: Optional[Decimal] = None
    non_member_price: Optional[Decimal] = None
    cost_price: Optional[Decimal] = None
    stock_quantity: Optional[int] = None


class ProductResponse(ProductBase):
    """产品响应模式"""
    id: int
    stock_quantity: int
    low_stock_warning: int
    image_url: Optional[str] = None
    spec: Optional[str] = None
    unit: str
    sales_count: int
    rating: Decimal
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductDetailResponse(ProductResponse):
    """产品详情响应"""
    category: Optional[ProductCategoryResponse] = None
    detailed_description: Optional[str] = None


class ProductListResponse(BaseModel):
    """产品列表响应"""
    id: int
    name: str
    member_price: Decimal
    non_member_price: Decimal
    image_url: Optional[str] = None
    stock_quantity: int
    is_featured: bool
    sales_count: int
    rating: Decimal

    class Config:
        from_attributes = True
