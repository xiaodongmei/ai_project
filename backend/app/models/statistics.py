"""统计模型"""
from decimal import Decimal
from sqlalchemy import Column, String, Integer, Numeric, DateTime, Date, ForeignKey
from app.db.base import Base, TimestampMixin, IDMixin
from datetime import date, datetime


class DailyStatistics(Base, IDMixin, TimestampMixin):
    """每日统计"""
    __tablename__ = "daily_statistics"

    stat_date = Column(Date, nullable=False, unique=True, index=True)  # 统计日期

    # 营收统计
    expected_revenue = Column(Numeric(10, 2), default=Decimal("0.00"))  # 应收
    actual_revenue = Column(Numeric(10, 2), default=Decimal("0.00"))  # 实收

    # 订单统计
    total_orders = Column(Integer, default=0)  # 订单总数
    completed_orders = Column(Integer, default=0)  # 已完成订单数
    cancelled_orders = Column(Integer, default=0)  # 已取消订单数

    # 客户统计
    new_customers = Column(Integer, default=0)  # 新增客户数
    repeat_customers = Column(Integer, default=0)  # 复购客户数

    # 客流统计
    total_visitors = Column(Integer, default=0)  # 总访问数


class ChannelStatistics(Base, IDMixin, TimestampMixin):
    """渠道统计"""
    __tablename__ = "channel_statistics"

    stat_date = Column(Date, nullable=False, index=True)  # 统计日期
    channel = Column(String(50), nullable=False, index=True)  # 渠道：meituan/douyin/mini_program/offline

    # 统计数据
    order_count = Column(Integer, default=0)  # 订单数
    revenue = Column(Numeric(10, 2), default=Decimal("0.00"))  # 收入
    customer_count = Column(Integer, default=0)  # 客户数


class EmployeePerformance(Base, IDMixin, TimestampMixin):
    """员工绩效"""
    __tablename__ = "employee_performance"

    stat_date = Column(Date, nullable=False, index=True)  # 统计日期
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)

    # 绩效数据
    performance = Column(Numeric(10, 2), default=Decimal("0.00"))  # 业绩
    commission = Column(Numeric(10, 2), default=Decimal("0.00"))  # 提成
    order_count = Column(Integer, default=0)  # 订单数
    customer_count = Column(Integer, default=0)  # 客户数

    # 排名
    rank = Column(Integer, nullable=True)  # 当天排名


class ProductSales(Base, IDMixin, TimestampMixin):
    """产品销售统计"""
    __tablename__ = "product_sales"

    stat_date = Column(Date, nullable=False, index=True)  # 统计日期
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)

    # 销售数据
    sales_quantity = Column(Integer, default=0)  # 销售数量
    sales_amount = Column(Numeric(10, 2), default=Decimal("0.00"))  # 销售额
