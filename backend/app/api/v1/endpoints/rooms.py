"""服务空间管理端点 - 通用化改造

根据行业模板动态生成mock数据：
- 空间名称、类型根据行业模板调整
- 服务项目名称从当前行业模板的 default_services 获取
- 服务人员名称与行业角色匹配
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from datetime import datetime
from app.api.v1.endpoints.config import _shop_config, _merge_config
from app.core.industry_templates import get_template

router = APIRouter(prefix="/rooms", tags=["服务空间管理"])


def _get_industry_data():
    """获取当前行业模板的完整数据"""
    cfg = _merge_config(_shop_config)
    industry_type = cfg.get("industry_type", "general_service")
    template = get_template(industry_type)
    return cfg, template


def _build_providers():
    """根据当前行业模板构建服务人员列表"""
    cfg, template = _get_industry_data()
    services = template.get("default_services", [])
    provider_label = cfg.get("provider_label", "服务师")

    # 通用姓名池 - 每个行业都适用
    names = ["李强", "王月", "赵敏", "张峰", "杨枫", "惠珠秀", "刘瑞", "贾少亮"]
    svc_names = [s["name"] for s in services]
    while len(svc_names) < len(names):
        svc_names = svc_names + svc_names

    providers = []
    for i, name in enumerate(names):
        providers.append({
            "id": i + 1,
            "name": name,
            "status": "working" if i < 5 else "idle",
            "current_room": str(100 + i + 1) if i < 5 else None,
            "specialty": svc_names[i % len(svc_names)],
        })
    return providers


def _build_spaces():
    """根据当前行业模板构建空间mock数据"""
    cfg, template = _get_industry_data()
    services = template.get("default_services", [])
    space_types = cfg.get("space_types", ["标准区"])
    station_types = cfg.get("station_types", ["标准工位"])

    svc_names = [s["name"] for s in services]
    while len(svc_names) < 8:
        svc_names = svc_names + svc_names

    providers = _build_providers()
    provider_names = [p["name"] for p in providers]

    # 根据行业模板决定空间命名风格
    industry = cfg.get("industry_type", "general_service")
    if industry == "wellness_spa":
        space_names = ["松风阁", "竹韵轩", "兰香苑", "云水间", "明月堂", "清风居", "听雨阁", "观澜厅"]
    elif industry == "hair_salon":
        space_names = ["A区", "B区", "C区", "VIP-1", "VIP-2", "洗护区", "烫染区", "造型区"]
    elif industry == "nail_salon":
        space_names = ["美甲区A", "美甲区B", "美睫区A", "VIP室", "护理区A", "护理区B", "美甲区C", "美睫区B"]
    elif industry == "hanfu_studio":
        space_names = ["化妆间1", "化妆间2", "换装区A", "VIP化妆间", "拍摄区A", "拍摄区B", "盘发区", "等候区"]
    else:
        space_names = ["区域1", "区域2", "区域3", "VIP区", "区域4", "区域5", "区域6", "区域7"]

    station_label = cfg.get("station_label", "工位")

    return [
        {
            "id": 1, "room_number": "101", "name": space_names[0],
            "type": space_types[0] if space_types else "VIP",
            "floor": 1, "capacity": 2, "price_per_hour": 198.0,
            "is_available": False, "is_vip": True, "description": f"VIP{cfg.get('space_label', '空间')}",
            "beds": [
                {
                    "id": 1, "name": f"A{station_label}", "status": "occupied",
                    "customer": {"name": "陈静", "is_vip": True, "phone": "138****1234"},
                    "service": {"name": svc_names[0], "progress": 70, "start_time": "14:30", "end_time": "15:30", "duration": 60},
                    "technician": {"name": provider_names[0], "status": "working"},
                },
                {
                    "id": 2, "name": f"B{station_label}", "status": "available",
                    "customer": None, "service": None, "technician": None,
                },
            ],
        },
        {
            "id": 2, "room_number": "102", "name": space_names[1],
            "type": space_types[1] if len(space_types) > 1 else "标准",
            "floor": 1, "capacity": 2, "price_per_hour": 128.0,
            "is_available": False, "is_vip": False, "description": f"标准{cfg.get('space_label', '空间')}",
            "beds": [
                {
                    "id": 3, "name": f"A{station_label}", "status": "occupied",
                    "customer": {"name": "张三", "is_vip": False, "phone": "159****5678"},
                    "service": {"name": svc_names[1], "progress": 45, "start_time": "14:00", "end_time": "15:00", "duration": 60},
                    "technician": {"name": provider_names[1], "status": "working"},
                },
                {
                    "id": 4, "name": f"B{station_label}", "status": "occupied",
                    "customer": {"name": "李四", "is_vip": True, "phone": "132****9012"},
                    "service": {"name": svc_names[2], "progress": 90, "start_time": "13:30", "end_time": "14:30", "duration": 60},
                    "technician": {"name": provider_names[2], "status": "finishing"},
                },
            ],
        },
        {
            "id": 3, "room_number": "103", "name": space_names[2],
            "type": space_types[1] if len(space_types) > 1 else "标准",
            "floor": 1, "capacity": 2, "price_per_hour": 128.0,
            "is_available": True, "is_vip": False, "description": f"标准{cfg.get('space_label', '空间')}",
            "beds": [
                {"id": 5, "name": f"A{station_label}", "status": "available", "customer": None, "service": None, "technician": None},
                {"id": 6, "name": f"B{station_label}", "status": "available", "customer": None, "service": None, "technician": None},
            ],
        },
        {
            "id": 4, "room_number": "201", "name": space_names[3],
            "type": space_types[0] if space_types else "VIP",
            "floor": 2, "capacity": 3, "price_per_hour": 258.0,
            "is_available": False, "is_vip": True, "description": f"VIP大{cfg.get('space_label', '空间')}",
            "beds": [
                {
                    "id": 7, "name": f"A{station_label}", "status": "occupied",
                    "customer": {"name": "赵明", "is_vip": True, "phone": "186****3456"},
                    "service": {"name": svc_names[3], "progress": 30, "start_time": "15:00", "end_time": "16:30", "duration": 90},
                    "technician": {"name": provider_names[3], "status": "working"},
                },
                {"id": 8, "name": f"B{station_label}", "status": "available", "customer": None, "service": None, "technician": None},
                {"id": 9, "name": f"C{station_label}", "status": "cleaning", "customer": None, "service": None, "technician": None},
            ],
        },
        {
            "id": 5, "room_number": "202", "name": space_names[4],
            "type": space_types[1] if len(space_types) > 1 else "标准",
            "floor": 2, "capacity": 2, "price_per_hour": 128.0,
            "is_available": True, "is_vip": False, "description": f"标准{cfg.get('space_label', '空间')}",
            "beds": [
                {"id": 10, "name": f"A{station_label}", "status": "available", "customer": None, "service": None, "technician": None},
                {"id": 11, "name": f"B{station_label}", "status": "available", "customer": None, "service": None, "technician": None},
            ],
        },
        {
            "id": 6, "room_number": "203", "name": space_names[5],
            "type": space_types[2] if len(space_types) > 2 else "单人",
            "floor": 2, "capacity": 1, "price_per_hour": 88.0,
            "is_available": False, "is_vip": False, "description": f"温馨{cfg.get('space_label', '空间')}",
            "beds": [
                {
                    "id": 12, "name": f"A{station_label}", "status": "occupied",
                    "customer": {"name": "钱薇", "is_vip": False, "phone": "177****7890"},
                    "service": {"name": svc_names[4], "progress": 60, "start_time": "14:15", "end_time": "15:15", "duration": 60},
                    "technician": {"name": provider_names[4], "status": "working"},
                },
            ],
        },
        {
            "id": 7, "room_number": "301", "name": space_names[6],
            "type": space_types[0] if space_types else "VIP",
            "floor": 3, "capacity": 2, "price_per_hour": 198.0,
            "is_available": True, "is_vip": True, "description": f"VIP{cfg.get('space_label', '空间')}",
            "beds": [
                {"id": 13, "name": f"A{station_label}", "status": "available", "customer": None, "service": None, "technician": None},
                {"id": 14, "name": f"B{station_label}", "status": "available", "customer": None, "service": None, "technician": None},
            ],
        },
        {
            "id": 8, "room_number": "302", "name": space_names[7],
            "type": space_types[1] if len(space_types) > 1 else "标准",
            "floor": 3, "capacity": 2, "price_per_hour": 128.0,
            "is_available": True, "is_vip": False, "description": f"标准{cfg.get('space_label', '空间')}",
            "beds": [
                {"id": 15, "name": f"A{station_label}", "status": "available", "customer": None, "service": None, "technician": None},
                {"id": 16, "name": f"B{station_label}", "status": "cleaning", "customer": None, "service": None, "technician": None},
            ],
        },
    ]


# 初始化 — 延迟构建，每次请求使用最新配置
def _get_spaces():
    return _build_spaces()


def _get_providers():
    return _build_providers()


@router.get("")
async def get_spaces(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    is_available: Optional[bool] = None,
    floor: Optional[int] = None,
    type: Optional[str] = None,
):
    """获取服务空间列表"""
    spaces = _get_spaces()
    filtered = spaces[:]
    if is_available is not None:
        filtered = [r for r in filtered if r["is_available"] == is_available]
    if floor is not None:
        filtered = [r for r in filtered if r["floor"] == floor]
    if type is not None:
        filtered = [r for r in filtered if r["type"] == type]
    return {"total": len(filtered), "data": filtered[skip:skip + limit]}


@router.get("/summary")
async def get_spaces_summary():
    """获取空间总览统计"""
    spaces = _get_spaces()
    providers = _get_providers()

    total = len(spaces)
    available = sum(1 for r in spaces if r["is_available"])
    occupied = total - available
    vip_total = sum(1 for r in spaces if r["is_vip"])
    vip_avail = sum(1 for r in spaces if r["is_vip"] and r["is_available"])

    all_stations = [b for r in spaces for b in r["beds"]]
    total_stations = len(all_stations)
    avail_stations = sum(1 for b in all_stations if b["status"] == "available")
    occupied_stations = sum(1 for b in all_stations if b["status"] == "occupied")
    cleaning_stations = sum(1 for b in all_stations if b["status"] == "cleaning")

    working = sum(1 for t in providers if t["status"] in ("working", "finishing"))
    idle = sum(1 for t in providers if t["status"] == "idle")
    finishing = sum(1 for t in providers if t["status"] == "finishing")

    return {
        "rooms": {"total": total, "available": available, "occupied": occupied},
        "vip": {"total": vip_total, "available": vip_avail},
        "beds": {"total": total_stations, "available": avail_stations, "occupied": occupied_stations, "cleaning": cleaning_stations},
        "technicians": {"total": len(providers), "working": working, "idle": idle, "finishing_soon": finishing},
    }


@router.get("/technicians")
async def get_providers_list():
    """获取服务人员列表"""
    return {"data": _get_providers()}


@router.get("/available/list")
async def get_available_spaces():
    """获取所有可用空间"""
    return [r for r in _get_spaces() if r["is_available"]]


@router.get("/{space_id}")
async def get_space(space_id: int):
    """获取单个空间详情"""
    for r in _get_spaces():
        if r["id"] == space_id:
            return r
    raise HTTPException(status_code=404, detail="空间不存在")


@router.post("")
async def create_space(data: dict):
    """创建新空间"""
    spaces = _get_spaces()
    new_id = max([r["id"] for r in spaces], default=0) + 1
    space_number = data.get("room_number", data.get("space_number", str(new_id)))
    for r in spaces:
        if r["room_number"] == space_number:
            raise HTTPException(status_code=400, detail="编号已存在")

    cfg, _ = _get_industry_data()
    station_label = cfg.get("station_label", "工位")
    capacity = data.get("capacity", 1)
    stations = []
    labels = "ABCDEFGH"
    base_id = max([b["id"] for r in spaces for b in r["beds"]], default=0)
    for i in range(capacity):
        stations.append({
            "id": base_id + i + 1,
            "name": f"{labels[i]}{station_label}",
            "status": "available",
            "customer": None, "service": None, "technician": None,
        })

    new_space = {
        "id": new_id,
        "room_number": space_number,
        "name": data.get("name", ""),
        "type": data.get("type", "标准"),
        "floor": data.get("floor"),
        "capacity": capacity,
        "price_per_hour": data.get("price_per_hour", 0),
        "is_available": True,
        "is_vip": data.get("is_vip", False),
        "description": data.get("description", ""),
        "beds": stations,
    }
    return new_space


@router.put("/{space_id}")
async def update_space(space_id: int, data: dict):
    """更新空间信息"""
    for r in _get_spaces():
        if r["id"] == space_id:
            for k, v in data.items():
                if k not in ("id", "beds"):
                    r[k] = v
            return r
    raise HTTPException(status_code=404, detail="空间不存在")


@router.delete("/{space_id}")
async def delete_space(space_id: int):
    """删除空间"""
    return {"message": "已删除"}


@router.post("/{space_id}/beds/{station_id}/open")
async def open_station(space_id: int, station_id: int, data: dict):
    """开始服务 - 分配顾客和服务人员"""
    for space in _get_spaces():
        if space["id"] == space_id:
            for station in space["beds"]:
                if station["id"] == station_id:
                    if station["status"] == "occupied":
                        raise HTTPException(status_code=400, detail="工位已被占用")
                    station["status"] = "occupied"
                    station["customer"] = data.get("customer", {"name": "新顾客", "is_vip": False})
                    station["service"] = data.get("service", {
                        "name": "待选择", "progress": 0,
                        "start_time": datetime.now().strftime("%H:%M"), "duration": 60,
                    })
                    station["technician"] = data.get("technician", {"name": "待分配", "status": "working"})
                    space["is_available"] = False
                    return {"message": "开始服务", "bed": station}
            raise HTTPException(status_code=404, detail="工位不存在")
    raise HTTPException(status_code=404, detail="空间不存在")


@router.post("/{space_id}/beds/{station_id}/checkout")
async def checkout_station(space_id: int, station_id: int):
    """结账 - 释放工位"""
    for space in _get_spaces():
        if space["id"] == space_id:
            for station in space["beds"]:
                if station["id"] == station_id:
                    station["status"] = "cleaning"
                    station["customer"] = None
                    station["service"] = None
                    station["technician"] = None
                    if all(b["status"] in ("available", "cleaning") for b in space["beds"]):
                        space["is_available"] = True
                    return {"message": "结账成功"}
            raise HTTPException(status_code=404, detail="工位不存在")
    raise HTTPException(status_code=404, detail="空间不存在")


@router.post("/{space_id}/beds/{station_id}/extend")
async def extend_service(space_id: int, station_id: int, data: dict):
    """延长服务"""
    extra = data.get("minutes", 30)
    for space in _get_spaces():
        if space["id"] == space_id:
            for station in space["beds"]:
                if station["id"] == station_id and station["service"]:
                    station["service"]["duration"] += extra
                    station["service"]["progress"] = max(0, station["service"]["progress"] - 20)
                    return {"message": f"已延长{extra}分钟", "bed": station}
            raise HTTPException(status_code=404, detail="工位不存在或无服务")
    raise HTTPException(status_code=404, detail="空间不存在")


@router.post("/{space_id}/beds/{station_id}/change-technician")
async def change_provider(space_id: int, station_id: int, data: dict):
    """更换服务人员"""
    new_name = data.get("technician_name", "")
    for space in _get_spaces():
        if space["id"] == space_id:
            for station in space["beds"]:
                if station["id"] == station_id and station["technician"]:
                    station["technician"]["name"] = new_name
                    return {"message": f"已更换为{new_name}", "bed": station}
            raise HTTPException(status_code=404, detail="工位不存在")
    raise HTTPException(status_code=404, detail="空间不存在")
