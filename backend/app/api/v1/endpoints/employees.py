"""员工管理端点 - 根据行业模板提供动态mock数据"""
from fastapi import APIRouter, HTTPException
from app.api.v1.endpoints.config import _shop_config, _merge_config
from app.core.industry_templates import get_template

router = APIRouter(prefix="/employees", tags=["employees"])


def _build_employees():
    """根据当前行业模板生成员工数据"""
    cfg = _merge_config(_shop_config)
    industry_type = cfg.get("industry_type", "general_service")
    template = get_template(industry_type)
    staff_roles = cfg.get("staff_roles", template.get("staff_roles", ["服务师"]))
    default_services = template.get("default_services", [])
    skill_tags = cfg.get("skill_tags", template.get("skill_tags", []))

    # 通用员工名称和手机号
    employee_pool = [
        {"name": "李强", "phone": "138****1001", "gender": "male"},
        {"name": "王月", "phone": "139****1002", "gender": "female"},
        {"name": "赵敏", "phone": "136****1003", "gender": "female"},
        {"name": "张峰", "phone": "137****1004", "gender": "male"},
        {"name": "杨枫", "phone": "135****1005", "gender": "male"},
        {"name": "惠珠秀", "phone": "158****1006", "gender": "female"},
        {"name": "刘瑞", "phone": "159****1007", "gender": "male"},
        {"name": "贾少亮", "phone": "177****1008", "gender": "male"},
    ]

    employees = []
    # 第一个总是店长
    employees.append({
        "id": 1,
        "name": "店长",
        "phone": "130****0001",
        "gender": "female",
        "department": industry_type,
        "position": staff_roles[0] if staff_roles else "店长",
        "status": "active",
        "skills": skill_tags[:3] if skill_tags else [],
        "hire_date": "2024-01-01",
        "performance": 848.8,
        "order_count": 5,
    })

    # 根据员工池分配角色
    for i, emp in enumerate(employee_pool):
        # 轮流分配角色（跳过店长角色）
        available_roles = [r for r in staff_roles if r != "店长" and r != "收银员" and r != "前台"]
        if not available_roles:
            available_roles = staff_roles[1:] if len(staff_roles) > 1 else staff_roles
        role = available_roles[i % len(available_roles)] if available_roles else "服务师"

        # 分配技能
        emp_skills = []
        if skill_tags:
            start = (i * 2) % len(skill_tags)
            emp_skills = [skill_tags[start % len(skill_tags)], skill_tags[(start + 1) % len(skill_tags)]]

        employees.append({
            "id": i + 2,
            "name": emp["name"],
            "phone": emp["phone"],
            "gender": emp["gender"],
            "department": industry_type,
            "position": role,
            "status": "active",
            "skills": emp_skills,
            "hire_date": "2024-01-15",
            "performance": round(800 - i * 80, 1),
            "order_count": max(1, 8 - i),
        })

    return employees


# 内存存储 - 允许运行时修改
_custom_employees = []


def _get_employees():
    """获取员工列表（优先自定义，否则行业模板默认）"""
    if _custom_employees:
        return _custom_employees
    return _build_employees()


@router.get("/")
async def list_employees(skip: int = 0, limit: int = 50, search: str = None, position: str = None):
    """获取员工列表"""
    employees = _get_employees()
    filtered = employees[:]
    if search:
        filtered = [e for e in filtered if search.lower() in e["name"].lower()]
    if position:
        filtered = [e for e in filtered if e["position"] == position]
    total = len(filtered)
    return {"total": total, "items": filtered[skip:skip + limit]}


@router.get("/{employee_id}")
async def get_employee(employee_id: int):
    """获取员工详情"""
    for e in _get_employees():
        if e["id"] == employee_id:
            return e
    raise HTTPException(status_code=404, detail="员工不存在")


@router.post("/")
async def create_employee(data: dict):
    """创建员工"""
    employees = _get_employees()
    new_id = max([e["id"] for e in employees], default=0) + 1
    new_emp = {
        "id": new_id,
        "name": data.get("name", ""),
        "phone": data.get("phone", ""),
        "gender": data.get("gender", "male"),
        "department": data.get("department", ""),
        "position": data.get("position", ""),
        "status": "active",
        "skills": data.get("skills", []),
        "hire_date": data.get("hire_date", ""),
        "performance": 0,
        "order_count": 0,
    }
    _custom_employees.clear()
    _custom_employees.extend(employees)
    _custom_employees.append(new_emp)
    return new_emp


@router.put("/{employee_id}")
async def update_employee(employee_id: int, data: dict):
    """更新员工"""
    employees = _get_employees()
    if not _custom_employees:
        _custom_employees.clear()
        _custom_employees.extend(employees)
    for e in _custom_employees:
        if e["id"] == employee_id:
            for k, v in data.items():
                if k != "id":
                    e[k] = v
            return e
    raise HTTPException(status_code=404, detail="员工不存在")


@router.delete("/{employee_id}")
async def delete_employee(employee_id: int):
    """删除员工"""
    employees = _get_employees()
    if not _custom_employees:
        _custom_employees.clear()
        _custom_employees.extend(employees)
    before = len(_custom_employees)
    _custom_employees[:] = [e for e in _custom_employees if e["id"] != employee_id]
    if len(_custom_employees) == before:
        raise HTTPException(status_code=404, detail="员工不存在")
    return {"message": "已删除"}
