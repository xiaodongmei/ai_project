"""API 路由配置"""
from fastapi import APIRouter

from app.api.v1.endpoints import health, auth, customers, products, orders, employees, statistics, rooms

api_router = APIRouter(prefix="/api/v1")

# 包含路由
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, tags=["Auth"])
api_router.include_router(customers.router, tags=["Customers"])
api_router.include_router(products.router, tags=["Products"])
api_router.include_router(orders.router, tags=["Orders"])
api_router.include_router(employees.router, tags=["Employees"])
api_router.include_router(statistics.router, tags=["Statistics"])
api_router.include_router(rooms.router, tags=["Rooms"])
