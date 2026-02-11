"""行业模板配置 - 通用化服务类店铺管理系统

支持的行业类型:
- wellness_spa: 养生推拿
- nail_salon: 美甲美睫
- hair_salon: 美发沙龙
- hanfu_studio: 汉服妆造
- general_service: 通用服务（自定义）
"""

INDUSTRY_TEMPLATES = {
    "wellness_spa": {
        "name": "养生推拿",
        "icon": "spa",
        "description": "适用于养生馆、推拿馆、SPA会所等",
        # 空间和工位术语
        "space_label": "房间",
        "space_label_plural": "房间管理",
        "station_label": "床位",
        # 服务人员术语
        "provider_label": "技师",
        "provider_label_plural": "技师管理",
        # 空间类型选项
        "space_types": ["VIP包间", "标准间", "单人间", "足疗间", "SPA间"],
        # 工位类型选项
        "station_types": ["按摩床", "足疗椅", "SPA床", "艾灸床"],
        # 员工角色选项
        "staff_roles": ["店长", "技师", "调理师", "收银员", "前台"],
        # 默认服务分类
        "service_categories": [
            "推拿按摩", "足疗", "艾灸", "拔罐", "刮痧",
            "精油SPA", "肩颈理疗", "头部按摩",
        ],
        # 默认商品分类
        "product_categories": [
            "养方", "枕头", "养生小食", "艾草棒", "热敷贴",
            "养生茶", "精油", "保健品",
        ],
        # 服务人员技能标签
        "skill_tags": [
            "推拿", "足疗", "艾灸", "拔罐", "刮痧",
            "精油SPA", "肩颈理疗", "头部按摩",
        ],
        # 默认服务项目
        "default_services": [
            {"name": "肩颈推拿", "duration": 60, "price": 198},
            {"name": "足部按摩", "duration": 60, "price": 168},
            {"name": "艾灸理疗", "duration": 60, "price": 258},
            {"name": "精油SPA", "duration": 90, "price": 398},
            {"name": "拔罐", "duration": 30, "price": 128},
            {"name": "刮痧", "duration": 45, "price": 158},
        ],
    },
    "nail_salon": {
        "name": "美甲美睫",
        "icon": "nail",
        "description": "适用于美甲店、美睫店、美容院等",
        "space_label": "服务区",
        "space_label_plural": "服务区管理",
        "station_label": "工位",
        "provider_label": "美甲师",
        "provider_label_plural": "美甲师管理",
        "space_types": ["美甲区", "美睫区", "VIP室", "手部护理区"],
        "station_types": ["美甲台", "美睫床", "护理台"],
        "staff_roles": ["店长", "美甲师", "美睫师", "美容师", "收银员", "前台"],
        "service_categories": [
            "基础美甲", "高级美甲", "美甲款式", "卸甲",
            "嫁接美睫", "美睫款式", "卸睫", "手部护理",
        ],
        "product_categories": [
            "指甲油", "甲片", "水钻饰品", "美睫材料",
            "护手霜", "美甲工具", "美容用品",
        ],
        "skill_tags": [
            "日式美甲", "法式美甲", "彩绘", "镶钻",
            "嫁接美睫", "日式美睫", "卸甲", "手部护理",
        ],
        "default_services": [
            {"name": "纯色美甲", "duration": 60, "price": 98},
            {"name": "彩绘美甲", "duration": 90, "price": 198},
            {"name": "日式美甲", "duration": 90, "price": 258},
            {"name": "嫁接美睫", "duration": 60, "price": 168},
            {"name": "卸甲", "duration": 30, "price": 38},
            {"name": "手部护理", "duration": 45, "price": 128},
        ],
    },
    "hair_salon": {
        "name": "美发沙龙",
        "icon": "scissors",
        "description": "适用于理发店、美发沙龙、造型工作室等",
        "space_label": "区域",
        "space_label_plural": "区域管理",
        "station_label": "工位",
        "provider_label": "发型师",
        "provider_label_plural": "发型师管理",
        "space_types": ["剪发区", "洗发区", "烫染区", "VIP室"],
        "station_types": ["理发椅", "洗头床", "烫染位", "造型台"],
        "staff_roles": ["店长", "总监发型师", "资深发型师", "发型师", "助理", "洗护师", "收银员"],
        "service_categories": [
            "剪发", "烫发", "染发", "洗护",
            "造型", "接发", "头皮护理", "焗油",
        ],
        "product_categories": [
            "洗发水", "护发素", "发蜡发泥", "染发剂",
            "护理精油", "造型工具", "头皮护理",
        ],
        "skill_tags": [
            "男士剪发", "女士剪发", "烫发", "染发",
            "造型", "接发", "头皮护理", "焗油",
        ],
        "default_services": [
            {"name": "男士剪发", "duration": 30, "price": 68},
            {"name": "女士剪发", "duration": 45, "price": 128},
            {"name": "烫发", "duration": 120, "price": 398},
            {"name": "染发", "duration": 90, "price": 298},
            {"name": "洗吹造型", "duration": 30, "price": 58},
            {"name": "头皮护理", "duration": 45, "price": 168},
        ],
    },
    "hanfu_studio": {
        "name": "汉服妆造",
        "icon": "palette",
        "description": "适用于汉服体验馆、妆造工作室、古风摄影等",
        "space_label": "功能区",
        "space_label_plural": "功能区管理",
        "station_label": "工位",
        "provider_label": "造型师",
        "provider_label_plural": "造型师管理",
        "space_types": ["化妆间", "换装区", "拍摄区", "VIP化妆间", "等候区"],
        "station_types": ["化妆台", "换装位", "拍摄位", "盘发位"],
        "staff_roles": ["店长", "造型师", "化妆师", "摄影师", "穿搭师", "前台"],
        "service_categories": [
            "古风全妆", "日常汉服妆", "盘发造型", "汉服穿搭",
            "汉服租赁", "跟拍服务", "证件照", "写真套餐",
        ],
        "product_categories": [
            "汉服", "发饰", "配饰", "团扇",
            "化妆品", "道具", "摄影周边",
        ],
        "skill_tags": [
            "古风妆", "日常妆", "特效妆", "盘发",
            "汉服穿搭", "古风摄影", "后期修图",
        ],
        "default_services": [
            {"name": "古风全妆造型", "duration": 90, "price": 298},
            {"name": "日常汉服妆", "duration": 60, "price": 168},
            {"name": "盘发造型", "duration": 45, "price": 128},
            {"name": "汉服体验套餐", "duration": 180, "price": 598},
            {"name": "跟拍服务", "duration": 120, "price": 498},
            {"name": "精修写真", "duration": 60, "price": 398},
        ],
    },
    "general_service": {
        "name": "通用服务",
        "icon": "service",
        "description": "通用服务类店铺，可完全自定义",
        "space_label": "服务区",
        "space_label_plural": "服务区管理",
        "station_label": "工位",
        "provider_label": "服务师",
        "provider_label_plural": "服务师管理",
        "space_types": ["标准区", "VIP区"],
        "station_types": ["标准工位", "VIP工位"],
        "staff_roles": ["店长", "服务师", "收银员", "前台"],
        "service_categories": ["基础服务", "高级服务", "VIP服务"],
        "product_categories": ["常规商品", "耗材", "周边"],
        "skill_tags": ["基础服务", "高级服务"],
        "default_services": [
            {"name": "基础服务", "duration": 60, "price": 100},
            {"name": "高级服务", "duration": 90, "price": 200},
        ],
    },
}


def get_template(industry_type: str) -> dict:
    """获取行业模板，不存在则返回通用模板"""
    return INDUSTRY_TEMPLATES.get(industry_type, INDUSTRY_TEMPLATES["general_service"])


def get_all_templates() -> dict:
    """获取所有行业模板（用于前端选择）"""
    return {
        key: {
            "name": val["name"],
            "icon": val["icon"],
            "description": val["description"],
        }
        for key, val in INDUSTRY_TEMPLATES.items()
    }
