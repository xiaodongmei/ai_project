"""员工 Pydantic 模式"""
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime, date


class EmployeeBase(BaseModel):
    """员工基础模式"""
    name: str
    employee_id: str
    position: str
    department: str
    base_salary: Decimal
    commission_rate: Decimal = Decimal("0.05")


class EmployeeCreate(EmployeeBase):
    """创建员工"""
    pass


class EmployeeUpdate(BaseModel):
    """更新员工"""
    name: Optional[str] = None
    position: Optional[str] = None
    department: Optional[str] = None
    base_salary: Optional[Decimal] = None
    commission_rate: Optional[Decimal] = None


class EmployeeResponse(EmployeeBase):
    """员工响应模式"""
    id: int
    total_commission: Decimal
    total_performance: Decimal
    customer_count: int
    status: str
    joined_date: date
    left_date: Optional[date] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EmployeePerformanceResponse(BaseModel):
    """员工绩效响应"""
    employee_id: int
    employee_name: str
    total_performance: Decimal
    commission: Decimal
    order_count: int
    customer_count: int
    rank: Optional[int] = None
    date: date
