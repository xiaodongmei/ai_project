"""服务项目模型 - 独立于商品的服务管理"""
from decimal import Decimal
from sqlalchemy import Column, String, Integer, Numeric, Boolean, Text
from app.db.base import Base, TimestampMixin, IDMixin


class ServiceCategory(Base, IDMixin, TimestampMixin):
    """服务分类"""
    __tablename__ = "service_categories"

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(100), nullable=True)
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)


class ServiceItem(Base, IDMixin, TimestampMixin):
    """服务项目"""
    __tablename__ = "service_items"

    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, nullable=True)
    duration_minutes = Column(Integer, nullable=False, default=60)
    price = Column(Numeric(10, 2), nullable=False)
    member_price = Column(Numeric(10, 2), nullable=True)
    cost_price = Column(Numeric(10, 2), nullable=True)
    # 服务要求
    required_skill_tags = Column(Text, nullable=True)  # JSON: 需要的技能标签
    required_station_type = Column(String(50), nullable=True)  # 需要的工位类型
    # 耗材
    materials_cost = Column(Numeric(10, 2), default=Decimal("0.00"))
    materials_description = Column(Text, nullable=True)
    # 展示
    image_url = Column(String(500), nullable=True)
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    sales_count = Column(Integer, default=0)
    rating = Column(Numeric(3, 2), default=Decimal("5.00"))
