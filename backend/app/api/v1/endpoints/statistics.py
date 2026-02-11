"""统计分析端点 - 根据行业模板动态生成演示数据"""
from fastapi import APIRouter, Query
from datetime import date, timedelta
import random

from app.api.v1.endpoints.config import _shop_config, _merge_config
from app.core.industry_templates import get_template

router = APIRouter(prefix="/statistics", tags=["statistics"])


def _get_industry_data():
    """获取当前行业模板数据"""
    cfg = _merge_config(_shop_config)
    template = get_template(cfg.get("industry_type", "general_service"))
    return cfg, template


def _generate_daily_data(days: int = 30):
    """生成每日营收数据"""
    data = []
    today = date.today()
    for i in range(days - 1, -1, -1):
        d = today - timedelta(days=i)
        revenue = round(random.uniform(500, 2500), 2)
        orders = random.randint(5, 25)
        data.append({
            "date": d.isoformat(),
            "revenue": revenue,
            "order_count": orders,
        })
    return data


@router.get("/dashboard")
async def get_dashboard(
    start_date: str = Query(None),
    end_date: str = Query(None),
    time_range: str = Query("30d"),
):
    """获取仪表板统计数据 - 员工名称和服务项目从行业模板动态获取"""
    cfg, template = _get_industry_data()
    staff_roles = cfg.get("staff_roles", ["服务师"])

    # 员工排行 - 使用通用员工名，角色跟随行业模板
    employee_names = ["店长", "李强", "王月", "赵敏", "张峰"]
    # 服务人员对应的角色
    available_roles = [r for r in staff_roles if r != "收银员" and r != "前台"]
    if not available_roles:
        available_roles = staff_roles

    top_employees = []
    performances = [848.8, 250.0, 150.0, 100.0, 80.0]
    order_counts = [5, 3, 2, 2, 1]
    for i, name in enumerate(employee_names):
        role = available_roles[0] if i == 0 else available_roles[min(i, len(available_roles) - 1)]
        top_employees.append({
            "rank": i + 1,
            "name": name,
            "position": role,
            "performance": performances[i],
            "order_count": order_counts[i],
        })

    return {
        "shop_revenue": 829.80,
        "shop_actual_revenue": 802.32,
        "member_recharge": 295.06,
        "one_yuan_cards": 0,
        "card_count": 3,
        "valid_orders": 13,
        "total_items": 12,
        "refund_orders": 0,
        "customer_visits": 13,
        "appointment_count": 0,
        "lost_customers": 0,
        "experience_amount_before": 0.00,
        "experience_amount_after": 0.00,
        "experience_items": 0,
        "channels": [
            {"channel": "美团券", "revenue": 344.8, "order_count": 6, "percentage": 42},
            {"channel": "抖音券", "revenue": 68.0, "order_count": 1, "percentage": 8},
            {"channel": "小程序", "revenue": 0, "order_count": 0, "percentage": 0},
            {"channel": "门店扫码", "revenue": 417.0, "order_count": 6, "percentage": 50},
        ],
        "customer_spending": {
            "member": [680, 520, 450, 380, 300, 250, 180],
            "non_member": [420, 380, 350, 280, 220, 180, 120],
            "visitor": [150, 120, 100, 80, 60, 40, 20],
            "labels": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"],
        },
        "top_employees": top_employees,
        "date": date.today().isoformat(),
    }


@router.get("/revenue")
async def get_revenue(
    start_date: str = Query(None),
    end_date: str = Query(None),
    time_range: str = Query("30d"),
):
    """获取收入趋势数据"""
    days = 30
    if time_range == "7d":
        days = 7
    elif time_range == "90d":
        days = 90

    daily_data = _generate_daily_data(days)
    total = sum(d["revenue"] for d in daily_data)

    return {
        "data": daily_data,
        "total_revenue": round(total, 2),
        "average_daily_revenue": round(total / days, 2),
    }


