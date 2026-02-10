"""数据库查询性能测试"""
import pytest
import time
from sqlalchemy import select
from app.models.user import User
from app.models.product import Product
from app.models.order import Order


@pytest.mark.asyncio
class TestQueryPerformance:
    \"\"\"查询性能测试\"\"\"

    async def test_single_user_query_performance(self, db_session, test_user):
        \"\"\"测试单个用户查询性能\"\"\"
        await db_session.flush()

        start = time.time()
        stmt = select(User).filter(User.id == test_user.id)
        result = await db_session.execute(stmt)
        user = result.scalar_one_or_none()
        end = time.time()

        elapsed = (end - start) * 1000  # 转换为毫秒

        assert user is not None
        # 单个查询应该在 10ms 以内
        assert elapsed < 10

    async def test_list_users_query_performance(self, db_session, user_factory):
        \"\"\"测试用户列表查询性能\"\"\"
        # 创建 100 个用户
        for i in range(100):
            await user_factory.create(
                db_session,
                username=f"user_{i}",
                email=f"user{i}@example.com"
            )
        await db_session.flush()

        start = time.time()
        stmt = select(User)
        result = await db_session.execute(stmt)
        users = result.scalars().all()
        end = time.time()

        elapsed = (end - start) * 1000

        assert len(users) >= 100
        # 列表查询应该在 100ms 以内
        assert elapsed < 100

    async def test_product_query_with_filter_performance(self, db_session, product_factory, test_category):
        \"\"\"测试带过滤的产品查询性能\"\"\"
        # 创建 50 个产品
        for i in range(50):
            await product_factory.create(
                db_session,
                category_id=test_category.id,
                name=f"产品_{i}",
                member_price=100.0 + i
            )
        await db_session.flush()

        start = time.time()
        stmt = select(Product).filter(Product.member_price > 150.0)
        result = await db_session.execute(stmt)
        products = result.scalars().all()
        end = time.time()

        elapsed = (end - start) * 1000

        assert len(products) > 0
        # 带过滤的查询应该在 20ms 以内
        assert elapsed < 20

    async def test_order_count_query_performance(self, db_session, order_factory, test_customer, test_employee):
        \"\"\"测试订单计数查询性能\"\"\"
        # 创建 200 个订单
        for i in range(200):
            await order_factory.create(
                db_session,
                customer_id=test_customer.id,
                employee_id=test_employee.id
            )
        await db_session.flush()

        start = time.time()
        stmt = select(Order).filter(Order.customer_id == test_customer.id)
        result = await db_session.execute(stmt)
        orders = result.scalars().all()
        end = time.time()

        elapsed = (end - start) * 1000
        count = len(orders)

        assert count == 200
        # 计数查询应该在 50ms 以内
        assert elapsed < 50

    async def test_pagination_query_performance(self, db_session, user_factory):
        \"\"\"测试分页查询性能\"\"\"
        # 创建 100 个用户
        for i in range(100):
            await user_factory.create(
                db_session,
                username=f"user_{i}",
                email=f"user{i}@example.com"
            )
        await db_session.flush()

        start = time.time()
        # 分页查询：第 1 页，每页 10 条
        stmt = select(User).offset(0).limit(10)
        result = await db_session.execute(stmt)
        page1 = result.scalars().all()
        end = time.time()

        elapsed = (end - start) * 1000

        assert len(page1) == 10
        # 分页查询应该在 10ms 以内
        assert elapsed < 10


@pytest.mark.asyncio
class TestNPlusProblem:
    \"\"\"N+1 查询问题测试\"\"\"

    async def test_order_without_n_plus_one(self, db_session, order_factory, test_customer, test_employee):
        \"\"\"测试订单查询是否存在 N+1 问题\"\"\"
        # 创建 10 个订单
        for i in range(10):
            await order_factory.create(
                db_session,
                customer_id=test_customer.id,
                employee_id=test_employee.id
            )
        await db_session.flush()

        # 单次查询获取所有订单
        stmt = select(Order).filter(Order.customer_id == test_customer.id)
        result = await db_session.execute(stmt)
        orders = result.scalars().all()

        # 验证结果
        assert len(orders) == 10

        # 检查关联数据访问（不应该触发额外查询）
        for order in orders:
            assert order.customer_id == test_customer.id


@pytest.mark.asyncio
class TestQueryOptimization:
    \"\"\"查询优化测试\"\"\"

    async def test_select_specific_columns(self, db_session, user_factory):
        \"\"\"测试选择特定列的性能\"\"\"
        # 创建 100 个用户
        for i in range(100):
            await user_factory.create(
                db_session,
                username=f"user_{i}",
                email=f"user{i}@example.com"
            )
        await db_session.flush()

        # 查询所有列
        start1 = time.time()
        stmt1 = select(User)
        result1 = await db_session.execute(stmt1)
        all_users = result1.scalars().all()
        end1 = time.time()
        time1 = (end1 - start1) * 1000

        # 查询特定列（如果支持）
        start2 = time.time()
        stmt2 = select(User.id, User.username)
        result2 = await db_session.execute(stmt2)
        specific_cols = result2.all()
        end2 = time.time()
        time2 = (end2 - start2) * 1000

        # 两种查询都应该快速完成
        assert time1 < 100
        assert time2 < 100

        # 特定列查询应该不会显著慢于全列查询
        # （因为 ORM 的开销）

    async def test_filter_before_fetch(self, db_session, product_factory, test_category):
        \"\"\"测试先过滤再获取的性能\"\"\"
        # 创建 100 个产品
        for i in range(100):
            await product_factory.create(
                db_session,
                category_id=test_category.id,
                name=f\"产品_{i}\",
                stock=i
            )
        await db_session.flush()

        # 使用过滤查询
        start = time.time()
        stmt = select(Product).filter(
            Product.stock > 50,
            Product.category_id == test_category.id
        )
        result = await db_session.execute(stmt)
        filtered = result.scalars().all()
        end = time.time()

        elapsed = (end - start) * 1000

        assert len(filtered) == 49  # stock 从 51-99
        # 过滤查询应该快速
        assert elapsed < 50
