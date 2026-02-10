"""房间管理端点 - 演示数据（含床位、技师状态）"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from datetime import datetime, timedelta
import random

router = APIRouter(prefix="/rooms", tags=["rooms"])

# 模拟房间数据（含床位和当前服务信息）
rooms_db = [
    {
        "id": 1, "room_number": "101", "name": "松风阁", "type": "VIP包间",
        "floor": 1, "capacity": 2, "price_per_hour": 198.0,
        "is_available": False, "is_vip": True, "description": "VIP豪华包间，配备独立卫浴",
        "beds": [
            {
                "id": 1, "name": "A床", "status": "occupied",
                "customer": {"name": "陈静", "is_vip": True, "phone": "138****1234"},
                "service": {"name": "艾灸理疗", "progress": 70, "start_time": "14:30", "end_time": "15:30", "duration": 60},
                "technician": {"name": "李师傅", "status": "working"},
            },
            {
                "id": 2, "name": "B床", "status": "available",
                "customer": None, "service": None, "technician": None,
            },
        ],
    },
    {
        "id": 2, "room_number": "102", "name": "竹韵轩", "type": "标准间",
        "floor": 1, "capacity": 2, "price_per_hour": 128.0,
        "is_available": False, "is_vip": False, "description": "标准双人间",
        "beds": [
            {
                "id": 3, "name": "A床", "status": "occupied",
                "customer": {"name": "张三", "is_vip": False, "phone": "159****5678"},
                "service": {"name": "足部按摩", "progress": 45, "start_time": "14:00", "end_time": "15:00", "duration": 60},
                "technician": {"name": "王师傅", "status": "working"},
            },
            {
                "id": 4, "name": "B床", "status": "occupied",
                "customer": {"name": "李四", "is_vip": True, "phone": "132****9012"},
                "service": {"name": "推拿按摩", "progress": 90, "start_time": "13:30", "end_time": "14:30", "duration": 60},
                "technician": {"name": "赵师傅", "status": "finishing"},
            },
        ],
    },
    {
        "id": 3, "room_number": "103", "name": "兰香苑", "type": "标准间",
        "floor": 1, "capacity": 2, "price_per_hour": 128.0,
        "is_available": True, "is_vip": False, "description": "标准双人间",
        "beds": [
            {"id": 5, "name": "A床", "status": "available", "customer": None, "service": None, "technician": None},
            {"id": 6, "name": "B床", "status": "available", "customer": None, "service": None, "technician": None},
        ],
    },
    {
        "id": 4, "room_number": "201", "name": "云水间", "type": "VIP包间",
        "floor": 2, "capacity": 3, "price_per_hour": 258.0,
        "is_available": False, "is_vip": True, "description": "VIP豪华大包间",
        "beds": [
            {
                "id": 7, "name": "A床", "status": "occupied",
                "customer": {"name": "赵明", "is_vip": True, "phone": "186****3456"},
                "service": {"name": "精油SPA", "progress": 30, "start_time": "15:00", "end_time": "16:30", "duration": 90},
                "technician": {"name": "张师傅", "status": "working"},
            },
            {"id": 8, "name": "B床", "status": "available", "customer": None, "service": None, "technician": None},
            {"id": 9, "name": "C床", "status": "cleaning", "customer": None, "service": None, "technician": None},
        ],
    },
    {
        "id": 5, "room_number": "202", "name": "明月堂", "type": "标准间",
        "floor": 2, "capacity": 2, "price_per_hour": 128.0,
        "is_available": True, "is_vip": False, "description": "标准双人间",
        "beds": [
            {"id": 10, "name": "A床", "status": "available", "customer": None, "service": None, "technician": None},
            {"id": 11, "name": "B床", "status": "available", "customer": None, "service": None, "technician": None},
        ],
    },
    {
        "id": 6, "room_number": "203", "name": "清风居", "type": "单人间",
        "floor": 2, "capacity": 1, "price_per_hour": 88.0,
        "is_available": False, "is_vip": False, "description": "温馨单人间",
        "beds": [
            {
                "id": 12, "name": "A床", "status": "occupied",
                "customer": {"name": "钱薇", "is_vip": False, "phone": "177****7890"},
                "service": {"name": "肩颈理疗", "progress": 60, "start_time": "14:15", "end_time": "15:15", "duration": 60},
                "technician": {"name": "杨枫", "status": "working"},
            },
        ],
    },
    {
        "id": 7, "room_number": "301", "name": "听雨阁", "type": "VIP包间",
        "floor": 3, "capacity": 2, "price_per_hour": 198.0,
        "is_available": True, "is_vip": True, "description": "VIP包间，安静舒适",
        "beds": [
            {"id": 13, "name": "A床", "status": "available", "customer": None, "service": None, "technician": None},
            {"id": 14, "name": "B床", "status": "available", "customer": None, "service": None, "technician": None},
        ],
    },
    {
        "id": 8, "room_number": "302", "name": "观澜厅", "type": "标准间",
        "floor": 3, "capacity": 2, "price_per_hour": 128.0,
        "is_available": True, "is_vip": False, "description": "标准双人间",
        "beds": [
            {"id": 15, "name": "A床", "status": "available", "customer": None, "service": None, "technician": None},
            {"id": 16, "name": "B床", "status": "cleaning", "customer": None, "service": None, "technician": None},
        ],
    },
]

# 技师列表
technicians_db = [
    {"id": 1, "name": "李师傅", "status": "working", "current_room": "101", "specialty": "艾灸理疗"},
    {"id": 2, "name": "王师傅", "status": "working", "current_room": "102", "specialty": "足部按摩"},
    {"id": 3, "name": "赵师傅", "status": "finishing", "current_room": "102", "specialty": "推拿按摩"},
    {"id": 4, "name": "张师傅", "status": "working", "current_room": "201", "specialty": "精油SPA"},
    {"id": 5, "name": "杨枫", "status": "working", "current_room": "203", "specialty": "肩颈理疗"},
    {"id": 6, "name": "惠珠秀", "status": "idle", "current_room": None, "specialty": "全身推拿"},
    {"id": 7, "name": "刘瑞", "status": "idle", "current_room": None, "specialty": "刮痧拔罐"},
    {"id": 8, "name": "贾少亮", "status": "idle", "current_room": None, "specialty": "足疗"},
]


@router.get("")
async def get_rooms(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    is_available: Optional[bool] = None,
    floor: Optional[int] = None,
    type: Optional[str] = None,
):
    """获取所有房间列表（含床位和服务状态）"""
    filtered = rooms_db[:]
    if is_available is not None:
        filtered = [r for r in filtered if r["is_available"] == is_available]
    if floor is not None:
        filtered = [r for r in filtered if r["floor"] == floor]
    if type is not None:
        filtered = [r for r in filtered if r["type"] == type]
    return {"total": len(filtered), "data": filtered[skip:skip + limit]}


@router.get("/summary")
async def get_rooms_summary():
    """获取房间总览统计"""
    total_rooms = len(rooms_db)
    available_rooms = sum(1 for r in rooms_db if r["is_available"])
    occupied_rooms = total_rooms - available_rooms
    vip_rooms = sum(1 for r in rooms_db if r["is_vip"])
    vip_available = sum(1 for r in rooms_db if r["is_vip"] and r["is_available"])

    total_beds = sum(len(r["beds"]) for r in rooms_db)
    available_beds = sum(1 for r in rooms_db for b in r["beds"] if b["status"] == "available")
    occupied_beds = sum(1 for r in rooms_db for b in r["beds"] if b["status"] == "occupied")
    cleaning_beds = sum(1 for r in rooms_db for b in r["beds"] if b["status"] == "cleaning")

    working_technicians = sum(1 for t in technicians_db if t["status"] in ("working", "finishing"))
    idle_technicians = sum(1 for t in technicians_db if t["status"] == "idle")
    finishing_soon = sum(1 for t in technicians_db if t["status"] == "finishing")

    return {
        "rooms": {"total": total_rooms, "available": available_rooms, "occupied": occupied_rooms},
        "vip": {"total": vip_rooms, "available": vip_available},
        "beds": {"total": total_beds, "available": available_beds, "occupied": occupied_beds, "cleaning": cleaning_beds},
        "technicians": {"total": len(technicians_db), "working": working_technicians, "idle": idle_technicians, "finishing_soon": finishing_soon},
    }


@router.get("/technicians")
async def get_technicians():
    """获取技师列表"""
    return {"data": technicians_db}


@router.get("/{room_id}")
async def get_room(room_id: int):
    """获取单个房间详情"""
    for r in rooms_db:
        if r["id"] == room_id:
            return r
    raise HTTPException(status_code=404, detail="房间不存在")


@router.post("")
async def create_room(data: dict):
    """创建新房间"""
    new_id = max([r["id"] for r in rooms_db], default=0) + 1
    room_number = data.get("room_number", str(new_id))
    for r in rooms_db:
        if r["room_number"] == room_number:
            raise HTTPException(status_code=400, detail="房间号已存在")

    capacity = data.get("capacity", 1)
    beds = []
    bed_labels = "ABCDEFGH"
    bed_base_id = max([b["id"] for r in rooms_db for b in r["beds"]], default=0)
    for i in range(capacity):
        beds.append({
            "id": bed_base_id + i + 1,
            "name": f"{bed_labels[i]}床",
            "status": "available",
            "customer": None, "service": None, "technician": None,
        })

    new_room = {
        "id": new_id,
        "room_number": room_number,
        "name": data.get("name", ""),
        "type": data.get("type", "标准间"),
        "floor": data.get("floor"),
        "capacity": capacity,
        "price_per_hour": data.get("price_per_hour", 128.0),
        "is_available": True,
        "is_vip": data.get("is_vip", False),
        "description": data.get("description", ""),
        "beds": beds,
    }
    rooms_db.append(new_room)
    return new_room


@router.put("/{room_id}")
async def update_room(room_id: int, data: dict):
    """更新房间信息"""
    for r in rooms_db:
        if r["id"] == room_id:
            for k, v in data.items():
                if k != "id" and k != "beds":
                    r[k] = v
            return r
    raise HTTPException(status_code=404, detail="房间不存在")


@router.delete("/{room_id}")
async def delete_room(room_id: int):
    """删除房间"""
    global rooms_db
    before = len(rooms_db)
    rooms_db = [r for r in rooms_db if r["id"] != room_id]
    if len(rooms_db) == before:
        raise HTTPException(status_code=404, detail="房间不存在")
    return {"message": "房间已删除"}


@router.post("/{room_id}/beds/{bed_id}/open")
async def open_bed(room_id: int, bed_id: int, data: dict):
    """开床 - 分配顾客和技师"""
    for room in rooms_db:
        if room["id"] == room_id:
            for bed in room["beds"]:
                if bed["id"] == bed_id:
                    if bed["status"] == "occupied":
                        raise HTTPException(status_code=400, detail="床位已被占用")
                    bed["status"] = "occupied"
                    bed["customer"] = data.get("customer", {"name": "新顾客", "is_vip": False})
                    bed["service"] = data.get("service", {"name": "待选择", "progress": 0, "start_time": datetime.now().strftime("%H:%M"), "duration": 60})
                    bed["technician"] = data.get("technician", {"name": "待分配", "status": "working"})
                    room["is_available"] = not any(b["status"] == "occupied" for b in room["beds"]) is False
                    room["is_available"] = False
                    return {"message": "开床成功", "bed": bed}
            raise HTTPException(status_code=404, detail="床位不存在")
    raise HTTPException(status_code=404, detail="房间不存在")


@router.post("/{room_id}/beds/{bed_id}/checkout")
async def checkout_bed(room_id: int, bed_id: int):
    """结账 - 释放床位"""
    for room in rooms_db:
        if room["id"] == room_id:
            for bed in room["beds"]:
                if bed["id"] == bed_id:
                    bed["status"] = "cleaning"
                    bed["customer"] = None
                    bed["service"] = None
                    bed["technician"] = None
                    # 如果所有床位都空闲则房间可用
                    if all(b["status"] in ("available", "cleaning") for b in room["beds"]):
                        room["is_available"] = True
                    return {"message": "结账成功"}
            raise HTTPException(status_code=404, detail="床位不存在")
    raise HTTPException(status_code=404, detail="房间不存在")


@router.post("/{room_id}/beds/{bed_id}/extend")
async def extend_service(room_id: int, bed_id: int, data: dict):
    """延长服务"""
    extra_minutes = data.get("minutes", 30)
    for room in rooms_db:
        if room["id"] == room_id:
            for bed in room["beds"]:
                if bed["id"] == bed_id and bed["service"]:
                    bed["service"]["duration"] += extra_minutes
                    bed["service"]["progress"] = max(0, bed["service"]["progress"] - 20)
                    return {"message": f"已延长{extra_minutes}分钟", "bed": bed}
            raise HTTPException(status_code=404, detail="床位不存在或无服务")
    raise HTTPException(status_code=404, detail="房间不存在")


@router.post("/{room_id}/beds/{bed_id}/change-technician")
async def change_technician(room_id: int, bed_id: int, data: dict):
    """换技师"""
    new_technician = data.get("technician_name", "")
    for room in rooms_db:
        if room["id"] == room_id:
            for bed in room["beds"]:
                if bed["id"] == bed_id and bed["technician"]:
                    old_name = bed["technician"]["name"]
                    bed["technician"]["name"] = new_technician
                    # 更新技师状态
                    for t in technicians_db:
                        if t["name"] == old_name:
                            t["status"] = "idle"
                            t["current_room"] = None
                        if t["name"] == new_technician:
                            t["status"] = "working"
                            t["current_room"] = room["room_number"]
                    return {"message": f"已更换技师为{new_technician}", "bed": bed}
            raise HTTPException(status_code=404, detail="床位不存在")
    raise HTTPException(status_code=404, detail="房间不存在")


@router.get("/available/list")
async def get_available_rooms():
    """获取所有可用房间"""
    return [r for r in rooms_db if r["is_available"]]
