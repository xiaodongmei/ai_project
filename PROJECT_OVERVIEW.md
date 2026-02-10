# 养生店管理系统 - 项目概览

## 项目简介

这是一个**完整的企业级养生店管理系统**，采用现代前后端分离架构。系统包含：

1. **Web 网页管理系统** - 员工端/管理员端的完整管理界面
2. **微信小程序** - 顾客端的购物和订单系统
3. **后端 API 服务** - FastAPI 构建的强大后端支撑

## 项目背景

根据提供的系统截图，系统需要支持：

- **顾客管理** - 会员等级、消费记录、卡券管理
- **产品管理** - 产品信息、分类、库存、定价
- **订单管理** - 订单创建、支付、状态跟踪、退货
- **员工管理** - 员工信息、职位、绩效统计
- **财务统计** - 实时营收、渠道分析、员工排行
- **系统配置** - 权限管理、门店配置

## 技术栈

### 后端 (Backend)

| 技术 | 版本 | 用途 |
|------|------|------|
| **FastAPI** | 0.104+ | Web 框架 |
| **Uvicorn** | 0.24+ | 应用服务器 |
| **PostgreSQL** | 14+ | 关系型数据库 |
| **SQLAlchemy** | 2.0+ | ORM 框架 |
| **Pydantic** | 2.5+ | 数据验证 |
| **python-jose** | 3.3+ | JWT 认证 |
| **passlib** | 1.7+ | 密码加密 |
| **Redis** | 7.0+ | 缓存（可选） |
| **pytest** | 7.4+ | 单元测试 |

### 前端 (Frontend)

| 技术 | 版本 | 用途 |
|------|------|------|
| **Vue** | 3.3+ | UI 框架 |
| **Vue Router** | 4.2+ | 路由管理 |
| **Pinia** | 2.1+ | 状态管理 |
| **Element Plus** | 2.4+ | UI 组件库 |
| **Axios** | 1.6+ | HTTP 客户端 |
| **ECharts** | 5.4+ | 数据可视化 |
| **Vite** | 5.0+ | 构建工具 |

### 小程序 (Mini Program)

| 技术 | 用途 |
|------|------|
| **微信小程序** | 应用框架 |
| **Vant WeApp** | UI 组件库 |

## 项目结构

```
wellness-shop-system/
│
├── backend/                     # FastAPI 后端服务
│   ├── app/
│   │   ├── models/             # 14 个数据库模型
│   │   ├── schemas/            # 22 个 Pydantic 模式
│   │   ├── api/v1/
│   │   │   └── endpoints/      # API 端点
│   │   ├── core/
│   │   │   ├── config.py       # 配置管理
│   │   │   ├── security.py     # 认证和安全
│   │   │   └── logging.py      # 日志配置
│   │   ├── db/
│   │   │   ├── database.py     # 数据库连接
│   │   │   └── base.py         # ORM 基类
│   │   ├── services/           # 业务逻辑层
│   │   ├── utils/              # 工具函数
│   │   └── main.py             # FastAPI 应用
│   ├── tests/                  # 单元测试
│   ├── init_db.py              # 数据库初始化脚本
│   ├── requirements.txt         # Python 依赖
│   └── .env.example            # 环境变量示例
│
├── frontend/                    # Vue 3 前端应用
│   ├── src/
│   │   ├── pages/              # 7 个页面组件
│   │   ├── components/         # 可复用组件
│   │   ├── router/             # Vue Router 配置
│   │   ├── store/              # Pinia 状态管理
│   │   ├── api/                # API 接口
│   │   ├── utils/              # 工具函数
│   │   ├── assets/             # 静态资源
│   │   ├── styles/             # 全局样式
│   │   ├── main.js             # 应用入口
│   │   └── App.vue             # 根组件
│   ├── index.html              # HTML 页面
│   ├── vite.config.js          # Vite 配置
│   ├── package.json            # npm 依赖
│   └── .eslintrc.cjs           # ESLint 配置
│
├── miniprogram/                # 微信小程序
│   ├── pages/                  # 各页面
│   │   ├── index/              # 首页（已实现）
│   │   ├── product/            # 产品
│   │   ├── order/              # 订单
│   │   ├── cart/               # 购物车
│   │   ├── profile/            # 个人中心
│   │   └── login/              # 登录
│   ├── components/             # 组件库
│   ├── api/                    # 接口调用
│   ├── utils/                  # 工具函数
│   ├── styles/                 # 样式
│   ├── app.js                  # 应用初始化
│   ├── app.json                # 应用配置
│   └── app.wxss                # 全局样式
│
└── docs/                       # 文档
    ├── README.md               # 项目说明
    ├── SETUP.md                # 初始化指南
    ├── DEVELOPMENT.md          # 开发指南
    ├── PROGRESS.md             # 进度总结
    ├── QUICKSTART.md           # 快速开始
    └── PROJECT_OVERVIEW.md     # 本文件
```

