# 登录认证功能 - 快速启动指南

## 前提条件

- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Redis 6+
- 微信开发者账号（可选）

## 后端启动 (30秒)

### 1. 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

### 2. 初始化数据库
```bash
python init_db.py
```

### 3. 启动服务
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**验证启动成功**:
- 访问 http://localhost:8000/docs
- 应该看到 Swagger API 文档
- 在左侧导航栏应该看到 "Auth" 分组

## 前端启动 (1分钟)

### 1. 安装依赖
```bash
cd frontend
npm install
```

### 2. 启动开发服务器
```bash
npm run dev
```

**验证启动成功**:
- 访问 http://localhost:5173/login
- 应该看到登录页面有三个标签页

## 小程序启动 (2分钟)

### 1. 打开微信开发者工具
- 下载最新版本 (https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)

### 2. 导入项目
- 点击「导入项目」
- 项目目录选择: `/path/to/miniprogram`
- AppID: 使用测试AppID或真实AppID

### 3. 配置服务器地址
- 点击「详情」
- 在「项目配置」中配置本地调试域名:
  - 服务器: `http://localhost:8000`

### 4. 启动模拟器
- 点击「预览」或直接在模拟器中查看

---

## 快速测试

### 测试1: 账号密码登录

#### 前端测试
1. 打开 http://localhost:5173/login
2. 在「账号登录」标签页
3. 输入用户名和密码（首次注册账号）
4. 点击「登录」

#### 后端测试 (使用curl)
```bash
# 创建账号
curl -X POST http://localhost:8000/api/v1/auth/register/password \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123"
  }'

# 登录
curl -X POST http://localhost:8000/api/v1/auth/login/password \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPass123"
  }'
```

**预期响应**:
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    ...
  }
}
```

---

### 测试2: 手机号登录

#### 说明
在开发环境中，验证码会打印到后端日志中。

#### 步骤

**第一步: 发送验证码**
```bash
curl -X POST http://localhost:8000/api/v1/auth/send-phone-code \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "13800138000",
    "type": "login"
  }'
```

检查后端日志，找到打印的验证码，例如:
```
[SMS] 发送验证码到 13800138000: 123456
```

**第二步: 登录**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/phone \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "13800138000",
    "code": "123456"
  }'
```

**前端测试**:
1. 切换到「手机登录」标签页
2. 输入手机号: `13800138000`
3. 点击「获取验证码」
4. 复制后端日志中的验证码
5. 粘贴到「验证码」输入框
6. 点击「登录」

---

### 测试3: 微信登录

#### 说明
微信登录在开发环境需要一些特殊配置。

#### 选项A: 使用测试AppID
```python
# 修改 backend/.env
WECHAT_APP_ID=wx8888888888888888
WECHAT_APP_SECRET=test_secret
```

#### 选项B: 使用真实AppID
1. 申请微信开发者账号
2. 创建小程序或公众号
3. 获取AppID和AppSecret
4. 配置回调URL和前置条件

#### 前端测试
1. 切换到「微信登录」标签页
2. 扫描二维码（开发环境会显示占位图）
3. 微信授权后自动登录

---

## 常见问题排查

### 问题1: "Cannot connect to server"
**原因**: 后端未启动或端口不正确
**解决**:
```bash
# 检查后端是否运行
curl http://localhost:8000/health

# 输出应该是:
# {"status":"ok","app":"Wellness Shop System","version":"1.0.0"}
```

### 问题2: "CORS policy error"
**原因**: CORS配置不正确
**解决**: 修改 `backend/app/core/config.py`:
```python
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",  # Vite默认端口
]
```

### 问题3: "Database connection error"
**原因**: PostgreSQL未启动或配置错误
**解决**:
```bash
# macOS 使用Homebrew
brew services start postgresql

# Linux
sudo systemctl start postgresql

# Windows
# 从Services.msc中启动PostgreSQL服务
```

### 问题4: "Redis connection error"
**原因**: Redis未启动
**解决**:
```bash
# macOS 使用Homebrew
brew services start redis

# Linux
sudo systemctl start redis-server

# Docker
docker run -d -p 6379:6379 redis:latest
```

### 问题5: "验证码总是错误"
**原因**: 验证码未正确获取或已过期
**解决**:
1. 检查后端日志查看是否成功发送
2. 确保在5分钟内使用验证码
3. 清除浏览器缓存重试

---

## 完整启动脚本 (推荐)

创建 `start.sh` 文件:

```bash
#!/bin/bash

echo "==================== 启动养生店系统 ===================="

# 启动后端
echo "1. 启动后端服务..."
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "✓ 后端服务已启动 (PID: $BACKEND_PID)"

sleep 2

# 启动前端
echo "2. 启动前端服务..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!
echo "✓ 前端服务已启动 (PID: $FRONTEND_PID)"

echo ""
echo "==================== 系统已启动 ===================="
echo "后端 API:     http://localhost:8000"
echo "API 文档:     http://localhost:8000/docs"
echo "前端应用:     http://localhost:5173"
echo "登录页面:     http://localhost:5173/login"
echo ""
echo "按 Ctrl+C 停止所有服务"
echo "========================================================="

# 等待进程
wait
```

使用方式:
```bash
chmod +x start.sh
./start.sh
```

---

## 数据库初始化

如果需要重置数据库:

```bash
cd backend
# 删除所有表并重新创建
python init_db.py --reset

# 或手动操作
psql -U postgres -d wellness_shop -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
python init_db.py
```

---

## 生产环境部署

### 后端部署
```bash
# 使用Gunicorn + Uvicorn workers
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --env DATABASE_URL=postgresql://... \
  --env SECRET_KEY=your-production-key
```

### 前端部署
```bash
# 构建生产版本
npm run build

# 结果在 dist/ 目录
# 部署到Nginx或任何静态服务器
```

### 小程序部署
1. 在微信开发者后台上传代码
2. 提交审核
3. 发布上线

---

## 下一步

完成登录功能后，建议开发顺序：

1. ✅ **登录认证** (已完成)
2. **用户信息** - 获取/编辑用户信息
3. **产品管理** - 产品列表、搜索、详情
4. **订单管理** - 创建、查询、修改订单
5. **支付集成** - 微信支付、支付宝
6. **统计分析** - 销售数据、图表展示
7. **员工管理** - 员工列表、业绩统计

---

## 帮助和支持

- **API文档**: http://localhost:8000/docs
- **完整文档**: 查看 `AUTH_GUIDE.md`
- **问题反馈**: 提交GitHub Issue

祝您使用愉快! 🎉
