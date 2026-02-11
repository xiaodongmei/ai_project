"""服务空间模型（原房间模型，通用化改造）

根据行业不同，空间含义不同：
- 养生推拿: 房间 + 床位
- 美甲美睫: 服务区 + 工位
- 美发沙龙: 区域 + 工位
- 汉服妆造: 功能区 + 工位
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from app.db.base import Base, TimestampMixin, IDMixin


class ServiceSpace(Base, IDMixin, TimestampMixin):
    """服务空间（通用化的房间/服务区/区域概念）"""
    __tablename__ = "service_spaces"

    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    space_number = Column(String(50), nullable=False, unique=True, index=True)
    space_type = Column(String(50), nullable=False)  # 由行业模板定义
    capacity = Column(Integer, nullable=False, default=1)  # 工位数量
    price_per_hour = Column(Float, nullable=False, default=0)
    floor = Column(Integer, nullable=True)
    is_available = Column(Boolean, nullable=False, default=True)
    is_vip = Column(Boolean, default=False)

    def __repr__(self):
        return f"<ServiceSpace {self.space_number} - {self.name}>"


class Station(Base, IDMixin, TimestampMixin):
    """工位（通用化的床位/美甲台/理发椅等概念）"""
    __tablename__ = "stations"

    space_id = Column(Integer, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    station_type = Column(String(50), nullable=False)  # 由行业模板定义
    status = Column(String(20), nullable=False, default="available")  # available/occupied/cleaning/maintenance
    display_order = Column(Integer, default=0)

    def __repr__(self):
        return f"<Station {self.name} - {self.status}>"


# 保留向后兼容的别名
Room = ServiceSpace