## 数据库设计

### 核心表结构 (14 个表)

#### 用户与认证
- **users** - 用户账户
  - 用户名、邮箱、密码、角色、权限

#### 顾客与销售
- **customers** - 顾客信息
  - 基本信息、会员等级、消费记录、账户余额
- **orders** - 订单
  - 订单号、金额、支付方式、状态、时间
- **order_items** - 订单明细
  - 产品、数量、价格、折扣
- **member_cards** - 会员卡
  - 卡号、余额、积分、有效期
- **payment_records** - 支付记录
  - 支付方式、交易号、金额、状态

#### 产品与库存
- **products** - 产品
  - 名称、分类、价格、库存、图片
- **product_categories** - 产品分类
  - 分类名称、描述、图标

#### 员工与绩效
- **employees** - 员工
  - 名称、岗位、部门、薪资、提成
- **employee_performance** - 员工绩效
  - 业绩、提成、订单数、客户数

#### 优惠与营销
- **discounts** - 优惠券
  - 优惠码、折扣、有效期

#### 统计与分析
- **daily_statistics** - 每日统计
  - 营收、订单数、客户数、客流量
- **channel_statistics** - 渠道统计
  - 渠道、订单数、收入、客户数
- **product_sales** - 产品销售统计
  - 产品、销售数量、销售额

## 已实现的功能

### 后端 ✓
- [x] 完整的数据库设计（14 个表）
- [x] 数据验证模式（22 个 Pydantic 模式）
- [x] FastAPI 应用框架
- [x] 数据库 ORM 配置
- [x] JWT 认证和密码加密
- [x] CORS 跨域支持
- [x] 日志系统
- [x] API 文档自动生成（Swagger）
- [x] 数据库初始化脚本

### 前端 ✓
- [x] Vue 3 项目配置
- [x] Vite 构建工具
- [x] Vue Router 路由系统
- [x] Pinia 状态管理
- [x] Axios HTTP 客户端
- [x] 7 个页面框架
- [x] 路由保护和认证
- [x] ESLint 代码检查

### 小程序 ✓
- [x] 微信小程序配置
- [x] 应用初始化框架
- [x] HTTP 请求工具库
- [x] 通用工具函数库
- [x] 首页基础实现（轮播图、分类、产品）

## 待实现的功能

### 后端 API 端点
- [ ] 认证接口（登录、刷新、登出）
- [ ] 用户接口（CRUD）
- [ ] 顾客接口（CRUD、统计）
- [ ] 产品接口（CRUD、搜索、分类）
- [ ] 订单接口（CRUD、支付、统计）
- [ ] 员工接口（CRUD、绩效）
- [ ] 统计接口（仪表板、报表）

### 前端页面
- [ ] 登录页面（完全实现）
- [ ] 仪表板（数据展示、图表）
- [ ] 顾客管理（列表、详情、编辑）
- [ ] 产品管理（列表、编辑、库存）
- [ ] 订单管理（列表、详情、状态）
- [ ] 员工管理（列表、绩效）
- [ ] 统计分析（报表、图表）
- [ ] 公共组件（Header、Sidebar、Table）

### 小程序页面
- [ ] 登录页面
- [ ] 产品列表和详情
- [ ] 购物车功能
- [ ] 下单流程
- [ ] 订单管理
- [ ] 个人中心
- [ ] 支付集成

## 快速启动

### 1. 后端启动

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，配置 PostgreSQL 数据库地址

