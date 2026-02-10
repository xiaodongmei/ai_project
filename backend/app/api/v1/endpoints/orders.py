"""订单管理端点"""
from fastapi import APIRouter

router = APIRouter(prefix="/orders", tags=["orders"])

# 模拟数据
orders_db = [
    {
        "id": 1,
        "customer_id": 1,
        "total_amount": 176.00,
        "status": "completed",
        "created_at": "2024-01-15T10:00:00"
    }
]


@router.get("/")
async def list_orders(skip: int = 0, limit: int = 10):
    """获取订单列表"""
    return {
        "total": len(orders_db),
        "items": orders_db[skip:skip + limit]
    }
