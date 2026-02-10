# 后端测试执行指南

## 📋 已实现的测试

### 1. 单元测试 (Unit Tests)

#### 模型测试
- `tests/test_models/test_user.py` - User 模型 (10个测试)
- `tests/test_models/test_customer.py` - Customer 模型 (10个测试)
- `tests/test_models/test_product.py` - Product 模型 (14个测试)
- `tests/test_models/test_order.py` - Order 模型 (15个测试)
- `tests/test_models/test_employee.py` - Employee 模型 (10个测试)

**小计**: 59个模型测试

#### 安全性测试
- `tests/test_security/test_password.py` - 密码安全 (10个测试)
- `tests/test_security/test_jwt.py` - JWT 安全 (12个测试)

**小计**: 22个安全测试

#### Schema 验证测试
- `tests/test_schemas/test_user_schema.py` - User Schema 验证 (13个测试)

**小计**: 13个 schema 测试

**单元测试总数**: 94个测试

---

### 2. 集成测试 (Integration Tests)

#### API 测试
- `tests/test_api/test_health.py` - 健康检查和 API 信息端点 (4个测试)

#### 数据库测试
- `tests/test_database/test_crud.py` - CRUD 操作 (22个测试)
  - User CRUD (5个)
  - Product CRUD (5个)
  - Order CRUD (5个)
  - 订单项操作

**集成测试总数**: 26个测试

---

## 🚀 运行测试

### 前置条件

```bash
cd backend
pip install -r requirements.txt
```

### 运行所有测试

```bash
pytest
```

### 运行特定测试文件

```bash
# 运行用户模型测试
pytest tests/test_models/test_user.py

# 运行所有模型测试
pytest tests/test_models/

# 运行所有安全性测试
pytest tests/test_security/

# 运行所有 API 测试
pytest tests/test_api/

# 运行所有数据库测试
pytest tests/test_database/
```

### 运行特定测试

```bash
# 运行特定测试类
pytest tests/test_models/test_user.py::TestUserModel

# 运行特定测试方法
pytest tests/test_models/test_user.py::TestUserModel::test_create_user
```

### 生成覆盖率报告

```bash
# 基本覆盖率报告
pytest --cov=app

# 生成详细的 HTML 报告
pytest --cov=app --cov-report=html

# 显示遗漏的代码行
pytest --cov=app --cov-report=term-missing
```

### 详细输出

```bash
# 显示打印输出
pytest -s

# 显示变量
pytest -v

# 两者结合
pytest -sv
```

### 并行运行

```bash
pip install pytest-xdist
pytest -n auto
```

---

## 📊 测试覆盖率目标

| 模块 | 目标覆盖率 | 当前状态 |
|------|----------|--------|
| Models | >= 90% | 待测量 |
| Schemas | >= 85% | 待测量 |
| Security | >= 95% | 待测量 |
| API | >= 80% | 待测量 |
| Services | >= 85% | 待测量 |
| **总体** | **>= 85%** | **待测量** |

---

## 🧪 测试结构

### conftest.py 中的 Fixtures

#### 数据库 Fixtures
- `db_engine` - 测试数据库引擎
- `db_session` - 数据库会话

#### 工厂 Fixtures
- `user_factory` - 用户工厂
- `customer_factory` - 顾客工厂
- `category_factory` - 分类工厂
- `product_factory` - 产品工厂
- `employee_factory` - 员工工厂
- `order_factory` - 订单工厂

#### 测试数据 Fixtures
- `test_user` - 创建一个测试用户
- `test_customer` - 创建一个测试顾客
- `test_product` - 创建一个测试产品
- `test_category` - 创建一个测试分类
- `test_employee` - 创建一个测试员工
- `test_order` - 创建一个测试订单

---

## 📝 测试最佳实践

### 1. 使用 Fixtures

```python
async def test_example(db_session, test_user):
    """使用 fixtures 简化测试"""
    assert test_user.username == "testuser"
```

### 2. 异步测试

```python
@pytest.mark.asyncio
async def test_async_operation(db_session):
    """异步测试"""
    result = await some_async_function()
    assert result is not None
```

### 3. 异常测试

```python
def test_invalid_input():
    """测试异常处理"""
    with pytest.raises(ValidationError):
        UserCreate(username="user")  # 缺少必填字段
```

### 4. 测试组织

```python
@pytest.mark.asyncio
class TestUserModel:
    """相关测试组织在类中"""

    async def test_create_user(self):
        """测试创建用户"""
        pass

    async def test_update_user(self):
        """测试更新用户"""
        pass
```

---

## 🔧 故障排除

### 数据库错误

如果遇到 SQLite 锁定错误：
```bash
# 使用异步 SQLite 驱动
pip install aiosqlite
```

### 时区问题

如果测试中有时间戳问题：
```python
from datetime import datetime
import pytz

# 使用 UTC 时区
utc_now = datetime.now(pytz.UTC)
```

### 异步 IO 错误

如果遇到"no running event loop"错误：
- 确保使用 `@pytest.mark.asyncio` 装饰符
- 检查 `pytest.ini` 中的 `asyncio_mode = auto` 配置

---

## 📈 下一步

### 需要添加的测试

1. **更多 Schema 测试**
   - `tests/test_schemas/test_customer_schema.py`
   - `tests/test_schemas/test_product_schema.py`
   - `tests/test_schemas/test_order_schema.py`
   - `tests/test_schemas/test_employee_schema.py`

2. **服务层测试**
   - `tests/test_services/test_auth_service.py`
   - `tests/test_services/test_customer_service.py`
   - `tests/test_services/test_product_service.py`

3. **更多 API 端点测试**
   - 认证 API 端点
   - 顾客管理 API
   - 产品管理 API
   - 订单管理 API
   - 员工管理 API

4. **性能测试**
   - `tests/test_performance/test_query_performance.py`
   - `tests/test_performance/test_api_performance.py`

5. **E2E 测试**
   - 完整的业务流程测试

---

## 📚 参考资源

### Pytest
- [Pytest 官方文档](https://docs.pytest.org/)
- [Pytest Fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)

### 异步测试
- [Pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [FastAPI 测试](https://fastapi.tiangolo.com/tutorial/testing/)

### SQLAlchemy 异步
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)

---

## 🎯 测试命令快速参考

```bash
# 运行所有测试
pytest

# 运行并显示覆盖率
pytest --cov=app

# 生成 HTML 覆盖率报告
pytest --cov=app --cov-report=html

# 运行特定文件
pytest tests/test_models/test_user.py

# 运行并显示输出
pytest -s

# 详细模式
pytest -v

# 运行并立即停止在第一个失败
pytest -x

# 显示 10 个最慢的测试
pytest --durations=10

# 运行上次失败的测试
pytest --lf

# 运行特定标记的测试
pytest -m asyncio
```

---

**最后更新**: 2026-01-28
**作者**: DeepV Code AI
**状态**: 首轮测试框架完成
