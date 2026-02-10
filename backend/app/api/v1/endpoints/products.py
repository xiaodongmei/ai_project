"""产品管理端点 - 演示数据"""
from fastapi import APIRouter, Query
from typing import Optional

products_router = APIRouter(prefix="/products", tags=["products"])
categories_router = APIRouter(prefix="/product-categories", tags=["categories"])
router = APIRouter()

# 产品分类
categories_db = [
    {"id": 1, "name": "养方", "description": "养生药方系列", "display_order": 1, "is_active": True},
    {"id": 2, "name": "枕头", "description": "养生枕头", "display_order": 2, "is_active": True},
    {"id": 3, "name": "养生小食", "description": "健康零食", "display_order": 3, "is_active": True},
    {"id": 4, "name": "艾草棒", "description": "艾灸用品", "display_order": 4, "is_active": True},
    {"id": 5, "name": "手提袋", "description": "包装袋", "display_order": 5, "is_active": True},
    {"id": 6, "name": "热敷贴", "description": "热敷理疗贴", "display_order": 6, "is_active": True},
    {"id": 7, "name": "养生茶", "description": "养生茶饮", "display_order": 7, "is_active": True},
    {"id": 8, "name": "三伏养生", "description": "三伏天养生产品", "display_order": 8, "is_active": True},
    {"id": 9, "name": "合液", "description": "养生合液", "display_order": 9, "is_active": True},
]

# 产品数据
products_db = [
    {"id": 1, "name": "低糖铁陈果芝麻丸(升级款)", "category_id": 1, "category_name": "养方", "price": 14.9, "member_price": 14.9, "stock": 200, "sales_volume": 86, "is_active": True, "image": None},
    {"id": 2, "name": "黄荟山楂膏155g", "category_id": 1, "category_name": "养方", "price": 14.9, "member_price": 14.9, "stock": 150, "sales_volume": 65, "is_active": True, "image": None},
    {"id": 3, "name": "五青方雪花酥单袋", "category_id": 3, "category_name": "养生小食", "price": 9.9, "member_price": 9.9, "stock": 300, "sales_volume": 120, "is_active": True, "image": None},
    {"id": 4, "name": "五青方雪花酥单袋(大)", "category_id": 3, "category_name": "养生小食", "price": 14.9, "member_price": 14.9, "stock": 180, "sales_volume": 95, "is_active": True, "image": None},
    {"id": 5, "name": "五黑方雪花酥单袋", "category_id": 3, "category_name": "养生小食", "price": 9.9, "member_price": 9.9, "stock": 250, "sales_volume": 110, "is_active": True, "image": None},
    {"id": 6, "name": "五黑方雪花酥", "category_id": 3, "category_name": "养生小食", "price": 29.9, "member_price": 29.9, "stock": 100, "sales_volume": 45, "is_active": True, "image": None},
    {"id": 7, "name": "五青方雪花酥", "category_id": 3, "category_name": "养生小食", "price": 39.9, "member_price": 39.9, "stock": 100, "sales_volume": 55, "is_active": True, "image": None},
    {"id": 8, "name": "梨膏软心糖 老", "category_id": 3, "category_name": "养生小食", "price": 9.9, "member_price": 9.9, "stock": 200, "sales_volume": 78, "is_active": True, "image": None},
    {"id": 9, "name": "黄金五黑软糖", "category_id": 3, "category_name": "养生小食", "price": 9.9, "member_price": 9.9, "stock": 180, "sales_volume": 60, "is_active": True, "image": None},
    {"id": 10, "name": "乌盈六黑糕", "category_id": 3, "category_name": "养生小食", "price": 29.9, "member_price": 29.9, "stock": 120, "sales_volume": 35, "is_active": True, "image": None},
    {"id": 11, "name": "鸡内金山楂盘清棒", "category_id": 3, "category_name": "养生小食", "price": 29.9, "member_price": 29.9, "stock": 90, "sales_volume": 28, "is_active": True, "image": None},
    {"id": 12, "name": "艾草精油棒(大)", "category_id": 4, "category_name": "艾草棒", "price": 68.0, "member_price": 58.0, "stock": 50, "sales_volume": 42, "is_active": True, "image": None},
    {"id": 13, "name": "艾草精油棒(小)", "category_id": 4, "category_name": "艾草棒", "price": 38.0, "member_price": 28.0, "stock": 80, "sales_volume": 55, "is_active": True, "image": None},
    {"id": 14, "name": "养生枕头-薰衣草", "category_id": 2, "category_name": "枕头", "price": 128.0, "member_price": 98.0, "stock": 30, "sales_volume": 18, "is_active": True, "image": None},
    {"id": 15, "name": "养生枕头-决明子", "category_id": 2, "category_name": "枕头", "price": 98.0, "member_price": 78.0, "stock": 25, "sales_volume": 22, "is_active": True, "image": None},
    {"id": 16, "name": "肩颈热敷贴", "category_id": 6, "category_name": "热敷贴", "price": 15.0, "member_price": 12.0, "stock": 500, "sales_volume": 200, "is_active": True, "image": None},
    {"id": 17, "name": "腰部热敷贴", "category_id": 6, "category_name": "热敷贴", "price": 15.0, "member_price": 12.0, "stock": 400, "sales_volume": 180, "is_active": True, "image": None},
    {"id": 18, "name": "菊花决明子茶", "category_id": 7, "category_name": "养生茶", "price": 38.0, "member_price": 28.0, "stock": 100, "sales_volume": 65, "is_active": True, "image": None},
    {"id": 19, "name": "红枣枸杞茶", "category_id": 7, "category_name": "养生茶", "price": 38.0, "member_price": 28.0, "stock": 80, "sales_volume": 72, "is_active": True, "image": None},
    {"id": 20, "name": "手提袋(大)", "category_id": 5, "category_name": "手提袋", "price": 3.0, "member_price": 2.0, "stock": 1000, "sales_volume": 300, "is_active": True, "image": None},
]


