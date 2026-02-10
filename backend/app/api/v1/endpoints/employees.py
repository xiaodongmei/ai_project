"""员工管理端点"""
from fastapi import APIRouter

router = APIRouter(prefix="/employees", tags=["employees"])

# 模拟数据
employees_db = [
    {
        "id": 1,
        "name": "王五",
        "department": "massage",
        "position": "therapist",
        "status": "active"
    }
]


@router.get("/")
async def list_employees(skip: int = 0, limit: int = 10):
    """获取员工列表"""
    return {
        "total": len(employees_db),
        "items": employees_db[skip:skip + limit]
    }
