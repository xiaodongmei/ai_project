"""产品模型"""
from sqlalchemy import Column, String, Integer, Boolean, Numeric, Text, ForeignKey
from decimal import Decimal

from app.db.base import Base, TimestampMixin, IDMixin


class ProductCategory(Base, IDMixin, TimestampMixin):
    """产品分类模型"""
    __tablename__ = "product_categories"

    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)


class Product(Base, IDMixin, TimestampMixin):
    """产品模型"""
    __tablename__ = "products"

    # 基础信息
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey("product_categories.id"), nullable=True)

    # 价格
    member_price = Column(Numeric(10, 2), nullable=False)  # 非会员价
    cost_price = Column(Numeric(10, 2), nullable=True)  # 成本价

    # 库存
    stock_quantity = Column(Integer, default=0)
    low_stock_alert = Column(Integer, default=10)  # 低库存警告阈值

    # 图片和详情
    image_url = Column(String(500), nullable=True)
    detailed_description = Column(Text, nullable=True)

    # 属性
    unit = Column(String(50), default="个")  # 单位
    weight = Column(String(100), nullable=True)  # 重量
    specification = Column(String(500), nullable=True)  # 规格

    # 状态
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)  # 是否推荐
    display_order = Column(Integer, default=0)  # 显示顺序

    # 统计
    sales_count = Column(Integer, default=0)  # 销售数量
    rating = Column(Numeric(3, 2), default=Decimal("5.00"))  # 评分
