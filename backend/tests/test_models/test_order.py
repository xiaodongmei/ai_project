"""Order 模型测试"""
import pytest
from app.models.order import Order, OrderItem


@pytest.mark.asyncio
class TestOrderModel:
    """Order 模型测试类"""

    async def test_create_order(self, db_session, test_order):
        """测试创建订单"""
        assert test_order.id is not None
        assert test_order.status == "completed"
        assert test_order.total_amount == 500.0

    async def test_order_number_generation(self, db_session, order_factory, test_customer, test_employee):
        """测试订单号生成"""
        order = await order_factory.create(db_session, customer_id=test_customer.id, employee_id=test_employee.id)
        await db_session.flush()

        # 订单号应该是自动生成的
        assert order.order_no is not None
        assert len(order.order_no) > 0

    async def test_order_types(self, db_session, order_factory, test_customer, test_employee):
        """测试订单类型"""
        store_order = await order_factory.create(
            db_session,
            customer_id=test_customer.id,
            employee_id=test_employee.id,
            order_type="store"
        )
        appointment_order = await order_factory.create(
            db_session,
            customer_id=test_customer.id,
            employee_id=test_employee.id,
            order_type="appointment"
        )
        online_order = await order_factory.create(
            db_session,
            customer_id=test_customer.id,
            employee_id=test_employee.id,
            order_type="online"
        )
        await db_session.flush()

        assert store_order.order_type == "store"
        assert appointment_order.order_type == "appointment"
        assert online_order.order_type == "online"

    async def test_order_status_progression(self, db_session, test_order):
        """测试订单状态变更"""
        assert test_order.status == "completed"

        # 修改状态
        test_order.status = "cancelled"
        await db_session.flush()
        assert test_order.status == "cancelled"

    async def test_order_amounts(self, db_session, test_order):
        """测试订单金额"""
        assert test_order.total_amount == 500.0
        assert test_order.paid_amount == 500.0
        assert test_order.discount_amount == 0.0

    async def test_order_with_discount(self, db_session, order_factory, test_customer, test_employee):
        """测试带折扣的订单"""
        order = await order_factory.create(
            db_session,
            customer_id=test_customer.id,
            employee_id=test_employee.id,
            total_amount=1000.0,
            paid_amount=900.0,
            discount_amount=100.0
        )
        await db_session.flush()

        # 验证折扣计算
        actual_paid = order.total_amount - order.discount_amount
        assert actual_paid == order.paid_amount

    async def test_order_payment_methods(self, db_session, order_factory, test_customer, test_employee):
        """测试支付方式"""
        card_order = await order_factory.create(
            db_session,
            customer_id=test_customer.id,
            employee_id=test_employee.id,
            payment_method="card"
        )
        cash_order = await order_factory.create(
            db_session,
            customer_id=test_customer.id,
            employee_id=test_employee.id,
            payment_method="cash"
        )
        wechat_order = await order_factory.create(
            db_session,
            customer_id=test_customer.id,
            employee_id=test_employee.id,
            payment_method="wechat"
        )
        await db_session.flush()

        assert card_order.payment_method == "card"
        assert cash_order.payment_method == "cash"
        assert wechat_order.payment_method == "wechat"

    async def test_order_payment_status(self, db_session, order_factory, test_customer, test_employee):
        """测试支付状态"""
        paid_order = await order_factory.create(
            db_session,
            customer_id=test_customer.id,
            employee_id=test_employee.id,
            is_paid=True
        )
        unpaid_order = await order_factory.create(
            db_session,
            customer_id=test_customer.id,
            employee_id=test_employee.id,
            is_paid=False
        )
        await db_session.flush()

        assert paid_order.is_paid is True
        assert unpaid_order.is_paid is False

    async def test_order_customer_relationship(self, db_session, test_order, test_customer):
        """测试订单与顾客关系"""
        assert test_order.customer_id == test_customer.id

    async def test_order_employee_relationship(self, db_session, test_order, test_employee):
        """测试订单与员工关系"""
        assert test_order.employee_id == test_employee.id

    async def test_order_update(self, db_session, test_order):
        """测试更新订单"""
        test_order.status = "pending"
        test_order.discount_amount = 50.0
        test_order.paid_amount = 450.0
        await db_session.flush()

        assert test_order.status == "pending"
        assert test_order.discount_amount == 50.0
        assert test_order.paid_amount == 450.0

    async def test_order_timestamps(self, db_session, test_order):
        """测试订单时间戳"""
        await db_session.flush()
        assert test_order.created_at is not None
        assert test_order.updated_at is not None

    async def test_order_refund_amount(self, db_session, order_factory, test_customer, test_employee):
        """测试订单退款金额"""
        order = await order_factory.create(
            db_session,
            customer_id=test_customer.id,
            employee_id=test_employee.id,
            total_amount=1000.0,
            paid_amount=800.0,
            discount_amount=200.0
        )
        await db_session.flush()

        refund_amount = order.paid_amount
        assert refund_amount == 800.0


@pytest.mark.asyncio
class TestOrderItemModel:
    """OrderItem 模型测试类"""

    async def test_create_order_item(self, db_session, test_order, test_product):
        """测试创建订单项"""
        item = OrderItem(
            order_id=test_order.id,
            product_id=test_product.id,
            quantity=2,
            unit_price=88.0,
            subtotal=176.0
        )
        db_session.add(item)
        await db_session.flush()

        assert item.id is not None
        assert item.quantity == 2
        assert item.unit_price == 88.0
        assert item.subtotal == 176.0

    async def test_order_item_quantity(self, db_session, test_order, test_product):
        """测试订单项数量"""
        item = OrderItem(
            order_id=test_order.id,
            product_id=test_product.id,
            quantity=5,
            unit_price=100.0,
            subtotal=500.0
        )
        db_session.add(item)
        await db_session.flush()

        assert item.quantity == 5

    async def test_order_item_price_calculation(self, db_session, test_order, test_product):
        """测试订单项价格计算"""
        quantity = 3
        unit_price = 99.0
        expected_subtotal = quantity * unit_price

        item = OrderItem(
            order_id=test_order.id,
            product_id=test_product.id,
            quantity=quantity,
            unit_price=unit_price,
            subtotal=expected_subtotal
        )
        db_session.add(item)
        await db_session.flush()

        assert item.subtotal == expected_subtotal

    async def test_multiple_order_items(self, db_session, test_order, test_product, product_factory):
        """测试订单多个项"""
        product2 = await product_factory.create(
            db_session,
            category_id=test_product.category_id,
            name="产品2"
        )

        item1 = OrderItem(
            order_id=test_order.id,
            product_id=test_product.id,
            quantity=2,
            unit_price=88.0,
            subtotal=176.0
        )
        item2 = OrderItem(
            order_id=test_order.id,
            product_id=product2.id,
            quantity=1,
            unit_price=150.0,
            subtotal=150.0
        )
        db_session.add(item1)
        db_session.add(item2)
        await db_session.flush()

        assert item1.order_id == test_order.id
        assert item2.order_id == test_order.id