# 初始化数据库
python init_db.py

# 启动服务
uvicorn app.main:app --reload
```

**访问**:
- API: http://localhost:8000
- 文档: http://localhost:8000/docs

### 2. 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

**访问**:
- 前端: http://localhost:5173

### 3. 小程序启动

```bash
# 用微信开发者工具打开 miniprogram 目录
# 修改 app.js 中的 apiUrl 指向后端
```

## API 设计

### RESTful API 结构

```
/api/v1/
├── auth/                 # 认证
│   ├── POST /login
│   ├── POST /refresh
│   └── POST /logout
├── users/               # 用户
│   ├── GET /
│   ├── GET /{id}
│   ├── POST /
│   ├── PUT /{id}
│   └── DELETE /{id}
├── customers/          # 顾客
│   ├── GET /
│   ├── GET /{id}
│   ├── POST /
│   ├── PUT /{id}
│   └── DELETE /{id}
├── products/           # 产品
│   ├── GET /
│   ├── GET /{id}
│   ├── POST /
│   ├── PUT /{id}
│   └── DELETE /{id}
├── orders/             # 订单
│   ├── GET /
│   ├── GET /{id}
│   ├── POST /
│   ├── PUT /{id}
│   └── DELETE /{id}
├── employees/          # 员工
│   ├── GET /
│   ├── GET /{id}
│   ├── POST /
│   ├── PUT /{id}
│   └── DELETE /{id}
└── statistics/         # 统计
    ├── GET /dashboard
    ├── GET /daily
    ├── GET /revenue
    ├── GET /channels
    ├── GET /employees/performance
    └── GET /products/sales
```

## 项目特性

### 架构特性
- ✓ **前后端分离** - 清晰的架构边界
- ✓ **异步处理** - FastAPI 异步支持
- ✓ **数据验证** - Pydantic 自动验证
- ✓ **认证授权** - JWT token 机制
- ✓ **日志记录** - 完整的日志系统
- ✓ **错误处理** - 统一的错误响应

### 开发特性
- ✓ **自动文档** - Swagger/ReDoc 自动生成
- ✓ **代码检查** - ESLint/Flake8/Black
- ✓ **测试框架** - pytest 单元测试
- ✓ **数据库迁移** - Alembic 数据库版本控制
- ✓ **热重载** - 开发时自动重启

### 业务特性
- ✓ **完整的数据模型** - 覆盖所有业务场景
- ✓ **多角色支持** - Admin/Employee/Customer
- ✓ **统计分析** - 多维度数据分析
- ✓ **渠道管理** - 支持多个销售渠道
- ✓ **绩效管理** - 员工绩效追踪

## 开发工作流

### 1. 后端开发

```
编写模型 → 创建 schema → 实现 API → 测试
```

### 2. 前端开发

```
设计页面 → 编写组件 → 集成 API → 测试
```

### 3. 小程序开发

```
设计页面 → 编写 wxml → 实现逻辑 → 测试
```

## 部署建议

### 后端部署
- 使用 Docker 容器化
- Gunicorn + Uvicorn 应用服务器
- Nginx 反向代理
- PostgreSQL 数据库
- Redis 缓存（可选）

### 前端部署
- 构建: `npm run build`
- 上传 dist 文件夹
- Nginx 静态文件服务
- 启用 HTTPS

### 小程序发布
- 上传至微信公众平台
- 配置服务器地址
- 申请权限
- 提交审核

## 文档

| 文档 | 说明 |
|------|------|
| README.md | 项目总体说明 |
| QUICKSTART.md | 5 分钟快速启动 |
| SETUP.md | 项目初始化指南 |
| DEVELOPMENT.md | 详细开发指南 |
| PROGRESS.md | 项目进度总结 |
| PROJECT_OVERVIEW.md | 本文件 |

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交代码
4. 发起 Pull Request

## 许可证

MIT License

## 联系方式

项目维护者: [Your Name]
邮箱: [Your Email]

---

**项目完成度**: 约 30%
**下一个里程碑**: 完成前端登录和仪表板（预计 1-2 周）
**项目状态**: 🚀 积极开发中

---

*最后更新: 2026-01-28*
