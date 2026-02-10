"""统计分析端点 - 演示数据"""
from fastapi import APIRouter, Query
from datetime import datetime, date, timedelta
from decimal import Decimal
import random

router = APIRouter(prefix="/statistics", tags=["statistics"])


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
    """获取仪表板统计数据"""
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
        "top_employees": [
            {"rank": 1, "name": "店长", "performance": 848.8, "order_count": 5},
            {"rank": 2, "name": "张月芳", "performance": 250.0, "order_count": 3},
            {"rank": 3, "name": "惠珠秀", "performance": 150.0, "order_count": 2},
            {"rank": 4, "name": "杨枫", "performance": 100.0, "order_count": 2},
            {"rank": 5, "name": "王浪峰", "performance": 80.0, "order_count": 1},
        ],
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
    """获取员工绩效"""
    return {
        "data": [
            {"rank": 1, "employee_name": "店长", "position": "店长", "performance": 848.8, "commission": 84.88, "order_count": 5},
            {"rank": 2, "employee_name": "张月芳", "position": "调理师", "performance": 250.0, "commission": 25.0, "order_count": 3},
            {"rank": 3, "employee_name": "惠珠秀", "position": "调理师", "performance": 150.0, "commission": 15.0, "order_count": 2},
            {"rank": 4, "employee_name": "杨枫", "position": "调理师", "performance": 100.0, "commission": 10.0, "order_count": 2},
            {"rank": 5, "employee_name": "王浪峰", "position": "调理师", "performance": 80.0, "commission": 8.0, "order_count": 1},
        ]
    }


@router.get("/products/sales")
async def get_product_sales(
    start_date: str = Query(None),
    end_date: str = Query(None),
):
    """获取产品销售统计"""
    return {
        "data": [
            {"product_name": "肩颈疗法", "sales_quantity": 120, "sales_amount": 5880, "percentage": 28.5},
            {"product_name": "足疗", "sales_quantity": 95, "sales_amount": 4750, "percentage": 22.9},
            {"product_name": "拔罐", "sales_quantity": 78, "sales_amount": 3900, "percentage": 18.9},
            {"product_name": "刮痧", "sales_quantity": 65, "sales_amount": 3250, "percentage": 15.7},
            {"product_name": "艾灸", "sales_quantity": 42, "sales_amount": 2100, "percentage": 10.2},
            {"product_name": "精油SPA", "sales_quantity": 35, "sales_amount": 3500, "percentage": 3.8},
        ]
    }


@router.get("/customers")
async def get_customer_stats():
    """获取顾客统计"""
    return {
        "total_customers": 500,
        "active_customers": 450,
        "new_customers": 20,
        "member_count": 200,
    }
