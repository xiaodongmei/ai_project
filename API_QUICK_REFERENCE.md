# API 快速参考指南

## 🚀 快速启动

```bash
cd backend
uvicorn app.main:app --reload
```

访问: `http://localhost:8000/docs`

---

## 📋 顾客管理 API

### 获取顾客列表
```bash
GET /api/v1/customers?skip=0&limit=10&search=张&is_member=true
```

### 创建顾客
```bash
POST /api/v1/customers
Content-Type: application/json

{
  "name": "张三",
  "phone": "13800138000",
  "is_member": true,
  "member_level": "gold"
}
```

### 获取顾客详情
```bash
GET /api/v1/customers/1
```

### 更新顾客
```bash
PUT /api/v1/customers/1
Content-Type: application/json

{
  "name": "李四",
  "is_member": true
}
```

### 删除顾客
```bash
DELETE /api/v1/customers/1
```

### 顾客统计
```bash
GET /api/v1/customers/statistics/overview
```

---

## 🏷️ 产品管理 API

### 获取分类列表
```bash
GET /api/v1/categories
```

### 创建分类
```bash
POST /api/v1/categories
Content-Type: application/json

{
  "name": "按摩服务",
  "display_order": 1
}
```

### 获取产品列表
```bash
GET /api/v1/products?skip=0&limit=10&category_id=1&search=足疗
```

### 创建产品
```bash
POST /api/v1/products
Content-Type: application/json

{
  "category_id": 1,
  "name": "足疗服务",
  "member_price": 88.00,
  "non_member_price": 98.00,
  "stock_quantity": 100
}
```

### 获取产品详情
```bash
GET /api/v1/products/1
```

### 更新产品
```bash
PUT /api/v1/products/1
Content-Type: application/json

{
  "stock_quantity": 95,
  "is_featured": true
}
```

### 删除产品
```bash
DELETE /api/v1/products/1
```

---

## 📦 订单管理 API

### 获取订单列表
```bash
GET /api/v1/orders?skip=0&limit=10&status=pending
```

### 创建订单
```bash
POST /api/v1/orders
Content-Type: application/json

{
  "customer_id": 1,
  "total_amount": 188.00,
  "payment_method": "wechat"
}
```

### 获取订单详情
```bash
GET /api/v1/orders/1
```

### 更新订单
```bash
PUT /api/v1/orders/1
Content-Type: application/json

{
  "remark": "客户特殊要求"
}
```

### 更新订单状态
```bash
PATCH /api/v1/orders/1/status
Content-Type: application/json

{
  "status": "completed"
}
```

### 添加订单项
```bash
POST /api/v1/orders/1/items
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 2,
  "unit_price": 88.00
}
```

### 获取订单项列表
```bash
GET /api/v1/orders/1/items
```

### 删除订单项
```bash
DELETE /api/v1/order-items/1
```

---

## 👨‍💼 员工管理 API

### 获取员工列表
```bash
GET /api/v1/employees?skip=0&limit=10&position=按摩师
```

### 创建员工
```bash
POST /api/v1/employees
Content-Type: application/json

{
  "name": "王五",
  "employee_number": "EMP001",
  "phone": "13900139000",
  "position": "按摩师"
}
```

### 获取员工详情
```bash
GET /api/v1/employees/1
```

### 更新员工
```bash
PUT /api/v1/employees/1
Content-Type: application/json

{
  "position": "主管"
}
```

### 删除员工
```bash
DELETE /api/v1/employees/1
```

### 获取员工业绩
```bash
GET /api/v1/employees/1/performance
```

### 员工业绩排行
```bash
GET /api/v1/employees/performance/ranking?limit=10
```

---

## 📊 统计分析 API

### 获取每日统计
```bash
GET /api/v1/statistics/daily?start_date=2024-01-01&end_date=2024-01-31
```

### 获取指定日期统计
```bash
GET /api/v1/statistics/daily/2024-01-28
```

