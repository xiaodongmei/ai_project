# 养生店管理系统 - 开发指南

## 项目状态

✓ 第一步：项目初始化完成
✓ 第二步：FastAPI 后端框架搭建完成
- 第三步：Vue Web 前端开发（接下来）
- 第四步：微信小程序开发（之后）

---

## 当前已完成的工作

### 后端 (Backend)

#### 数据模型 (Models)
已创建以下数据模型：
- **User** - 用户模型
- **Customer** - 顾客模型
- **Product** - 产品模型
- **ProductCategory** - 产品分类
- **Employee** - 员工模型
- **Order** - 订单模型
- **OrderItem** - 订单项目
- **PaymentRecord** - 支付记录
- **MemberCard** - 会员卡
- **Discount** - 优惠券
- **DailyStatistics** - 每日统计
- **ChannelStatistics** - 渠道统计
- **EmployeePerformance** - 员工绩效
- **ProductSales** - 产品销售

#### Pydantic 模式 (Schemas)
已创建所有数据模型对应的 Pydantic 模式用于请求/响应验证：
- User schemas (Create, Update, Response)
- Customer schemas
- Product schemas
- Order schemas
- Employee schemas
- Statistics schemas

#### 核心配置
- `config.py` - 应用配置管理
- `security.py` - 认证和安全工具
- `logging.py` - 日志配置
- `database.py` - 数据库连接管理

#### API 框架
- `main.py` - FastAPI 主应用程序
- 健康检查端点已实现
- CORS 中间件已配置
- 路由结构已准备

### 前端 (Frontend)

#### 基础配置
- `vite.config.js` - Vite 构建配置
- `package.json` - 项目依赖
- `.eslintrc.cjs` - ESLint 配置

#### Vue 应用结构
- `main.js` - 应用入口
- `App.vue` - 根组件
- `router/index.js` - 路由配置

#### Pinia 状态管理
- `store/user.js` - 用户状态管理

#### API 客户端
- `api/client.js` - Axios HTTP 客户端

#### 页面组件（占位符）
- Login.vue - 登录页
- Dashboard.vue - 仪表板
- Customers.vue - 顾客管理
- Products.vue - 产品管理
- Orders.vue - 订单管理
- Employees.vue - 员工管理
- Statistics.vue - 统计页面

### 小程序 (Mini Program)

#### 基础配置
- `app.json` - 小程序配置
- `app.js` - 应用初始化
- `app.wxss` - 全局样式

#### 工具函数
- `utils/request.js` - HTTP 请求工具
- `utils/util.js` - 通用工具函数

#### 首页实现
- `pages/index/index.js` - 首页逻辑
- `pages/index/index.wxml` - 首页模板
- `pages/index/index.wxss` - 首页样式

---

## 下一步开发计划

### 第三步：Vue Web 前端详细开发

#### 3.1 登录页面实现
- 用户名/邮箱 + 密码登录
- 记住账号功能
- 错误提示
- Token 保存

#### 3.2 仪表板页面
根据截图实现：
- 店铺营收（¥829.80）
- 店铺实收（¥802.32）
- 会员充值（¥295.06）
- 有效订单数（13）
- 项目总数（12）
- 客流量（13人）
- 渠道分布（美团券 42%、抖音券 8%等）
- 员工绩效榜单
- 收益分布图表

#### 3.3 顾客管理页面
实现功能：
- 顾客列表（搜索、筛选）
- 顾客详情查看
- 新增顾客
- 编辑顾客信息
- 删除顾客

#### 3.4 产品管理页面
实现功能：
- 产品列表展示
- 分类管理
- 新增产品
- 编辑产品
- 删除产品
- 库存管理

#### 3.5 订单管理页面
实现功能：
- 订单列表（按状态筛选）
- 订单详情
- 订单状态更新
- 支付管理
- 退单处理

#### 3.6 员工管理页面
实现功能：
- 员工列表
- 员工详情
- 新增员工
- 编辑员工
- 员工状态管理
- 绩效查看

#### 3.7 统计分析页面
实现功能：
- 日期范围选择
- 收入统计图表
- 客流量统计
- 渠道分布分析
- 员工排行榜
- 产品销售排名

#### 3.8 公共组件开发
- Header/Navbar - 顶部导航
- Sidebar - 左侧菜单
- Pagination - 分页
- SearchForm - 搜索表单
- Table - 数据表格
- Modal - 对话框
- Message - 消息提示
- Loading - 加载中

#### 3.9 样式和主题
- 全局样式设置
- Element Plus 主题定制
- 响应式设计
- 暗色模式支持（可选）

### 第四步：微信小程序开发

#### 4.1 登录认证
- 微信登录
- Token 管理
- 登录状态保持

