"""店铺配置和行业模板 API"""
import json
from fastapi import APIRouter

from app.core.industry_templates import get_template, get_all_templates, INDUSTRY_TEMPLATES

router = APIRouter(prefix="/config", tags=["店铺配置"])

# 内存中的店铺配置（后续接入数据库）
_shop_config = {
    "id": 1,
    "shop_name": "我的店铺",
    "industry_type": "wellness_spa",
    "description": "",
    "address": "",
    "phone": "",
    "business_hours": "09:00-21:00",
    "logo_url": "",
    "custom_space_label": None,
    "custom_station_label": None,
    "custom_provider_label": None,
    "custom_space_types": None,
    "custom_station_types": None,
    "custom_staff_roles": None,
    "custom_service_categories": None,
    "custom_product_categories": None,
    "custom_skill_tags": None,
}


def _merge_config(config: dict) -> dict:
    """合并店铺自定义配置和行业模板默认值"""
    template = get_template(config.get("industry_type", "general_service"))
    # 解析自定义JSON字段
    def parse_json_or_default(custom_val, template_key):
        if custom_val:
            try:
                return json.loads(custom_val)
            except (json.JSONDecodeError, TypeError):
                pass
        return template.get(template_key, [])

    return {
        "shop_name": config.get("shop_name", "我的店铺"),
        "industry_type": config.get("industry_type", "general_service"),
        "description": config.get("description", ""),
        "address": config.get("address", ""),
        "phone": config.get("phone", ""),
        "business_hours": config.get("business_hours", ""),
        "logo_url": config.get("logo_url", ""),
        # 术语（优先自定义，回退模板默认）
        "space_label": config.get("custom_space_label") or template["space_label"],
        "space_label_plural": template["space_label_plural"],
        "station_label": config.get("custom_station_label") or template["station_label"],
        "provider_label": config.get("custom_provider_label") or template["provider_label"],
        "provider_label_plural": template["provider_label_plural"],
        # 选项列表（优先自定义，回退模板默认）
        "space_types": parse_json_or_default(config.get("custom_space_types"), "space_types"),
        "station_types": parse_json_or_default(config.get("custom_station_types"), "station_types"),
        "staff_roles": parse_json_or_default(config.get("custom_staff_roles"), "staff_roles"),
        "service_categories": parse_json_or_default(config.get("custom_service_categories"), "service_categories"),
        "product_categories": parse_json_or_default(config.get("custom_product_categories"), "product_categories"),
        "skill_tags": parse_json_or_default(config.get("custom_skill_tags"), "skill_tags"),
        # 默认服务项目（含价格、时长等详情）
        "default_services": template.get("default_services", []),
    }


@router.get("/shop")
async def get_shop_config():
    """获取当前店铺的完整配置（合并行业模板+自定义配置）"""
    return _merge_config(_shop_config)


@router.put("/shop")
async def update_shop_config(data: dict):
    """更新店铺配置"""
    allowed_fields = [
        "shop_name", "industry_type", "description", "address", "phone",
        "business_hours", "logo_url",
        "custom_space_label", "custom_station_label", "custom_provider_label",
        "custom_space_types", "custom_station_types", "custom_staff_roles",
        "custom_service_categories", "custom_product_categories", "custom_skill_tags",
    ]
    for key, value in data.items():
        if key in allowed_fields:
            _shop_config[key] = value
    return _merge_config(_shop_config)


@router.get("/templates")
async def get_industry_templates():
    """获取所有行业模板列表（用于前端选择）"""
    return get_all_templates()


@router.get("/templates/{industry_type}")
async def get_industry_template_detail(industry_type: str):
    """获取指定行业模板的完整配置"""
    template = get_template(industry_type)
    return template
