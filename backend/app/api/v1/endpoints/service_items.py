"""服务项目管理端点

提供服务项目的CRUD操作，数据来源：
1. 行业模板默认服务（default_services）
2. 用户自定义服务项目（custom_services）
用户可以在设置页面添加/编辑/删除自己的服务项目。
"""
from fastapi import APIRouter, HTTPException
from app.api.v1.endpoints.config import _shop_config, _merge_config
from app.core.industry_templates import get_template

router = APIRouter(prefix="/service-items", tags=["服务项目管理"])

# 内存存储自定义服务项目（后续接入数据库）
_custom_services = []


def _get_services():
    """获取服务项目列表（优先自定义，否则行业模板默认）"""
    if _custom_services:
        return _custom_services[:]
    cfg = _merge_config(_shop_config)
    template = get_template(cfg.get("industry_type", "general_service"))
    default_services = template.get("default_services", [])
    # 为默认服务添加id
    return [
        {
            "id": i + 1,
            "name": s["name"],
            "category": cfg.get("service_categories", [])[i % len(cfg.get("service_categories", ["默认"]))] if cfg.get("service_categories") else "默认",
            "duration": s.get("duration", 60),
            "price": s.get("price", 0),
            "is_active": True,
            "description": "",
        }
        for i, s in enumerate(default_services)
    ]


@router.get("")
async def list_services(category: str = None, is_active: bool = None):
    """获取服务项目列表"""
    services = _get_services()
    if category:
        services = [s for s in services if s.get("category") == category]
    if is_active is not None:
        services = [s for s in services if s.get("is_active") == is_active]
    return {"total": len(services), "items": services}


@router.get("/{service_id}")
async def get_service(service_id: int):
    """获取单个服务项目"""
    for s in _get_services():
        if s["id"] == service_id:
            return s
    raise HTTPException(status_code=404, detail="服务项目不存在")


@router.post("")
async def create_service(data: dict):
    """创建服务项目"""
    services = _get_services()
    new_id = max([s["id"] for s in services], default=0) + 1
    new_service = {
        "id": new_id,
        "name": data.get("name", ""),
        "category": data.get("category", ""),
        "duration": data.get("duration", 60),
        "price": data.get("price", 0),
        "is_active": data.get("is_active", True),
        "description": data.get("description", ""),
    }
    if not _custom_services:
        _custom_services.extend(services)
    _custom_services.append(new_service)
    return new_service


@router.put("/{service_id}")
async def update_service(service_id: int, data: dict):
    """更新服务项目"""
    services = _get_services()
    if not _custom_services:
        _custom_services.extend(services)
    for s in _custom_services:
        if s["id"] == service_id:
            for k, v in data.items():
                if k != "id":
                    s[k] = v
            return s
    raise HTTPException(status_code=404, detail="服务项目不存在")


@router.delete("/{service_id}")
async def delete_service(service_id: int):
    """删除服务项目"""
    services = _get_services()
    if not _custom_services:
        _custom_services.extend(services)
    before = len(_custom_services)
    _custom_services[:] = [s for s in _custom_services if s["id"] != service_id]
    if len(_custom_services) == before:
        raise HTTPException(status_code=404, detail="服务项目不存在")
    return {"message": "已删除"}


@router.post("/reset")
async def reset_services():
    """重置为行业模板默认服务项目"""
    _custom_services.clear()
    return {"message": "已重置为默认服务项目", "items": _get_services()}
