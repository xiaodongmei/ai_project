"""Pytest 配置和公共 fixtures"""
import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.security import hash_password
from app.db.base import Base
from app.models.user import User
from app.models.customer import Customer
from app.models.product import Product, ProductCategory
from app.models.employee import Employee
from app.models.order import Order, OrderItem
from app.models.payment import PaymentRecord
from app.models.member_card import MemberCard
from app.models.discount import Discount
from app.models.statistics import DailyStatistics, ChannelStatistics
from app.models.employee_performance import EmployeePerformance
from app.models.product_sales import ProductSales


# 配置 pytest-asyncio
pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def db_engine():
    """创建测试用数据库引擎（使用内存 SQLite）"""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,  # 设置为 True 以查看 SQL
    )

    # 创建所有表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # 清理
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def db_session(db_engine) -> AsyncGenerator[AsyncSession, None]:
    """创建数据库会话"""
    async_session = sessionmaker(
        db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    async with async_session() as session:
        yield session
        await session.rollback()


# ============= 测试数据工厂 =============

class UserFactory:
    """用户工厂"""

    @staticmethod
    async def create(
        db: AsyncSession,
        username: str = "testuser",
        email: str = "test@example.com",
        password: str = "password123",
        full_name: str = "Test User",
        phone: str = "13800000001",
        role: str = "employee",
        is_active: bool = True,
        is_superuser: bool = False,
    ) -> User:
        """创建测试用户"""
        user = User(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            full_name=full_name,
            phone=phone,
            role=role,
            is_active=is_active,
            is_superuser=is_superuser,
        )
        db.add(user)
        await db.flush()
        return user


class CustomerFactory:
    """顾客工厂"""

    @staticmethod
    async def create(
        db: AsyncSession,
        name: str = "李四",
        phone: str = "13800000002",
        wechat_id: str = "lisi123",
        member_level: str = "gold",
        balance: float = 1000.0,
        points: int = 500,
        valid_cards: int = 1,
        total_consumption: float = 5000.0,
        order_count: int = 10,
    ) -> Customer:
        """创建测试顾客"""
        customer = Customer(
            name=name,
            phone=phone,
            wechat_id=wechat_id,
            member_level=member_level,
            balance=balance,
            points=points,
            valid_cards=valid_cards,
            total_consumption=total_consumption,
            order_count=order_count,
        )
        db.add(customer)
        await db.flush()
        return customer


class ProductCategoryFactory:
    """产品分类工厂"""

    @staticmethod
    async def create(
        db: AsyncSession,
        name: str = "美容护肤",
        description: str = "美容护肤产品",
        icon: str = "skincare",
        display_order: int = 1,
        is_active: bool = True,
    ) -> ProductCategory:
        """创建测试分类"""
        category = ProductCategory(
            name=name,
            description=description,
            icon=icon,
            display_order=display_order,
            is_active=is_active,
        )
        db.add(category)
        await db.flush()
        return category


class ProductFactory:
    """产品工厂"""

    @staticmethod
    async def create(
        db: AsyncSession,
        category_id: int = 1,
        name: str = "面膜",
        description: str = "补水面膜",
        member_price: float = 88.0,
        non_member_price: float = 99.0,
        cost_price: float = 30.0,
        stock: int = 100,
        low_stock_threshold: int = 10,
        image_url: str = "https://example.com/product.jpg",
        specification: str = "20ml",
        unit: str = "盒",
        sales_count: int = 50,
        rating: float = 4.8,
    ) -> Product:
        """创建测试产品"""
        product = Product(
            category_id=category_id,
            name=name,
            description=description,
            member_price=member_price,
            non_member_price=non_member_price,
            cost_price=cost_price,
            stock=stock,
            low_stock_threshold=low_stock_threshold,
            image_url=image_url,
            specification=specification,
            unit=unit,
            sales_count=sales_count,
            rating=rating,
        )
        db.add(product)
        await db.flush()
        return product


class EmployeeFactory:
    """员工工厂"""

    @staticmethod
    async def create(
        db: AsyncSession,
        user_id: int = 1,
        name: str = "张三",
        employee_id: str = "EMP001",
        position: str = "美容师",
        department: str = "美容部",
        salary: float = 5000.0,
        commission_rate: float = 0.1,
        is_active: bool = True,
    ) -> Employee:
        """创建测试员工"""
        employee = Employee(
            user_id=user_id,
            name=name,
            employee_id=employee_id,
            position=position,
            department=department,
            salary=salary,
            commission_rate=commission_rate,
            is_active=is_active,
        )
        db.add(employee)
        await db.flush()
        return employee


class OrderFactory:
    """订单工厂"""

    @staticmethod
    async def create(
        db: AsyncSession,
        customer_id: int = 1,
        employee_id: int = 1,
        order_type: str = "store",
        status: str = "completed",
        total_amount: float = 500.0,
        paid_amount: float = 500.0,
        discount_amount: float = 0.0,
        payment_method: str = "card",
        is_paid: bool = True,
    ) -> Order:
        """创建测试订单"""
        order = Order(
            customer_id=customer_id,
            employee_id=employee_id,
            order_type=order_type,
            status=status,
            total_amount=total_amount,
            paid_amount=paid_amount,
            discount_amount=discount_amount,
            payment_method=payment_method,
            is_paid=is_paid,
        )
        db.add(order)
        await db.flush()
        return order


# ============= 公共 Fixtures =============

@pytest.fixture
async def user_factory(db_session):
    """用户工厂 fixture"""
    return UserFactory


@pytest.fixture
async def customer_factory(db_session):
    """顾客工厂 fixture"""
    return CustomerFactory


@pytest.fixture
async def category_factory(db_session):
    """分类工厂 fixture"""
    return ProductCategoryFactory


@pytest.fixture
async def product_factory(db_session):
    """产品工厂 fixture"""
    return ProductFactory


@pytest.fixture
async def employee_factory(db_session):
    """员工工厂 fixture"""
    return EmployeeFactory


@pytest.fixture
async def order_factory(db_session):
    """订单工厂 fixture"""
    return OrderFactory


@pytest.fixture
async def test_user(db_session, user_factory):
    """创建一个测试用户"""
    return await user_factory.create(db_session)


@pytest.fixture
async def test_customer(db_session, customer_factory):
    """创建一个测试顾客"""
    return await customer_factory.create(db_session)


@pytest.fixture
async def test_category(db_session, category_factory):
    """创建一个测试分类"""
    return await category_factory.create(db_session)


@pytest.fixture
async def test_product(db_session, product_factory, test_category):
    """创建一个测试产品"""
    return await product_factory.create(db_session, category_id=test_category.id)


@pytest.fixture
async def test_employee(db_session, employee_factory, test_user):
    """创建一个测试员工"""
    return await employee_factory.create(db_session, user_id=test_user.id)


@pytest.fixture
async def test_order(db_session, order_factory, test_customer, test_employee):
    """创建一个测试订单"""
    return await order_factory.create(
        db_session,
        customer_id=test_customer.id,
        employee_id=test_employee.id
    )
