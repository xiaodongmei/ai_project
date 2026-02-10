# 项目初始化指南

## 第一步：初始化项目结构（已完成 ✓）

项目基础目录和配置文件已创建完成。

### 创建的内容：

#### 后端 (Backend)
```
backend/
├── app/
│   ├── api/v1/endpoints/     # API 端点
│   ├── models/               # 数据模型
│   ├── schemas/              # 请求/响应模式
│   ├── services/             # 业务逻辑
│   ├── core/                 # 核心配置
│   │   ├── config.py         # 应用配置
│   │   └── logging.py        # 日志配置
│   ├── db/                   # 数据库
│   │   ├── database.py       # 数据库连接
│   │   └── base.py           # 基础模型
│   └── utils/                # 工具函数
├── tests/                    # 测试
├── logs/                     # 日志
├── requirements.txt          # Python 依赖
├── .env.example             # 环境变量示例
└── main.py                  # 应用入口（待创建）
```

#### 前端 (Frontend)
```
frontend/
├── src/
│   ├── components/           # 可复用组件
│   ├── pages/               # 页面组件
│   ├── views/               # 视图组件
│   ├── layouts/             # 布局组件
│   ├── store/               # Pinia 状态管理
│   ├── api/                 # API 接口
│   ├── utils/               # 工具函数
│   ├── assets/              # 静态资源
│   └── styles/              # 样式文件
├── public/                  # 公共文件
├── vite.config.js          # Vite 配置
├── package.json            # 依赖配置
└── .eslintrc.cjs          # ESLint 配置
```

#### 小程序 (Miniprogram)
```
miniprogram/
├── pages/                   # 页面
│   ├── index/              # 首页
│   ├── product/            # 产品
│   ├── order/              # 订单
│   ├── cart/               # 购物车
│   ├── profile/            # 个人中心
│   └── login/              # 登录
├── components/             # 组件
├── api/                    # API 接口
├── utils/                  # 工具函数
│   ├── request.js         # HTTP 请求工具
│   └── util.js            # 通用工具
├── styles/                # 全局样式
├── images/                # 图片资源
├── app.js                 # 应用主文件
├── app.json               # 应用配置
└── app.wxss              # 应用样式
```

---

## 第二步：搭建 FastAPI 后端（接下来）

将创建：
1. ✓ 数据库模型（User, Customer, Product, Order 等）
2. ✓ Pydantic 模式定义
3. ✓ API 路由和端点
4. ✓ 业务逻辑层（Service）
5. ✓ 数据库迁移脚本
6. ✓ 主应用文件（main.py）

### 后端技术栈
- FastAPI 0.104+ - Web 框架
- SQLAlchemy 2.0+ - ORM
- PostgreSQL - 数据库
- Pydantic - 数据验证
- JWT - 认证
- Redis - 缓存

---

## 第三步：开发 Vue Web 前端（之后）

将创建：
1. ✓ Vue Router 路由配置
2. ✓ Pinia 状态管理
3. ✓ HTTP 客户端（axios）
4. ✓ 页面组件
5. ✓ Element Plus UI 集成

### 前端页面
- 登录页面
- 仪表盘（数据统计）
- 顾客管理
- 产品管理
- 订单管理
- 员工管理
- 财务统计

---

## 第四步：开发微信小程序（最后）

将创建：
1. ✓ 小程序页面
2. ✓ 组件库
3. ✓ 数据绑定
4. ✓ 支付集成

### 小程序页面
- 登录页面
- 首页
- 产品列表
- 产品详情
- 购物车
- 订单列表
- 个人中心

---

## 快速开始命令

### 后端初始化
```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 复制环境配置
cp .env.example .env

# 修改 .env 配置数据库和其他参数
# 然后初始化数据库和启动服务
```

### 前端初始化
```bash
cd frontend

# 安装依赖
npm install
# 或 yarn install

# 启动开发服务器
npm run dev
```

### 小程序
```bash
# 使用微信开发者工具打开 miniprogram 目录
# 修改 app.js 中的 apiUrl 指向后端服务
```

---

## 环境要求

### 后端
- Python 3.9+
- PostgreSQL 14+
- Redis 7.0+（可选，用于缓存）

### 前端
- Node.js 16+
- npm 8+ 或 yarn 3+

### 小程序
- 微信开发者工具
- 微信小程序账号

---

## 下一步

继续按照步骤进行开发：

1. ✓ **项目初始化** - 完成
2. **搭建 FastAPI 后端** - 接下来
   - 创建数据库模型
   - 创建 API 端点
   - 实现业务逻辑
3. **开发 Vue Web 前端**
4. **开发微信小程序**

准备好开始第二步了吗？
