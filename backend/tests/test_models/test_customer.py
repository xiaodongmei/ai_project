"""Customer 模型测试"""
import pytest
from app.models.customer import Customer


@pytest.mark.asyncio
class TestCustomerModel:
    """Customer 模型测试类"""

    async def test_create_customer(self, db_session, test_customer):
        """测试创建顾客"""
        assert test_customer.id is not None
        assert test_customer.name == "李四"
        assert test_customer.phone == "13800000002"
        assert test_customer.wechat_id == "lisi123"

    async def test_customer_member_level(self, db_session, customer_factory):
        """测试会员等级"""
        bronze = await customer_factory.create(db_session, member_level="bronze")
        silver = await customer_factory.create(
            db_session,
            name="王五",
            phone="13800000003",
            member_level="silver"
        )
        gold = await customer_factory.create(
            db_session,
            name="赵六",
            phone="13800000004",
            member_level="gold"
        )
        platinum = await customer_factory.create(
            db_session,
            name="孙七",
            phone="13800000005",
            member_level="platinum"
        )

        await db_session.flush()

        assert bronze.member_level == "bronze"
        assert silver.member_level == "silver"
        assert gold.member_level == "gold"
        assert platinum.member_level == "platinum"

    async def test_customer_balance(self, db_session, customer_factory):
        """测试顾客余额"""
        customer = await customer_factory.create(db_session, balance=1000.0)
        await db_session.flush()

        assert customer.balance == 1000.0

        # 测试余额修改
        customer.balance = 500.0
        await db_session.flush()
        assert customer.balance == 500.0

    async def test_customer_points(self, db_session, customer_factory):
        """测试积分"""
        customer = await customer_factory.create(db_session, points=1000)
        await db_session.flush()

        assert customer.points == 1000

        # 测试积分修改
        customer.points = 1500
        await db_session.flush()
        assert customer.points == 1500

    async def test_customer_statistics(self, db_session, customer_factory):
        """测试顾客统计信息"""
        customer = await customer_factory.create(
            db_session,
            total_consumption=5000.0,
            order_count=10,
            valid_cards=2
        )
        await db_session.flush()

        assert customer.total_consumption == 5000.0
        assert customer.order_count == 10
        assert customer.valid_cards == 2

    async def test_duplicate_phone(self, db_session, customer_factory):
        """测试重复手机号"""
        customer1 = await customer_factory.create(db_session, phone="13800000020")
        customer2 = Customer(
            name="新顾客",
            phone="13800000020",
            wechat_id="newcust"
        )
        db_session.add(customer2)

        with pytest.raises(Exception):
            await db_session.flush()

    async def test_customer_active_status(self, db_session, customer_factory):
        """测试顾客活跃状态"""
        active = await customer_factory.create(db_session)
        await db_session.flush()

        # 默认应该是活跃的
        assert active.is_active is True

    async def test_customer_update(self, db_session, test_customer):
        """测试更新顾客"""
        test_customer.name = "新名字"
        test_customer.balance = 2000.0
        test_customer.points = 800
        await db_session.flush()

        assert test_customer.name == "新名字"
        assert test_customer.balance == 2000.0
        assert test_customer.points == 800

    async def test_customer_membership_duration(self, db_session, customer_factory):
        """测试会员时长"""
        customer = await customer_factory.create(db_session)
        await db_session.flush()

        assert customer.membership_start_date is not None

    async def test_customer_consumption_tracking(self, db_session, customer_factory):
        """测试消费跟踪"""
        customer = await customer_factory.create(
            db_session,
            total_consumption=10000.0,
            order_count=20
        )
        await db_session.flush()

        # 计算平均消费
        avg_consumption = customer.total_consumption / customer.order_count if customer.order_count > 0 else 0
        assert avg_consumption == 500.0