#### 4.2 首页完整实现
- 轮播图
- 分类导航
- 热销产品
- 推荐产品

#### 4.3 产品模块
- 产品列表
- 产品搜索
- 产品详情
- 产品评价

#### 4.4 购物车模块
- 添加到购物车
- 购物车列表
- 数量修改
- 删除商品
- 购物车统计

#### 4.5 订单模块
- 下单流程
- 订单列表
- 订单详情
- 订单取消/退货
- 订单评价

#### 4.6 个人中心
- 个人信息
- 收货地址
- 订单历史
- 卡券管理
- 帮助中心

---

## 数据库初始化

### 1. 创建 PostgreSQL 数据库

```sql
CREATE DATABASE wellness_shop;
```

### 2. 初始化数据表

```bash
cd backend
python init_db.py
```

### 3. 验证连接

在 `.env` 文件中配置数据库地址：
```
DATABASE_URL=postgresql://username:password@localhost:5432/wellness_shop
```

---

## 运行项目

### 启动后端

```bash
cd backend

# 1. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 文件配置数据库等

# 4. 初始化数据库
python init_db.py

# 5. 启动 FastAPI 服务
uvicorn app.main:app --reload
```

服务将在 `http://localhost:8000` 启动
- API 文档: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 启动前端

```bash
cd frontend

# 1. 安装依赖
npm install
# 或 yarn install

# 2. 启动开发服务器
npm run dev
# 或 yarn dev
```

前端将在 `http://localhost:5173` 启动

### 启动小程序

```bash
# 用微信开发者工具打开 miniprogram 目录
# 修改 app.js 中的 apiUrl 指向后端服务
```

---

## API 接口规划

### 认证接口
- `POST /auth/login` - 用户登录
- `POST /auth/refresh` - 刷新令牌
- `POST /auth/logout` - 用户登出

### 用户接口
- `GET /users/profile` - 获取用户信息
- `PUT /users/profile` - 更新用户信息
- `POST /users` - 创建用户（仅管理员）
- `PUT /users/{id}` - 更新用户
- `DELETE /users/{id}` - 删除用户

### 顾客接口
- `GET /customers` - 顾客列表
- `GET /customers/{id}` - 顾客详情
- `POST /customers` - 新增顾客
- `PUT /customers/{id}` - 更新顾客
- `DELETE /customers/{id}` - 删除顾客

### 产品接口
- `GET /products` - 产品列表
- `GET /products/{id}` - 产品详情
- `POST /products` - 新增产品
- `PUT /products/{id}` - 更新产品
- `DELETE /products/{id}` - 删除产品
- `GET /categories` - 产品分类列表

### 订单接口
- `GET /orders` - 订单列表
- `GET /orders/{id}` - 订单详情
- `POST /orders` - 创建订单
- `PUT /orders/{id}` - 更新订单
- `DELETE /orders/{id}` - 删除订单
- `POST /orders/{id}/payment` - 支付

### 员工接口
- `GET /employees` - 员工列表
- `GET /employees/{id}` - 员工详情
- `POST /employees` - 新增员工
- `PUT /employees/{id}` - 更新员工
- `DELETE /employees/{id}` - 删除员工

### 统计接口
- `GET /statistics/dashboard` - 仪表板数据
- `GET /statistics/daily` - 日统计
- `GET /statistics/revenue` - 收入统计
- `GET /statistics/channels` - 渠道分析
- `GET /statistics/employees/performance` - 员工绩效
- `GET /statistics/products/sales` - 产品销售

---

## 代码规范

### Python (后端)
- 遵循 PEP 8 规范
- 使用 Black 格式化代码
- 使用 Flake8 检查代码质量
- 使用 isort 整理导入

```bash
black app/
flake8 app/
isort app/
```

### JavaScript/Vue (前端)
- 遵循 Airbnb 规范
- 使用 ESLint 检查代码
- 使用 Prettier 格式化代码

```bash
npm run lint  # ESLint
npm run format  # Prettier
```

---

## 常见问题

### Q: 如何修改数据库配置？
A: 编辑 `backend/.env` 文件中的 `DATABASE_URL`

### Q: 如何添加新的 API 端点？
A:
1. 在 `app/models/` 中创建数据模型
2. 在 `app/schemas/` 中创建 Pydantic 模式
3. 在 `app/api/v1/endpoints/` 中创建路由文件
4. 在 `app/api/v1/routers.py` 中注册路由

### Q: 如何部署到生产环境？
A: 参考项目根目录的 `DEPLOYMENT.md` 文件（待创建）

---

## 相关文档

- [README.md](./README.md) - 项目概述
- [SETUP.md](./SETUP.md) - 初始化指南
- 后端 API 文档: `http://localhost:8000/docs` (Swagger)

---

继续开发第三步：Vue Web 前端详细实现吗？