### 获取渠道分布
```bash
GET /api/v1/statistics/channels?date_str=2024-01-28
```

### 渠道趋势
```bash
GET /api/v1/statistics/channels/trend?channel=meituan&days=7
```

### 仪表板数据
```bash
GET /api/v1/statistics/dashboard
```

### 统计摘要
```bash
GET /api/v1/statistics/summary?period=week
```

---

## 🔑 通用参数

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| skip | int | 分页偏移 | 0 |
| limit | int | 每页数量 | 10 |
| search | string | 搜索关键词 | "张三" |
| status | string | 状态筛选 | "pending" |
| start_date | string | 开始日期 | "2024-01-01" |
| end_date | string | 结束日期 | "2024-01-31" |

---

## 📈 状态值列表

### 订单状态
- `pending` - 待处理
- `completed` - 已完成
- `cancelled` - 已取消

### 会员等级
- `normal` - 普通会员
- `silver` - 银卡会员
- `gold` - 金卡会员
- `platinum` - 铂金会员

### 支付方式
- `cash` - 现金
- `card` - 刷卡
- `wechat` - 微信支付
- `alipay` - 支付宝

---

## ✅ 响应示例

### 成功响应 (200)
```json
{
  "id": 1,
  "name": "张三",
  "phone": "13800138000",
  "created_at": "2024-01-28T10:00:00",
  "updated_at": "2024-01-28T10:00:00"
}
```

### 列表响应 (200)
```json
{
  "total": 50,
  "skip": 0,
  "limit": 10,
  "data": [...]
}
```

### 创建成功 (201)
```json
{
  "id": 1,
  "name": "新顾客",
  "created_at": "2024-01-28T10:00:00"
}
```

### 错误响应 (400/404/500)
```json
{
  "detail": "顾客ID 1 不存在"
}
```

---

## 🛠️ 常用curl命令

### 列表查询
```bash
curl -X GET "http://localhost:8000/api/v1/customers?skip=0&limit=10"
```

### 创建
```bash
curl -X POST "http://localhost:8000/api/v1/customers" \
  -H "Content-Type: application/json" \
  -d '{"name":"test","phone":"13800000000"}'
```

### 更新
```bash
curl -X PUT "http://localhost:8000/api/v1/customers/1" \
  -H "Content-Type: application/json" \
  -d '{"name":"updated"}'
```

### 删除
```bash
curl -X DELETE "http://localhost:8000/api/v1/customers/1"
```

---

## 🔍 调试技巧

### 查看API文档
```
http://localhost:8000/docs
```

### 查看数据库日志
```python
# 在 app/core/config.py 中启用
SQLALCHEMY_ECHO = True
```

### 测试异步操作
使用Swagger UI的"Try it out"按钮

### 检查请求/响应
浏览器F12 → Network标签

---

## 📱 Python客户端示例

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# 获取顾客列表
response = requests.get(f"{BASE_URL}/customers")
customers = response.json()

# 创建顾客
data = {
    "name": "张三",
    "phone": "13800138000",
    "is_member": True
}
response = requests.post(f"{BASE_URL}/customers", json=data)
new_customer = response.json()

# 更新顾客
response = requests.put(f"{BASE_URL}/customers/1", json={"name": "李四"})

# 删除顾客
response = requests.delete(f"{BASE_URL}/customers/1")
```

---

## 🚨 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| 404 | 资源不存在 | 检查ID是否正确 |
| 400 | 请求参数错误 | 检查JSON格式和字段值 |
| 500 | 服务器错误 | 查看后端日志 |
| CORS错误 | 跨域问题 | 检查CORS配置 |

---

## 📞 获取帮助

- API文档: `http://localhost:8000/docs`
- 代码: `/Users/xiaodongmei/Desktop/xdm_2026_agent/ys/wellness-shop-system/`
- 详细文档: `API_DEVELOPMENT_SUMMARY.md`

---

**版本**: 1.0.0
**最后更新**: 2024年
