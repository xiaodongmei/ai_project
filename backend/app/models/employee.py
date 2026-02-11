"""员工模型 - 通用化改造

position 字段不再限定为固定枚举，由行业模板的 staff_roles 定义可选值。
新增 skill_tags 字段，存储服务人员的技能标签。
新增 level 字段，表示员工等级（初级/中级/高级/总监）。
"""
from decimal import Decimal
from sqlalchemy import Column, String, Integer, Numeric, DateTime, Boolean, ForeignKey, Text
from app.db.base import Base, TimestampMixin, IDMixin


class Employee(Base, IDMixin, TimestampMixin):
    """员工模型"""
    __tablename__ = "employees"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    employee_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    # 角色和职位（由行业模板的 staff_roles 提供可选值）
    position = Column(String(100), nullable=False)
    # 员工等级
    level = Column(String(50), default="初级")  # 初级/中级/高级/总监
    department = Column(String(100), nullable=True)
    # 技能标签（JSON数组字符串，由行业模板的 skill_tags 提供可选值）
    skill_tags = Column(Text, nullable=True)
    # 薪资
    base_salary = Column(Numeric(10, 2), default=Decimal("0.00"))
    salary_group = Column(String(50), nullable=True)
    # 日期
    joined_date = Column(DateTime, nullable=False)
    left_date = Column(DateTime, nullable=True)
    status = Column(String(50), default="in_service")
    # 提成
    commission_rate = Column(Numeric(5, 2), default=Decimal("0.00"))
    product_commission_rate = Column(Numeric(5, 2), default=Decimal("0.00"))
    card_commission_rate = Column(Numeric(5, 2), default=Decimal("0.00"))
    total_commission = Column(Numeric(10, 2), default=Decimal("0.00"))
    total_performance = Column(Numeric(10, 2), default=Decimal("0.00"))
    customer_count = Column(Integer, default=0)
    # 个人信息
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
