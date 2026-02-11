"""Pydantic 数据验证模式"""
from app.schemas.user import UserResponse, LoginByPasswordRequest, LoginByPhoneRequest
from app.schemas.customer import CustomerResponse, CustomerCreate, CustomerUpdate
from app.schemas.product import ProductResponse, ProductCreate, ProductUpdate
from app.schemas.order import OrderResponse, OrderCreate, OrderListResponse
from app.schemas.employee import EmployeeResponse, EmployeeCreate
from app.schemas.statistics import DashboardDataResponse, ChannelStatisticsResponse
from app.schemas.room import (
    ServiceSpaceResponse, ServiceSpaceCreate, ServiceSpaceUpdate,
    StationResponse, StationCreate,
    RoomResponse, RoomCreate, RoomUpdate,
)
from app.schemas.shop_config import (
    ShopConfigResponse, ShopConfigCreate, ShopConfigUpdate, ShopFullConfig,
)
from app.schemas.service_item import (
    ServiceItemResponse, ServiceItemCreate, ServiceItemUpdate,
    ServiceCategoryResponse, ServiceCategoryCreate,
)

__all__ = [
    "UserResponse", "LoginByPasswordRequest", "LoginByPhoneRequest",
    "CustomerResponse", "CustomerCreate", "CustomerUpdate",
    "ProductResponse", "ProductCreate", "ProductUpdate",
    "OrderResponse", "OrderCreate", "OrderListResponse",
    "EmployeeResponse", "EmployeeCreate",
    "DashboardDataResponse", "ChannelStatisticsResponse",
    "ServiceSpaceResponse", "ServiceSpaceCreate", "ServiceSpaceUpdate",
    "StationResponse", "StationCreate",
    "RoomResponse", "RoomCreate", "RoomUpdate",
    "ShopConfigResponse", "ShopConfigCreate", "ShopConfigUpdate", "ShopFullConfig",
    "ServiceItemResponse", "ServiceItemCreate", "ServiceItemUpdate",
    "ServiceCategoryResponse", "ServiceCategoryCreate",
]
