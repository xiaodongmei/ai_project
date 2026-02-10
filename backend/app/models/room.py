from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    capacity = Column(Integer, nullable=False, default=1)  # 房间容量
    type = Column(String(50), nullable=False)  # 房间类型：单人间、双人间等
    price_per_hour = Column(Float, nullable=False)  # 每小时价格
    is_available = Column(Boolean, nullable=False, default=True)  # 是否可用
    floor = Column(Integer, nullable=True)  # 楼层
    room_number = Column(String(50), nullable=False, unique=True, index=True)  # 房间号
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Room {self.room_number} - {self.name}>"