@router.get("/traffic")
async def get_traffic(
    start_date: str = Query(None),
    end_date: str = Query(None),
    time_range: str = Query("7d"),
):
    """获取客流量统计"""
    days = 7
    if time_range == "30d":
        days = 30

    today = date.today()
    data = []
    for i in range(days - 1, -1, -1):
        d = today - timedelta(days=i)
        data.append({
            "date": d.isoformat(),
            "visitors": random.randint(8, 25),
            "new_customers": random.randint(0, 5),
        })

    return {"data": data}


@router.get("/channels")
async def get_channels(
    start_date: str = Query(None),
    end_date: str = Query(None),
):
    """获取渠道统计"""
    return {
        "channels": [
            {"channel": "美团券", "revenue": 344.8, "order_count": 6, "customer_count": 5, "percentage": 42},
            {"channel": "抖音券", "revenue": 68.0, "order_count": 1, "customer_count": 1, "percentage": 8},
            {"channel": "小程序", "revenue": 0, "order_count": 0, "customer_count": 0, "percentage": 0},
            {"channel": "门店扫码", "revenue": 417.0, "order_count": 6, "customer_count": 5, "percentage": 50},
        ],
        "total_revenue": 829.8,
    }


@router.get("/employees/performance")
async def get_employee_performance(
    start_date: str = Query(None),
    end_date: str = Query(None),
):
    """获取员工绩效 - 角色跟随行业模板"""
    cfg, template = _get_industry_data()
    staff_roles = cfg.get("staff_roles", ["服务师"])
    available_roles = [r for r in staff_roles if r != "收银员" and r != "前台"]
    if not available_roles:
        available_roles = staff_roles

    employee_data = [
        {"name": "店长", "perf": 848.8, "comm": 84.88, "orders": 5},
        {"name": "李强", "perf": 250.0, "comm": 25.0, "orders": 3},
        {"name": "王月", "perf": 150.0, "comm": 15.0, "orders": 2},
        {"name": "赵敏", "perf": 100.0, "comm": 10.0, "orders": 2},
        {"name": "张峰", "perf": 80.0, "comm": 8.0, "orders": 1},
    ]

    data = []
    for i, emp in enumerate(employee_data):
        role = available_roles[0] if i == 0 else available_roles[min(i, len(available_roles) - 1)]
        data.append({
            "rank": i + 1,
            "employee_name": emp["name"],
            "position": role,
            "performance": emp["perf"],
            "commission": emp["comm"],
            "order_count": emp["orders"],
        })

    return {"data": data}


@router.get("/products/sales")
async def get_product_sales(
    start_date: str = Query(None),
    end_date: str = Query(None),
):
    """获取产品/服务项目销售统计 - 从行业模板动态获取服务项目名称"""
    cfg, template = _get_industry_data()
    default_services = template.get("default_services", [])
    service_categories = cfg.get("service_categories", [])

    # 使用 default_services 作为产品名称（更具体）
    if default_services:
        names = [s["name"] for s in default_services[:6]]
    elif service_categories:
        names = service_categories[:6]
    else:
        names = ["服务项目1", "服务项目2", "服务项目3"]

    # 补够6个
    while len(names) < 6:
        names.append(f"其他服务{len(names)}")

    quantities = [120, 95, 78, 65, 42, 35]
    amounts = [5880, 4750, 3900, 3250, 2100, 3500]
    percentages = [28.5, 22.9, 18.9, 15.7, 10.2, 3.8]

    data = []
    for i, name in enumerate(names[:6]):
        data.append({
            "product_name": name,
            "sales_quantity": quantities[i],
            "sales_amount": amounts[i],
            "percentage": percentages[i],
        })

    return {"data": data}


@router.get("/customers")
async def get_customer_stats():
    """获取顾客统计"""
    return {
        "total_customers": 500,
        "active_customers": 450,
        "new_customers": 20,
        "member_count": 200,
    }
