"""店铺配置模型"""
from sqlalchemy import Column, String, Text, Boolean
from app.db.base import Base, TimestampMixin, IDMixin


class ShopConfig(Base, IDMixin, TimestampMixin):
    """店铺配置 - 存储店铺基本信息和行业类型"""
    __tablename__ = "shop_configs"

    # 基本信息
    shop_name = Column(String(200), nullable=False, default="我的店铺")
    industry_type = Column(String(50), nullable=False, default="general_service")
    description = Column(Text, nullable=True)
    address = Column(String(500), nullable=True)
    phone = Column(String(20), nullable=True)
    business_hours = Column(String(100), nullable=True)
    logo_url = Column(String(500), nullable=True)

    # 行业术语自定义（覆盖模板默认值）
    custom_space_label = Column(String(50), nullable=True)
    custom_station_label = Column(String(50), nullable=True)
    custom_provider_label = Column(String(50), nullable=True)

    # 自定义配置 JSON（存储额外配置）
    custom_space_types = Column(Text, nullable=True)  # JSON string
    custom_station_types = Column(Text, nullable=True)  # JSON string
    custom_staff_roles = Column(Text, nullable=True)  # JSON string
    custom_service_categories = Column(Text, nullable=True)  # JSON string
    custom_product_categories = Column(Text, nullable=True)  # JSON string
    custom_skill_tags = Column(Text, nullable=True)  # JSON string

    is_active = Column(Boolean, default=True)
