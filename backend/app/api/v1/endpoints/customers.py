"""顾客管理端点"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/customers", tags=["customers"])


class Customer(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    membership_status: str = "regular"


class CustomerUpdate(BaseModel):
    """更新顾客时所有字段可选"""
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    membership_status: Optional[str] = None


# 模拟数据
customers_db = [
    {
        "id": 1,
        "name": "张三",
        "phone": "13800138000",
        "email": "zhangsan@example.com",
        "membership_status": "vip",
        "total_consumption": 5000.00
    },
    {
        "id": 2,
        "name": "李四",
        "phone": "13900139000",
        "email": "lisi@example.com",
        "membership_status": "regular",
        "total_consumption": 1000.00
    }
]


@router.get("/")
async def list_customers(skip: int = 0, limit: int = 10):
    """获取顾客列表"""
    return {
        "total": len(customers_db),
        "items": customers_db[skip:skip + limit]
    }


@router.get("/{customer_id}")
async def get_customer(customer_id: int):
    """获取单个顾客"""
    for customer in customers_db:
        if customer["id"] == customer_id:
            return customer
    return {"error": "Customer not found"}


@router.post("/")
async def create_customer(customer: Customer):
    """创建顾客"""
    new_customer = customer.dict()
    new_customer["id"] = len(customers_db) + 1
    new_customer["total_consumption"] = 0
    customers_db.append(new_customer)
    return new_customer


@router.put("/{customer_id}")
async def update_customer(customer_id: int, customer: CustomerUpdate):
    """更新顾客信息"""
    for i, existing_customer in enumerate(customers_db):
        if existing_customer["id"] == customer_id:
            # 只更新传入的字段
            updated_data = customer.dict(exclude_unset=True)
            customers_db[i].update(updated_data)
            return customers_db[i]
    return {"error": "Customer not found"}


@router.delete("/{customer_id}")
async def delete_customer(customer_id: int):
    """删除顾客"""
    for i, customer in enumerate(customers_db):
        if customer["id"] == customer_id:
            deleted = customers_db.pop(i)
            return {"message": "Customer deleted", "data": deleted}
    return {"error": "Customer not found"}
