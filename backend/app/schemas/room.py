"""服务空间 Pydantic 模式（原房间模式，通用化改造）"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class StationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    station_type: str = Field(..., min_length=1, max_length=50)
    status: str = Field(default="available")
    display_order: int = 0


class StationCreate(StationBase):
    space_id: int


class StationResponse(StationBase):
    id: int
    space_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ServiceSpaceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="空间名称")
    description: Optional[str] = Field(None, description="描述")
    space_number: str = Field(..., min_length=1, max_length=50, description="编号")
    space_type: str = Field(..., min_length=1, max_length=50, description="空间类型")
    capacity: int = Field(default=1, ge=1, description="工位容量")
    price_per_hour: float = Field(default=0, ge=0, description="每小时价格")
    floor: Optional[int] = Field(None, description="楼层")
    is_available: bool = Field(default=True, description="是否可用")
    is_vip: bool = Field(default=False, description="是否VIP")


class ServiceSpaceCreate(ServiceSpaceBase):
    pass


class ServiceSpaceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    space_type: Optional[str] = Field(None, min_length=1, max_length=50)
    capacity: Optional[int] = Field(None, ge=1)
    price_per_hour: Optional[float] = Field(None, ge=0)
    is_available: Optional[bool] = None
    is_vip: Optional[bool] = None
    floor: Optional[int] = None
    space_number: Optional[str] = Field(None, min_length=1, max_length=50)


class ServiceSpaceResponse(ServiceSpaceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# 保留向后兼容别名
RoomBase = ServiceSpaceBase
RoomCreate = ServiceSpaceCreate
RoomUpdate = ServiceSpaceUpdate
RoomResponse = ServiceSpaceResponse