# 产品分类接口
@categories_router.get("")
async def list_categories():
    """获取产品分类列表"""
    return {"total": len(categories_db), "items": categories_db}


@categories_router.get("/{category_id}")
async def get_category(category_id: int):
    for c in categories_db:
        if c["id"] == category_id:
            return c
    return {"error": "Category not found"}


@categories_router.post("/")
async def create_category(data: dict):
    new_id = max([c["id"] for c in categories_db], default=0) + 1
    new_cat = {"id": new_id, "name": data.get("name"), "description": data.get("description", ""), "display_order": data.get("display_order", 0), "is_active": True}
    categories_db.append(new_cat)
    return new_cat


@categories_router.put("/{category_id}")
async def update_category(category_id: int, data: dict):
    for c in categories_db:
        if c["id"] == category_id:
            c.update(data)
            return c
    return {"error": "Category not found"}


@categories_router.delete("/{category_id}")
async def delete_category(category_id: int):
    global categories_db
    categories_db = [c for c in categories_db if c["id"] != category_id]
    return {"success": True}


# 产品接口
@products_router.get("")
async def list_products(
    skip: int = 0,
    limit: int = 50,
    search: Optional[str] = None,
    category_id: Optional[int] = None,
):
    """获取产品列表"""
    filtered = products_db[:]
    if search:
        filtered = [p for p in filtered if search.lower() in p["name"].lower()]
    if category_id:
        filtered = [p for p in filtered if p["category_id"] == category_id]
    total = len(filtered)
    items = filtered[skip:skip + limit]
    return {"total": total, "items": items}


@products_router.get("/{product_id}")
async def get_product(product_id: int):
    for p in products_db:
        if p["id"] == product_id:
            return p
    return {"error": "Product not found"}


@products_router.post("/")
async def create_product(data: dict):
    new_id = max([p["id"] for p in products_db], default=0) + 1
    cat_name = ""
    for c in categories_db:
        if c["id"] == data.get("category_id"):
            cat_name = c["name"]
            break
    new_prod = {
        "id": new_id,
        "name": data.get("name", ""),
        "category_id": data.get("category_id"),
        "category_name": cat_name,
        "price": data.get("price", 0),
        "member_price": data.get("member_price", 0),
        "stock": data.get("stock", 0),
        "sales_volume": 0,
        "is_active": True,
        "image": None,
    }
    products_db.append(new_prod)
    return new_prod


@products_router.put("/{product_id}")
async def update_product(product_id: int, data: dict):
    for p in products_db:
        if p["id"] == product_id:
            p.update(data)
            return p
    return {"error": "Product not found"}


@products_router.delete("/{product_id}")
async def delete_product(product_id: int):
    global products_db
    products_db = [p for p in products_db if p["id"] != product_id]
    return {"success": True}


router.include_router(products_router)
router.include_router(categories_router)
