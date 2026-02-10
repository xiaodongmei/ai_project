from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class RoomBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="房间名称")
    description: Optional[str] = Field(None, description="房间描述")
    capacity: int = Field(default=1, ge=1, description="房间容量")
    type: str = Field(..., min_length=1, max_length=50, description="房间类型")
    price_per_hour: float = Field(..., gt=0, description="每小时价格")
    is_available: bool = Field(default=True, description="是否可用")
    floor: Optional[int] = Field(None, description="楼层")
    room_number: str = Field(..., min_length=1, max_length=50, description="房间号")


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    capacity: Optional[int] = Field(None, ge=1)
    type: Optional[str] = Field(None, min_length=1, max_length=50)
    price_per_hour: Optional[float] = Field(None, gt=0)
    is_available: Optional[bool] = None
    floor: Optional[int] = None
    room_number: Optional[str] = Field(None, min_length=1, max_length=50)


class RoomResponse(RoomBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
