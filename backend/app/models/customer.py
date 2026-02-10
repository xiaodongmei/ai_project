"""顾客模型"""
from decimal import Decimal
from sqlalchemy import Column, String, Integer, Numeric, Boolean, ForeignKey, DateTime, func
from app.db.base import Base, TimestampMixin, IDMixin


class Customer(Base, IDMixin, TimestampMixin):
    """顾客模型"""
    __tablename__ = "customers"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    wechat_id = Column(String(255), unique=True, nullable=True, index=True)
    phone = Column(String(20), nullable=True, index=True)
    name = Column(String(255), nullable=False)

    # 会员相关
    member_level = Column(String(50), default="normal")  # normal/silver/gold/platinum
    is_member = Column(Boolean, default=False)
    member_since = Column(DateTime, nullable=True)

    # 资产信息
    balance = Column(Numeric(10, 2), default=Decimal("0.00"))  # 账户余额
    points = Column(Integer, default=0)  # 积分
    valid_card_count = Column(Integer, default=0)  # 有效卡数

    # 消费统计
    total_consumption = Column(Numeric(10, 2), default=Decimal("0.00"))  # 总消费金额
    total_orders = Column(Integer, default=0)  # 总订单数
    last_consumption_date = Column(DateTime, nullable=True)  # 最后消费时间

    # 标签
    tags = Column(String(500), nullable=True)  # JSON 格式的标签

    # 备注
    remark = Column(String(1000), nullable=True)

    # 状态
    is_active = Column(Boolean, default=True)
