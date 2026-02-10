"""API端点模块"""
from . import health, auth, customers, products, orders, employees, statistics, rooms

__all__ = ["health", "auth", "customers", "products", "orders", "employees", "statistics", "rooms"]
