# 养生店管理系统

一个完整的养生店管理解决方案，包含 Web 网页系统和微信小程序系统。

## 项目结构

```
wellness-shop-system/
├── backend/           # FastAPI 后端服务
├── frontend/          # Vue 3 Web 前端
├── miniprogram/       # 微信小程序
└── docs/             # 项目文档
```

## 功能模块

### 1. 顾客管理
- 顾客信息管理（会员/非会员）
- 顾客消费记录追踪
- 客户分层管理
- 会员卡管理

### 2. 产品管理
- 产品信息维护
- 产品分类管理
- 库存管理
- 产品定价（会员价/非会员价）

### 3. 订单管理
- 订单创建与管理
- 订单状态跟踪
- 支付管理（微信/支付宝）
- 发票管理

### 4. 员工管理
- 员工信息管理
- 员工权限管理
- 员工绩效统计
- 员工提成计算

### 5. 财务统计
- 实时营收统计
- 渠道分析（美团、抖音、微信小程序等）
- 客户消费分析
- 员工业绩排行

### 6. 系统配置
- 门店配置
- 用户权限管理
- 支付渠道配置

## 快速开始

### 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置数据库等信息

# 初始化数据库
alembic upgrade head

# 启动服务
uvicorn app.main:app --reload
```

服务将在 `http://localhost:8000` 启动，API 文档：`http://localhost:8000/docs`

### 前端启动

```bash
cd frontend

# 安装依赖
npm install
# 或 yarn install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

前端将在 `http://localhost:5173` 启动

### 小程序启动

```bash
cd miniprogram

# 使用微信开发者工具打开此目录
# 配置 app.json 中的 API 服务器地址
```

## 技术栈

### 后端
- **框架**: FastAPI 0.104+
- **数据库**: PostgreSQL 14+
- **ORM**: SQLAlchemy 2.0+
- **缓存**: Redis 7.0+
- **认证**: JWT
- **异步**: asyncio

### 前端
- **框架**: Vue 3
- **UI 库**: Element Plus
- **状态管理**: Pinia
- **构建工具**: Vite
- **图表**: ECharts

### 小程序
- **框架**: 微信小程序原生/Taro
- **UI**: Vant WeApp

## 开发指南

### 后端开发

1. **创建新的 API 端点**

```python
# app/api/v1/endpoints/example.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db

router = APIRouter(prefix="/example", tags=["Example"])

@router.get("/")
async def get_example(db: AsyncSession = Depends(get_db)):
    return {"message": "Example endpoint"}
```

2. **创建数据模型**

```python
# app/models/example.py
from sqlalchemy import Column, String
from app.db.base import Base, TimestampMixin, IDMixin

class ExampleModel(Base, IDMixin, TimestampMixin):
    __tablename__ = "examples"
    name = Column(String(255), nullable=False)
```

3. **创建请求/响应模式**

```python
# app/schemas/example.py
from pydantic import BaseModel

class ExampleSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
```

## API 文档

启动后端后，访问 `http://localhost:8000/docs` 查看完整的 API 文档。

## 部署

### Docker 部署

```bash
# 构建镜像
docker build -t wellness-shop:latest .

# 运行容器
docker run -p 8000:8000 wellness-shop:latest
```

## 贡献指南

欢迎提交 Pull Request 或报告 Issue。

## 许可证

MIT License

## 联系方式

项目维护者：[Your Name]
邮箱：[your email]
