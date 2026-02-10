"""数据库 CRUD 操作测试"""
import pytest
from sqlalchemy import select
from app.models.user import User
from app.models.customer import Customer
from app.models.product import Product, ProductCategory
from app.models.order import Order, OrderItem


@pytest.mark.asyncio
class TestUserCRUD:
    \"\"\"User CRUD 操作测试\"\"\"

    async def test_create_user(self, db_session, test_user):
        \"\"\"测试创建用户\"\"\"
        await db_session.flush()

        # 查询用户
        stmt = select(User).filter(User.username == "testuser")
        result = await db_session.execute(stmt)
        user = result.scalar_one_or_none()

        assert user is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"

    async def test_read_user(self, db_session, test_user):
        \"\"\"测试读取用户\"\"\"
        await db_session.flush()

        stmt = select(User).filter(User.id == test_user.id)
        result = await db_session.execute(stmt)
        user = result.scalar_one_or_none()

        assert user is not None
        assert user.id == test_user.id
        assert user.username == test_user.username

    async def test_update_user(self, db_session, test_user):
        \"\"\"测试更新用户\"\"\"
        test_user.full_name = "Updated Name"
        test_user.phone = "13900000002"
        await db_session.flush()

        stmt = select(User).filter(User.id == test_user.id)
        result = await db_session.execute(stmt)
        user = result.scalar_one_or_none()

        assert user.full_name == "Updated Name"
        assert user.phone == "13900000002"

    async def test_delete_user(self, db_session, user_factory):
        \"\"\"测试删除用户\"\"\"
        user = await user_factory.create(
            db_session,
            username="to_delete",
            email="delete@example.com"
        )
        await db_session.flush()
        user_id = user.id

        # 删除用户
        await db_session.delete(user)
        await db_session.flush()

        # 验证用户已删除
        stmt = select(User).filter(User.id == user_id)
        result = await db_session.execute(stmt)
        deleted_user = result.scalar_one_or_none()

        assert deleted_user is None

    async def test_list_users(self, db_session, user_factory):
        \"\"\"测试列出用户\"\"\"
        user1 = await user_factory.create(
            db_session,
            username="user1",
            email="user1@example.com"
        )
        user2 = await user_factory.create(
            db_session,
            username="user2",
            email="user2@example.com"
        )
        await db_session.flush()

        stmt = select(User)
        result = await db_session.execute(stmt)
        users = result.scalars().all()

        assert len(users) >= 2
        assert any(u.username == "user1" for u in users)
        assert any(u.username == "user2" for u in users)


@pytest.mark.asyncio
class TestProductCRUD:
    \"\"\"Product CRUD 操作测试\"\"\"

    async def test_create_product(self, db_session, test_product):
        \"\"\"测试创建产品\"\"\"
        await db_session.flush()

        stmt = select(Product).filter(Product.name == "面膜")
        result = await db_session.execute(stmt)
        product = result.scalar_one_or_none()

        assert product is not None
        assert product.name == "面膜"
        assert product.member_price == 88.0

    async def test_read_product(self, db_session, test_product):
        \"\"\"测试读取产品\"\"\"
        await db_session.flush()

        stmt = select(Product).filter(Product.id == test_product.id)
        result = await db_session.execute(stmt)
        product = result.scalar_one_or_none()

        assert product is not None
        assert product.id == test_product.id
        assert product.stock == 100

    async def test_update_product(self, db_session, test_product):
        \"\"\"测试更新产品\"\"\"
        test_product.stock = 50
        test_product.member_price = 99.0
        await db_session.flush()

        stmt = select(Product).filter(Product.id == test_product.id)
        result = await db_session.execute(stmt)
        product = result.scalar_one_or_none()

        assert product.stock == 50
        assert product.member_price == 99.0

    async def test_delete_product(self, db_session, product_factory, test_category):
        \"\"\"测试删除产品\"\"\"
        product = await product_factory.create(
            db_session,
            category_id=test_category.id,
            name="to_delete"
        )
        await db_session.flush()
        product_id = product.id

        # 删除产品
        await db_session.delete(product)
        await db_session.flush()

        # 验证产品已删除
        stmt = select(Product).filter(Product.id == product_id)
        result = await db_session.execute(stmt)
        deleted_product = result.scalar_one_or_none()

        assert deleted_product is None

    async def test_list_products(self, db_session, product_factory, test_category):
        \"\"\"测试列出产品\"\"\"
        prod1 = await product_factory.create(
            db_session,
            category_id=test_category.id,
            name="产品1"
        )
        prod2 = await product_factory.create(
            db_session,
            category_id=test_category.id,
            name="产品2"
        )
        await db_session.flush()

        stmt = select(Product)
        result = await db_session.execute(stmt)
        products = result.scalars().all()

        assert len(products) >= 2


@pytest.mark.asyncio
class TestOrderCRUD:
    \"\"\"Order CRUD 操作测试\"\"\"

    async def test_create_order(self, db_session, test_order):
        \"\"\"测试创建订单\"\"\"
        await db_session.flush()

        stmt = select(Order).filter(Order.id == test_order.id)
        result = await db_session.execute(stmt)
        order = result.scalar_one_or_none()

        assert order is not None
        assert order.id == test_order.id
        assert order.total_amount == 500.0

    async def test_read_order(self, db_session, test_order):
        \"\"\"测试读取订单\"\"\"
        await db_session.flush()

        stmt = select(Order).filter(Order.id == test_order.id)
        result = await db_session.execute(stmt)
        order = result.scalar_one_or_none()

        assert order is not None
        assert order.status == "completed"

    async def test_update_order(self, db_session, test_order):
        \"\"\"测试更新订单\"\"\"
        test_order.status = "cancelled"
        test_order.discount_amount = 50.0
        await db_session.flush()

        stmt = select(Order).filter(Order.id == test_order.id)
        result = await db_session.execute(stmt)
        order = result.scalar_one_or_none()

        assert order.status == "cancelled"
        assert order.discount_amount == 50.0

    async def test_delete_order(self, db_session, order_factory, test_customer, test_employee):
        \"\"\"测试删除订单\"\"\"
        order = await order_factory.create(
            db_session,
            customer_id=test_customer.id,
            employee_id=test_employee.id
        )
        await db_session.flush()
        order_id = order.id

        # 删除订单
        await db_session.delete(order)
        await db_session.flush()

        # 验证订单已删除
        stmt = select(Order).filter(Order.id == order_id)
        result = await db_session.execute(stmt)
        deleted_order = result.scalar_one_or_none()

        assert deleted_order is None

    async def test_list_orders(self, db_session, order_factory, test_customer, test_employee):
        \"\"\"测试列出订单\"\"\"
        ord1 = await order_factory.create(
            db_session,
            customer_id=test_customer.id,
            employee_id=test_employee.id
        )
        ord2 = await order_factory.create(
            db_session,
            customer_id=test_customer.id,
            employee_id=test_employee.id
        )
        await db_session.flush()

        stmt = select(Order)
        result = await db_session.execute(stmt)
        orders = result.scalars().all()

        assert len(orders) >= 2
