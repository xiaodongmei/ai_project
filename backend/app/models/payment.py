"""支付和会员相关模型"""
from decimal import Decimal
from sqlalchemy import Column, String, Integer, Numeric, DateTime, Boolean, ForeignKey, Text
from app.db.base import Base, TimestampMixin, IDMixin
from datetime import datetime


class PaymentRecord(Base, IDMixin, TimestampMixin):
    """支付记录"""
    __tablename__ = "payment_records"

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)  # 订单ID
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)  # 顾客ID

    # 支付方式和交易号
    payment_method = Column(String(50), nullable=False)  # wechat/alipay/card/cash/account
    transaction_no = Column(String(100), unique=True, nullable=False)  # 交易号

    # 金额
    amount = Column(Numeric(10, 2), nullable=False)  # 支付金额

    # 状态
    status = Column(String(50), default="pending")  # pending/completed/failed/refunded

    # 备注
    remark = Column(Text, nullable=True)  # 支付备注


class MemberCard(Base, IDMixin, TimestampMixin):
    """会员卡"""
    __tablename__ = "member_cards"

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, unique=True)
    card_no = Column(String(100), unique=True, nullable=False, index=True)  # 卡号

    # 卡类型和余额
    card_type = Column(String(50), nullable=False)  # gold/silver/bronze
    balance = Column(Numeric(10, 2), default=Decimal("0.00"))  # 余额
    points = Column(Integer, default=0)  # 积分

    # 有效期
    valid_from = Column(DateTime, nullable=False)  # 开卡日期
    valid_until = Column(DateTime, nullable=False)  # 有效期至

    # 状态
    status = Column(String(50), default="active")  # active/inactive/frozen


class Discount(Base, IDMixin, TimestampMixin):
    """优惠券/折扣"""
    __tablename__ = "discounts"

    code = Column(String(50), unique=True, nullable=False, index=True)  # 优惠码
    name = Column(String(255), nullable=False)  # 优惠券名称
    description = Column(Text, nullable=True)  # 描述

    # 折扣类型
    discount_type = Column(String(50), nullable=False)  # percentage/fixed_amount
    discount_value = Column(Numeric(10, 2), nullable=False)  # 折扣值

    # 限制条件
    min_purchase = Column(Numeric(10, 2), default=Decimal("0.00"))  # 最低消费
    max_discount = Column(Numeric(10, 2), nullable=True)  # 最大折扣

    # 使用限制
    total_count = Column(Integer, nullable=True)  # 总数量
    used_count = Column(Integer, default=0)  # 已使用数量
    per_customer_limit = Column(Integer, default=1)  # 每个客户最多使用次数

    # 有效期
    valid_from = Column(DateTime, nullable=False)
    valid_until = Column(DateTime, nullable=False)

    # 状态
    is_active = Column(Boolean, default=True)
