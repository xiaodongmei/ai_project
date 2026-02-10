"""订单模型"""
from decimal import Decimal
from sqlalchemy import Column, String, Integer, Numeric, DateTime, Boolean, ForeignKey, Text, Table
from app.db.base import Base, TimestampMixin, IDMixin
from datetime import datetime


# 订单-员工关联表（一个订单可以有多个员工）
order_employee = Table(
    'order_employee_association',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id'), primary_key=True),
    Column('employee_id', Integer, ForeignKey('employees.id'), primary_key=True),
)


class Order(Base, IDMixin, TimestampMixin):
    """订单模型"""
    __tablename__ = "orders"

    order_no = Column(String(100), unique=True, nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)  # 主要服务员

    # 订单类型和状态
    order_type = Column(String(50), nullable=False)  # door/appointment/online 门店消费/预约/在线
    status = Column(String(50), default="pending")  # pending/completed/cancelled/refunded

    # 金额信息
    total_amount = Column(Numeric(10, 2), nullable=False)  # 应付金额
    discount_amount = Column(Numeric(10, 2), default=Decimal("0.00"))  # 优惠金额
    actual_amount = Column(Numeric(10, 2), nullable=False)  # 实付金额
    paid_amount = Column(Numeric(10, 2), default=Decimal("0.00"))  # 已支付金额

    # 支付信息
    payment_method = Column(String(50), nullable=True)  # wechat/alipay/card/cash/account
    payment_no = Column(String(100), nullable=True)  # 支付交易号
    payment_date = Column(DateTime, nullable=True)  # 支付时间

    # 时间信息
    scheduled_time = Column(DateTime, nullable=True)  # 预约时间
    completed_time = Column(DateTime, nullable=True)  # 完成时间

    # 备注和标签
    remark = Column(Text, nullable=True)  # 订单备注
    tags = Column(String(500), nullable=True)  # JSON 格式的标签

    # 渠道来源
    channel = Column(String(50), nullable=True)  # meituan/douyin/mini_program/offline

    # 其他
    is_refunded = Column(Boolean, default=False)  # 是否已退款


class OrderItem(Base, IDMixin, TimestampMixin):
    """订单项目（订单包含的产品或服务）"""
    __tablename__ = "order_items"

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    # 数量和价格
    quantity = Column(Integer, default=1)
    unit_price = Column(Numeric(10, 2), nullable=False)  # 单价
    item_total = Column(Numeric(10, 2), nullable=False)  # 小计

    # 折扣
    discount_rate = Column(Numeric(5, 2), default=Decimal("0.00"))  # 折扣比例
    discount_amount = Column(Numeric(10, 2), default=Decimal("0.00"))  # 折扣金额

    # 产品快照
    product_name = Column(String(255))  # 产品名称快照
    product_image = Column(String(500), nullable=True)  # 产品图片快照
