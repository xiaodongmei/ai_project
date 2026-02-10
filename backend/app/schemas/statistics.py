"""统计 Pydantic 模式"""
from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from datetime import datetime, date


class DailyStatisticsResponse(BaseModel):
    """每日统计响应"""
    id: int
    stat_date: date
    expected_revenue: Decimal
    actual_revenue: Decimal
    total_orders: int
    completed_orders: int
    new_customers: int
    total_visitors: int
    created_at: datetime

    class Config:
        from_attributes = True


class ChannelStatisticsResponse(BaseModel):
    """渠道统计响应"""
    channel: str
    order_count: int
    revenue: Decimal
    customer_count: int
    percentage: float = 0.0


class ChannelDistributionResponse(BaseModel):
    """渠道分布响应"""
    channels: List[ChannelStatisticsResponse]
    total_revenue: Decimal
    date: date


class EmployeePerformanceRankResponse(BaseModel):
    """员工绩效排行"""
    rank: int
    employee_id: int
    employee_name: str
    position: str
    total_performance: Decimal
    commission: Decimal
    order_count: int
    date: date


class DashboardDataResponse(BaseModel):
    """仪表板数据"""
    # 营收统计
    shop_revenue: Decimal
    shop_actual_revenue: Decimal
    member_recharge: Decimal

    # 订单统计
    valid_orders: int
    total_items: int

    # 客流统计
    customer_visits: int
    appointment_count: int
    lost_customers: int

    # 渠道分析
    channels: List[ChannelStatisticsResponse] = []

    # 员工绩效
    top_employees: List[EmployeePerformanceRankResponse] = []

    # 时间
    date: date


class ProductSalesResponse(BaseModel):
    """产品销售统计"""
    product_id: int
    product_name: str
    sales_quantity: int
    sales_amount: Decimal
    date: date

    class Config:
        from_attributes = True


class RevenueChartData(BaseModel):
    """收入图表数据"""
    date: str
    revenue: Decimal
    order_count: int


class RevenueChartResponse(BaseModel):
    """收入图表响应"""
    data: List[RevenueChartData]
    total_revenue: Decimal
    average_daily_revenue: Decimal
    start_date: date
    end_date: date


class CustomerSourceResponse(BaseModel):
    """客户来源统计"""
    channel: str
    customer_count: int
    percentage: float


class CustomerAnalyticsResponse(BaseModel):
    """客户分析"""
    total_customers: int
    new_customers_today: int
    member_count: int
    non_member_count: int
    customer_sources: List[CustomerSourceResponse] = []
