# API 文档

养生店管理系统完整 API 文档。基于 FastAPI 和 OpenAPI 3.0 规范。

## 目录

1. [快速开始](#快速开始)
2. [认证](#认证)
3. [API 端点](#api-端点)
4. [错误处理](#错误处理)
5. [请求示例](#请求示例)
6. [状态码](#状态码)
7. [数据类型](#数据类型)

---

## 快速开始

### 访问 API 文档

启动后端服务后，可通过以下方式查看 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### API 基础 URL

```
http://localhost:8000/api/v1  # 开发环境
https://api.example.com/api/v1  # 生产环境
```

### 通用请求头

所有请求应包含以下通用头：

```
Content-Type: application/json
Authorization: Bearer <your-jwt-token>  # 受保护的端点需要
```

---

## 认证

### JWT 认证流程

1. **获取 Token**（登录）
2. **在请求头中使用 Token**
3. **Token 过期时刷新**

### 登录端点

#### POST `/api/v1/auth/login`

使用用户名和密码登录。

**请求体：**
```json
{
  "username": "admin",
  "password": "your-password"
}
```

**响应（200 OK）：**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "role": "admin"
  }
}
```

**curl 示例：**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "your-password"
  }'
```

### 使用 Token

在所有受保护的请求中，在 Authorization 头中包含 token：

```bash
curl -X GET http://localhost:8000/api/v1/customers \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Token 刷新

#### POST `/api/v1/auth/refresh`

**请求头：**
```
Authorization: Bearer <expired-token>
```

**响应（200 OK）：**
```json
{
  "access_token": "new-token-here",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### 登出

#### POST `/api/v1/auth/logout`

**请求头：**
```
Authorization: Bearer <your-token>
```

**响应（200 OK）：**
```json
{
  "message": "Logged out successfully"
}
```

---

## API 端点

### 健康检查

#### GET `/health`

检查服务健康状态。

**响应（200 OK）：**
```json
{
  "status": "ok",
  "app": "wellness-shop-system",
  "version": "1.0.0"
}
```

### 认证相关 (Auth)

所有端点前缀：`/api/v1/auth`

| 方法 | 端点 | 说明 | 认证 |
|------|------|------|------|
| POST | `/login` | 用户登录 | ❌ |
| POST | `/register` | 用户注册 | ❌ |
| POST | `/refresh` | 刷新 Token | ✅ |
| POST | `/logout` | 用户登出 | ✅ |
| GET | `/me` | 获取当前用户信息 | ✅ |
| POST | `/change-password` | 修改密码 | ✅ |

### 顾客管理 (Customers)

所有端点前缀：`/api/v1/customers`

#### 列表查询

```http
GET /api/v1/customers
```

**查询参数：**
```
skip: 0           # 跳过记录数（分页）
limit: 10         # 限制返回数
search: "name"    # 搜索字段
sort_by: "name"   # 排序字段
order: "asc"      # 排序顺序（asc/desc）
status: "active"  # 筛选状态
```

**响应示例：**
```json
{
  "total": 100,
  "page": 1,
  "limit": 10,
  "items": [
    {
      "id": 1,
      "name": "张三",
      "phone": "13800138000",
      "email": "zhangsan@example.com",
      "membership_status": "vip",
      "total_consumption": 5000.00,
      "created_at": "2024-01-01T10:00:00",
      "updated_at": "2024-01-15T10:00:00"
    }
  ]
}
```

#### 创建顾客

```http
POST /api/v1/customers
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "李四",
  "phone": "13900139000",
  "email": "lisi@example.com",
  "membership_status": "regular",
  "address": "北京市朝阳区",
  "notes": "VIP 客户"
}
```

**响应（201 Created）：**
```json
{
  "id": 101,
  "name": "李四",
  "phone": "13900139000",
  "email": "lisi@example.com",
  "membership_status": "regular",
  "address": "北京市朝阳区",
  "notes": "VIP 客户",
  "total_consumption": 0,
  "created_at": "2024-01-16T10:00:00"
}
```

#### 获取单个顾客

```http
GET /api/v1/customers/{customer_id}
Authorization: Bearer <token>
```

**响应（200 OK）：**
```json
{
  "id": 1,
  "name": "张三",
  "phone": "13800138000",
  "email": "zhangsan@example.com",
  "membership_status": "vip",
  "address": "上海市浦东新区",
  "notes": "长期客户",
  "total_consumption": 5000.00,
  "orders_count": 10,
  "last_order_date": "2024-01-15T10:00:00",
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-15T10:00:00"
}
```

#### 更新顾客

```http
PUT /api/v1/customers/{customer_id}
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "张三（已更新）",
  "phone": "13800138000",
  "email": "zhangsan.new@example.com",
  "membership_status": "vip",
  "notes": "更新的备注"
}
```

**响应（200 OK）：**
```json
{
  "id": 1,
  "name": "张三（已更新）",
  "phone": "13800138000",
  "email": "zhangsan.new@example.com",
  "membership_status": "vip",
  "updated_at": "2024-01-16T10:00:00"
}
```

#### 删除顾客

```http
DELETE /api/v1/customers/{customer_id}
Authorization: Bearer <token>
```

**响应（204 No Content）：**
```
(empty response)
```

### 产品管理 (Products)

所有端点前缀：`/api/v1/products`

#### 列表查询

```http
GET /api/v1/products?skip=0&limit=10&category=spa&status=active
```

**查询参数：**
```
skip: 0           # 分页偏移
limit: 10         # 每页数量
category: "spa"   # 产品分类
status: "active"  # 状态筛选
search: "name"    # 搜索
sort_by: "price"  # 排序字段
order: "asc"      # 排序顺序
```

**响应示例：**
```json
{
  "total": 50,
  "items": [
    {
      "id": 1,
      "name": "足部按摩服务",
      "category": "massage",
      "description": "专业足部按摩",
      "price": 88.00,
      "member_price": 68.00,
      "stock": 100,
      "status": "active",
      "image_url": "https://example.com/image.jpg",
      "created_at": "2024-01-01T10:00:00"
    }
  ]
}
```

#### 创建产品

```http
POST /api/v1/products
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "新产品",
  "category": "spa",
  "description": "产品描述",
  "price": 99.99,
  "member_price": 79.99,
  "stock": 50,
  "status": "active",
  "image_url": "https://example.com/image.jpg"
}
```

**响应（201 Created）：**
```json
{
  "id": 51,
  "name": "新产品",
  "category": "spa",
  ...
}
```

### 订单管理 (Orders)

所有端点前缀：`/api/v1/orders`

#### 列表查询

```http
GET /api/v1/orders?status=completed&skip=0&limit=20
```

**查询参数：**
```
status: "completed"  # 订单状态（pending, processing, completed, cancelled）
customer_id: 1       # 顾客 ID
skip: 0              # 分页
limit: 20            # 每页数量
start_date: "2024-01-01"  # 开始日期
end_date: "2024-01-31"    # 结束日期
```

**响应示例：**
```json
{
  "total": 25,
  "items": [
    {
      "id": 1001,
      "customer_id": 1,
      "customer_name": "张三",
      "order_date": "2024-01-15T10:00:00",
      "total_amount": 500.00,
      "status": "completed",
      "payment_method": "wechat",
      "items": [
        {
          "product_id": 1,
          "product_name": "足部按摩服务",
          "quantity": 1,
          "unit_price": 88.00,
          "subtotal": 88.00
        }
      ],
      "created_at": "2024-01-15T10:00:00"
    }
  ]
}
```

#### 创建订单

```http
POST /api/v1/orders
Content-Type: application/json
Authorization: Bearer <token>

{
  "customer_id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "unit_price": 88.00
    }
  ],
  "payment_method": "wechat",
  "notes": "订单备注"
}
```

**响应（201 Created）：**
```json
{
  "id": 1001,
  "customer_id": 1,
  "total_amount": 176.00,
  "status": "pending",
  "order_date": "2024-01-16T10:00:00",
  "created_at": "2024-01-16T10:00:00"
}
```

#### 获取订单详情

```http
GET /api/v1/orders/{order_id}
Authorization: Bearer <token>
```

#### 更新订单状态

```http
PATCH /api/v1/orders/{order_id}
Content-Type: application/json
Authorization: Bearer <token>

{
  "status": "completed"
}
```

**状态流转：**
```
pending → processing → completed
  ↓
  └─→ cancelled
```

### 员工管理 (Employees)

所有端点前缀：`/api/v1/employees`

#### 列表查询

```http
GET /api/v1/employees?department=massage&status=active
```

**查询参数：**
```
department: "massage"  # 部门
status: "active"       # 状态
role: "therapist"      # 职位
search: "name"         # 搜索
```

**响应示例：**
```json
{
  "total": 15,
  "items": [
    {
      "id": 1,
      "name": "王五",
      "employee_id": "EMP001",
      "department": "massage",
      "position": "therapist",
      "phone": "13700137000",
      "email": "wangwu@example.com",
      "status": "active",
      "hire_date": "2023-01-01",
      "performance_rating": 4.5,
      "commission_rate": 0.1,
      "created_at": "2023-01-01T10:00:00"
    }
  ]
}
```

#### 创建员工

```http
POST /api/v1/employees
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "赵六",
  "employee_id": "EMP016",
  "department": "massage",
  "position": "therapist",
  "phone": "13600136000",
  "email": "zhaoliu@example.com",
  "hire_date": "2024-01-01",
  "commission_rate": 0.1
}
```

### 统计分析 (Statistics)

所有端点前缀：`/api/v1/statistics`

#### 收入统计

```http
GET /api/v1/statistics/revenue?date_range=month&start_date=2024-01-01&end_date=2024-01-31
```

**查询参数：**
```
date_range: "day|week|month|year"
start_date: "2024-01-01"
end_date: "2024-01-31"
```

**响应示例：**
```json
{
  "total_revenue": 50000.00,
  "order_count": 100,
  "average_order_value": 500.00,
  "data": [
    {
      "date": "2024-01-01",
      "revenue": 1000.00,
      "order_count": 2
    }
  ],
  "period": "2024-01"
}
```

#### 顾客统计

```http
GET /api/v1/statistics/customers?metrics=total,active,new
```

**响应示例：**
```json
{
  "total_customers": 500,
  "active_customers": 450,
  "new_customers": 20,
  "member_count": 200,
  "average_consumption": 1000.00,
  "member_ratio": 0.4
}
```

#### 产品销售排行

```http
GET /api/v1/statistics/product-sales?limit=10&order=desc
```

**响应示例：**
```json
{
  "data": [
    {
      "product_id": 1,
      "product_name": "足部按摩服务",
      "sales_count": 200,
      "revenue": 17600.00,
      "rank": 1
    }
  ]
}
```

#### 员工业绩统计

```http
GET /api/v1/statistics/employee-performance?start_date=2024-01-01&end_date=2024-01-31
```

**响应示例：**
```json
{
  "data": [
    {
      "employee_id": 1,
      "employee_name": "王五",
      "total_sales": 10000.00,
      "commission": 1000.00,
      "customer_count": 50,
      "rating": 4.8
    }
  ]
}
```

---

## 错误处理

### 错误响应格式

所有错误响应遵循统一格式：

```json
{
  "detail": "错误描述信息",
  "error_code": "ERROR_CODE",
  "timestamp": "2024-01-16T10:00:00"
}
```

### 常见错误

#### 400 Bad Request

请求参数不合法或格式错误。

```json
{
  "detail": "Invalid email format",
  "error_code": "INVALID_REQUEST"
}
```

#### 401 Unauthorized

未提供或无效的认证凭据。

```json
{
  "detail": "Missing or invalid authentication credentials",
  "error_code": "UNAUTHORIZED"
}
```

#### 403 Forbidden

有效的认证但无权限访问该资源。

```json
{
  "detail": "Insufficient permissions",
  "error_code": "FORBIDDEN"
}
```

#### 404 Not Found

请求的资源不存在。

```json
{
  "detail": "Customer not found",
  "error_code": "NOT_FOUND"
}
```

#### 409 Conflict

资源冲突（如重复的唯一字段）。

```json
{
  "detail": "Email already exists",
  "error_code": "CONFLICT"
}
```

#### 422 Unprocessable Entity

请求体验证失败。

```json
{
  "detail": [
    {
      "loc": ["body", "price"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

#### 500 Internal Server Error

服务器内部错误。

```json
{
  "detail": "Internal server error",
  "error_code": "INTERNAL_ERROR"
}
```

---

## 请求示例

### Python - requests

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# 登录
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={
        "username": "admin",
        "password": "password"
    }
)
token = response.json()["access_token"]

# 创建请求头
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# 获取顾客列表
response = requests.get(
    f"{BASE_URL}/customers?skip=0&limit=10",
    headers=headers
)
customers = response.json()
print(customers)

# 创建顾客
response = requests.post(
    f"{BASE_URL}/customers",
    headers=headers,
    json={
        "name": "新顾客",
        "phone": "13900139000",
        "email": "customer@example.com",
        "membership_status": "regular"
    }
)
new_customer = response.json()
print(new_customer)
```

### JavaScript - fetch

```javascript
const BASE_URL = "http://localhost:8000/api/v1";

// 登录
async function login() {
  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: "admin",
      password: "password"
    })
  });
  return await response.json();
}

// 获取顾客列表
async function getCustomers(token) {
  const response = await fetch(`${BASE_URL}/customers?skip=0&limit=10`, {
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json"
    }
  });
  return await response.json();
}

// 创建顾客
async function createCustomer(token, data) {
  const response = await fetch(`${BASE_URL}/customers`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });
  return await response.json();
}

// 使用示例
async function main() {
  const loginResponse = await login();
  const token = loginResponse.access_token;

  const customers = await getCustomers(token);
  console.log(customers);

  const newCustomer = await createCustomer(token, {
    name: "新顾客",
    phone: "13900139000",
    email: "customer@example.com",
    membership_status: "regular"
  });
  console.log(newCustomer);
}

main();
```

### cURL

```bash
# 登录
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}' \
  | jq -r '.access_token')

# 获取顾客列表
curl -X GET "http://localhost:8000/api/v1/customers?skip=0&limit=10" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"

# 创建顾客
curl -X POST http://localhost:8000/api/v1/customers \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "新顾客",
    "phone": "13900139000",
    "email": "customer@example.com",
    "membership_status": "regular"
  }'
```

---

## 状态码

| 状态码 | 说明 |
|--------|------|
| 200 | OK - 请求成功 |
| 201 | Created - 资源创建成功 |
| 204 | No Content - 请求成功但无返回内容 |
| 400 | Bad Request - 请求参数错误 |
| 401 | Unauthorized - 认证失败或过期 |
| 403 | Forbidden - 无权限访问 |
| 404 | Not Found - 资源不存在 |
| 409 | Conflict - 资源冲突 |
| 422 | Unprocessable Entity - 请求体验证失败 |
| 500 | Internal Server Error - 服务器错误 |
| 502 | Bad Gateway - 网关错误 |
| 503 | Service Unavailable - 服务不可用 |

---

## 数据类型

### 常用数据类型

#### 顾客对象

```json
{
  "id": 1,
  "name": "string",
  "phone": "string",
  "email": "string",
  "membership_status": "regular|vip|platinum",
  "address": "string",
  "notes": "string",
  "total_consumption": 0.00,
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T10:00:00"
}
```

#### 产品对象

```json
{
  "id": 1,
  "name": "string",
  "category": "string",
  "description": "string",
  "price": 0.00,
  "member_price": 0.00,
  "stock": 0,
  "status": "active|inactive",
  "image_url": "string",
  "created_at": "2024-01-01T10:00:00"
}
```

#### 订单对象

```json
{
  "id": 1,
  "customer_id": 1,
  "order_date": "2024-01-01T10:00:00",
  "total_amount": 0.00,
  "status": "pending|processing|completed|cancelled",
  "payment_method": "cash|wechat|alipay",
  "items": [
    {
      "product_id": 1,
      "product_name": "string",
      "quantity": 1,
      "unit_price": 0.00,
      "subtotal": 0.00
    }
  ],
  "notes": "string",
  "created_at": "2024-01-01T10:00:00"
}
```

---

## 速率限制

目前未启用速率限制，建议生产环境配置：

- 每个 IP 每分钟 1000 个请求
- 每个用户每分钟 500 个请求

---

## 版本控制

当前 API 版本：**v1**

未来的重大更新将使用新的版本号（如 `/api/v2`）。旧版本将保持向后兼容。

---

## 参考资源

- [OpenAPI 规范](https://swagger.io/specification/)
- [REST API 最佳实践](https://restfulapi.net/)
- [HTTP 状态码](https://httpwg.org/specs/rfc7231.html#status.codes)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)

---

**最后更新:** 2024年1月
**版本:** 1.0.0
**维护者:** 项目团队
