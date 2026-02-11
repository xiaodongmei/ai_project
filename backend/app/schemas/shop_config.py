"""店铺配置 Pydantic 模式"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ShopConfigBase(BaseModel):
    shop_name: str = Field(default="我的店铺", max_length=200)
    industry_type: str = Field(default="general_service", max_length=50)
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    business_hours: Optional[str] = None
    logo_url: Optional[str] = None
    custom_space_label: Optional[str] = None
    custom_station_label: Optional[str] = None
    custom_provider_label: Optional[str] = None
    custom_space_types: Optional[str] = None
    custom_station_types: Optional[str] = None
    custom_staff_roles: Optional[str] = None
    custom_service_categories: Optional[str] = None
    custom_product_categories: Optional[str] = None
    custom_skill_tags: Optional[str] = None


class ShopConfigCreate(ShopConfigBase):
    pass


class ShopConfigUpdate(BaseModel):
    shop_name: Optional[str] = None
    industry_type: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    business_hours: Optional[str] = None
    logo_url: Optional[str] = None
    custom_space_label: Optional[str] = None
    custom_station_label: Optional[str] = None
    custom_provider_label: Optional[str] = None
    custom_space_types: Optional[str] = None
    custom_station_types: Optional[str] = None
    custom_staff_roles: Optional[str] = None
    custom_service_categories: Optional[str] = None
    custom_product_categories: Optional[str] = None
    custom_skill_tags: Optional[str] = None


class ShopConfigResponse(ShopConfigBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IndustryTemplateSummary(BaseModel):
    """行业模板摘要（用于前端选择列表）"""
    name: str
    icon: str
    description: str


class IndustryTemplateDetail(BaseModel):
    """行业模板详情（包含所有配置项）"""
    name: str
    icon: str
    description: str
    space_label: str
    space_label_plural: str
    station_label: str
    provider_label: str
    provider_label_plural: str
    space_types: List[str]
    station_types: List[str]
    staff_roles: List[str]
    service_categories: List[str]
    product_categories: List[str]
    skill_tags: List[str]
    default_services: list


class ShopFullConfig(BaseModel):
    """店铺完整配置（合并店铺设置 + 行业模板）"""
    shop_name: str
    industry_type: str
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    business_hours: Optional[str] = None
    logo_url: Optional[str] = None
    # 最终生效的术语（优先使用自定义，否则用模板默认值）
    space_label: str
    space_label_plural: str
    station_label: str
    provider_label: str
    provider_label_plural: str
    # 最终生效的选项列表
    space_types: List[str]
    station_types: List[str]
    staff_roles: List[str]
    service_categories: List[str]
    product_categories: List[str]
    skill_tags: List[str]
