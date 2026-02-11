"""订单管理端点 - 根据行业模板动态生成mock数据"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.api.v1.endpoints.config import _shop_config, _merge_config
from app.core.industry_templates import get_template

router = APIRouter(prefix="/orders", tags=["orders"])

# 内存存储订单
_custom_orders = []


def _build_default_orders():
    """根据当前行业模板生成默认订单"""
    cfg = _merge_config(_shop_config)
    template = get_template(cfg.get("industry_type", "general_service"))
    services = template.get("default_services", [])
    svc_names = [s["name"] for s in services] if services else ["基础服务"]
    provider_label = cfg.get("provider_label", "服务师")

    # 员工名称
    employees = ["李强", "王月", "赵敏", "张峰", "杨枫"]

    customers = [
        {"name": "陈静", "phone": "138****1234"},
        {"name": "张三", "phone": "159****5678"},
        {"name": "李四", "phone": "132****9012"},
        {"name": "刘洋", "phone": "186****3456"},
        {"name": "王芳", "phone": "177****7890"},
    ]

    statuses = ["completed", "completed", "pending", "completed", "pending"]
    times = ["10:30", "11:00", "11:30", "14:00", "14:30"]

    orders = []
    for i in range(5):
        svc = svc_names[i % len(svc_names)]
        emp = employees[i % len(employees)]
        cust = customers[i]
        price = services[i % len(services)]["price"] if services else 100
        orders.append({
            "id": i + 1,
            "order_no": f"ORD{str(i + 1).zfill(3)}",
            "customer_id": i + 1,
            "customer_name": cust["name"],
            "employee_name": emp,
            "service_items": [svc],
            "service_display": f"{svc}-{emp}",
            "total_amount": price,
            "amount": price,
            "discount": 0,
            "status": statuses[i],
            "payment_method": "cash",
            "remark": "",
            "created_at": f"2026-02-11T{times[i]}:00",
        })
    return orders


def _get_orders():
    if _custom_orders:
        return _custom_orders
    return _build_default_orders()


@router.get("/")
async def list_orders(skip: int = 0, limit: int = 20, search: str = None, status: str = None):
    """获取订单列表"""
    orders = _get_orders()
    filtered = orders[:]
    if search:
        filtered = [o for o in filtered
                     if search.lower() in o.get("order_no", "").lower()
                     or search.lower() in o.get("customer_name", "").lower()]
    if status:
        filtered = [o for o in filtered if o["status"] == status]
    total = len(filtered)
    return {"total": total, "items": filtered[skip:skip + limit]}


@router.get("/{order_id}")
async def get_order(order_id: int):
    """获取订单详情"""
    for o in _get_orders():
        if o["id"] == order_id:
            return o
    raise HTTPException(status_code=404, detail="订单不存在")


@router.post("/")
async def create_order(data: dict):
    """创建订单"""
    orders = _get_orders()
    new_id = max([o["id"] for o in orders], default=0) + 1
    svc_items = data.get("service_items", [])
    emp_name = data.get("employee_name", "")

    # 构建 "服务-员工" 显示字段
    svc_display = ", ".join([f"{s}-{emp_name}" for s in svc_items]) if svc_items and emp_name else ""

    new_order = {
        "id": new_id,
        "order_no": f"ORD{str(new_id).zfill(3)}",
        "customer_id": None,
        "customer_name": data.get("customer_name", ""),
        "employee_name": emp_name,
        "service_items": svc_items,
        "service_display": svc_display,
        "total_amount": data.get("amount", 0),
        "amount": data.get("amount", 0),
        "discount": data.get("discount", 0),
        "status": data.get("status", "pending"),
        "payment_method": data.get("payment_method", "cash"),
        "remark": data.get("remark", ""),
        "created_at": datetime.now().isoformat(),
    }
    if not _custom_orders:
        _custom_orders.extend(orders)
    _custom_orders.append(new_order)
    return new_order


@router.put("/{order_id}")
async def update_order(order_id: int, data: dict):
    """更新订单"""
    orders = _get_orders()
    if not _custom_orders:
        _custom_orders.extend(orders)
    for o in _custom_orders:
        if o["id"] == order_id:
            for k, v in data.items():
                if k != "id":
                    o[k] = v
            # 更新显示字段
            if "service_items" in data or "employee_name" in data:
                svc_items = o.get("service_items", [])
                emp_name = o.get("employee_name", "")
                o["service_display"] = ", ".join([f"{s}-{emp_name}" for s in svc_items]) if svc_items and emp_name else ""
            return o
    raise HTTPException(status_code=404, detail="订单不存在")


@router.delete("/{order_id}")
async def delete_order(order_id: int):
    """删除订单"""
    orders = _get_orders()
    if not _custom_orders:
        _custom_orders.extend(orders)
    before = len(_custom_orders)
    _custom_orders[:] = [o for o in _custom_orders if o["id"] != order_id]
    if len(_custom_orders) == before:
        raise HTTPException(status_code=404, detail="订单不存在")
    return {"message": "已删除"}
