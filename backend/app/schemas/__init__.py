"""Pydantic 数据验证模式"""
from app.schemas.user import UserResponse, LoginByPasswordRequest, LoginByPhoneRequest
from app.schemas.customer import CustomerResponse, CustomerCreate, CustomerUpdate
from app.schemas.product import ProductResponse, ProductCreate, ProductUpdate
from app.schemas.order import OrderResponse, OrderCreate, OrderListResponse
from app.schemas.employee import EmployeeResponse, EmployeeCreate
from app.schemas.statistics import DashboardDataResponse, ChannelStatisticsResponse

__all__ = [
    "UserResponse",
    "LoginByPasswordRequest",
    "LoginByPhoneRequest",
    "CustomerResponse",
    "CustomerCreate",
    "CustomerUpdate",
    "ProductResponse",
    "ProductCreate",
    "ProductUpdate",
    "OrderResponse",
    "OrderCreate",
    "OrderListResponse",
    "EmployeeResponse",
    "EmployeeCreate",
    "DashboardDataResponse",
    "ChannelStatisticsResponse",
]
