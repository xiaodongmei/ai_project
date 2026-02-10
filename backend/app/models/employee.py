"""员工模型"""
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

    # 职位信息
    position = Column(String(100), nullable=False)  # 技师/收银员/管理员等
    department = Column(String(100), nullable=True)  # 部门

    # 薪资
    base_salary = Column(Numeric(10, 2), default=Decimal("0.00"))
    salary_group = Column(String(50), nullable=True)  # 薪资等级

    # 入职离职
    joined_date = Column(DateTime, nullable=False)
    left_date = Column(DateTime, nullable=True)
    status = Column(String(50), default="in_service")  # in_service/on_leave/left

    # 绩效
    commission_rate = Column(Numeric(5, 2), default=Decimal("0.00"))  # 提成比例
    product_commission_rate = Column(Numeric(5, 2), default=Decimal("0.00"))  # 产品提成比例
    card_commission_rate = Column(Numeric(5, 2), default=Decimal("0.00"))  # 卡提成比例

    # 统计
    total_commission = Column(Numeric(10, 2), default=Decimal("0.00"))  # 累计提成
    total_performance = Column(Numeric(10, 2), default=Decimal("0.00"))  # 累计业绩
    customer_count = Column(Integer, default=0)  # 服务客户数

    # 其他
    bio = Column(Text, nullable=True)  # 简介
    avatar_url = Column(String(500), nullable=True)  # 头像
    is_active = Column(Boolean, default=True)
