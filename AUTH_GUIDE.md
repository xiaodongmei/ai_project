# 养生店系统 - 认证登录功能完整指南

## 目录
1. [系统架构](#系统架构)
2. [功能特性](#功能特性)
3. [后端实现](#后端实现)
4. [前端实现](#前端实现)
5. [小程序实现](#小程序实现)
6. [API文档](#api文档)
7. [配置说明](#配置说明)
8. [测试指南](#测试指南)

---

## 系统架构

### 整体架构图
```
┌─────────────────────────────────────────────────────┐
│                   Web浏览器 / 小程序                  │
├────────────────┬──────────────────┬─────────────────┤
│  前端页面      │  小程序页面      │  API客户端      │
│  (Vue 3)       │  (微信原生)      │  (Request)      │
└────────┬───────┴──────┬───────────┴────────┬────────┘
         │              │                    │
         └──────────────┼────────────────────┘
                        │
                   HTTP/REST
                        │
         ┌──────────────▼────────────────┐
         │   FastAPI 后端应用             │
         │  (app/main.py)                │
         ├──────────────────────────────┤
         │   认证模块                    │
         │  - Auth API Endpoints         │
         │  - AuthService               │
         │  - Security Utils            │
         ├──────────────────────────────┤
         │   数据层                      │
         │  - PostgreSQL                │
         │  - User Model                │
         │  - Redis (缓存/验证码)       │
         └──────────────────────────────┘
```

### 技术栈
- **后端**: FastAPI + SQLAlchemy + PostgreSQL + Redis
- **Web前端**: Vue 3 + Element Plus + Axios
- **小程序**: 微信原生小程序 (WXML/WXSS/JS)

---

## 功能特性

### 支持的登录方式

| 登录方式 | 说明 | 使用场景 |
|---------|------|--------|
| **账号密码** | 用户名 + 密码 | 员工/管理员 |
| **手机号** | 手机号 + 验证码 | 顾客/员工 |
| **微信扫码** | 微信授权登录 | 快速登录/小程序 |

### 核心功能
- ✅ 账号密码注册/登录
- ✅ 手机号验证码注册/登录
- ✅ 微信授权登录/绑定
- ✅ Token刷新管理
- ✅ 密码加密存储
- ✅ 验证码缓存管理
- ✅ 错误处理和提示

---

## 后端实现

### 1. 数据库模型 (`app/models/user.py`)

```python
class User(Base, IDMixin, TimestampMixin):
    __tablename__ = "users"

    # 账号信息
    username: Optional[str]           # 用户名
    email: Optional[str]              # 邮箱
    password_hash: Optional[str]      # 密码哈希

    # 个人信息
    full_name: Optional[str]          # 姓名
    phone: Optional[str]              # 手机号
    avatar_url: Optional[str]         # 头像

    # 微信信息
    wechat_openid: Optional[str]      # 微信OpenID
    wechat_unionid: Optional[str]     # 微信UnionID
    wechat_nickname: Optional[str]    # 微信昵称
    wechat_avatar: Optional[str]      # 微信头像

    # 账号状态
    role: str                         # 角色：admin/employee/customer
    is_active: bool                   # 是否激活
    is_superuser: bool                # 是否超管

    # 手机验证
    phone_verified: bool              # 手机是否验证
    phone_verify_code: Optional[str]  # 验证码
    phone_verify_expires: Optional[int]  # 验证码过期时间
```

### 2. 认证服务 (`app/services/auth_service.py`)

核心方法：
```python
class AuthService:
    # 账号密码认证
    async def login_by_password(req: LoginByPasswordRequest) -> LoginResponse
    async def register_by_password(req: RegisterByPasswordRequest) -> LoginResponse

    # 手机号认证
    async def send_phone_code(phone: str, type: str) -> dict
    async def login_by_phone(req: LoginByPhoneRequest) -> LoginResponse
    async def register_by_phone(req: RegisterByPhoneRequest) -> LoginResponse

    # 微信认证
    async def login_by_wechat(req: LoginByWechatRequest) -> LoginResponse
    async def bind_wechat(user_id: int, code: str) -> dict

    # Token管理
    async def refresh_token(refresh_token: str) -> dict
```

### 3. 安全工具 (`app/core/security.py`)

关键函数：
```python
def hash_password(password: str) -> str
def verify_password(plain_password: str, hashed_password: str) -> bool
def create_access_token(data: dict, expires_delta: Optional[timedelta]) -> str
def create_refresh_token(data: dict) -> str
def decode_token(token: str) -> Optional[dict]
async def get_wechat_user_info(code: str) -> Optional[dict]
```

### 4. API端点 (`app/api/v1/endpoints/auth.py`)

#### 账号密码认证
```
POST /api/v1/auth/login/password
POST /api/v1/auth/register/password
```

#### 手机号认证
```
POST /api/v1/auth/send-phone-code
POST /api/v1/auth/login/phone
POST /api/v1/auth/register/phone
```

#### 微信认证
```
POST /api/v1/auth/login/wechat
POST /api/v1/auth/bind-wechat/{user_id}
GET  /api/v1/auth/wechat/verify           (服务器验证)
POST /api/v1/auth/wechat/callback         (消息回调)
```

#### Token管理
```
POST /api/v1/auth/refresh-token
```

---

## 前端实现

### 1. API服务 (`frontend/src/api/auth.js`)

```javascript
import axios from 'axios'

// 账号密码
export const loginByPassword(username, password)
export const registerByPassword(data)

// 手机号
export const sendPhoneCode(phone, type)
export const loginByPhone(phone, code)
export const registerByPhone(data)

// 微信
export const loginByWechat(code, userInfo)
export const bindWechat(userId, code)

// Token
export const refreshToken(refreshToken)
```

### 2. Pinia Store (`frontend/src/store/user.js`)

```javascript
export const useUserStore = defineStore('user', () => {
  // 状态
  const user = ref(null)
  const accessToken = ref('')
  const refreshToken = ref('')
  const isAuthenticated = computed(() => !!accessToken.value)

  // 方法
  const loginByPassword(username, password)
  const registerByPassword(data)
  const loginByPhone(phone, code)
  const registerByPhone(data)
  const loginByWechat(code, userInfo)
  const bindWechat(code)
  const refreshAccessToken()
  const logout()
})
```

### 3. 登录页面 (`frontend/src/pages/Login.vue`)

**功能**:
- 三个标签页: 账号登录 / 手机登录 / 微信登录
- 账号密码登录表单
- 手机号登录 + 验证码倒计时
- 微信扫码登录提示
- 账号密码注册弹窗
- 手机号注册弹窗
- 完整的表单验证和错误处理

**主要方法**:
```javascript
handlePasswordLogin()          // 账号登录
handlePasswordRegister()       // 账号注册
sendPhoneCode()               // 发送验证码
handlePhoneLogin()            // 手机登录
handlePhoneRegister()         // 手机注册
switchToRegister()            // 切换到注册
validatePhone(phone)          // 验证手机号
startCodeCooldown()           // 验证码倒计时
```

### 4. 路由守卫 (`frontend/src/router/index.js`)

```javascript
router.beforeEach((to, from, next) => {
  const accessToken = localStorage.getItem('access_token')

  if (to.meta.requiresAuth && !accessToken) {
    next('/login')
  } else if (to.path === '/login' && accessToken) {
    next('/dashboard')
  } else {
    next()
  }
})
```

---

## 小程序实现

### 1. 登录页面 (`miniprogram/pages/login/index.wxml`)

**UI结构**:
- Logo和标题
- 三个标签页切换
- 每个标签页的表单
- 注册弹窗（账号和手机号）

### 2. 逻辑实现 (`miniprogram/pages/login/index.js`)

**主要方法**:
```javascript
switchTab(e)                        // 切换标签
handlePasswordLogin()               // 账号登录
handlePasswordRegister()            // 账号注册
sendPhoneCode()                     // 发送验证码
handlePhoneLogin()                  // 手机登录
handlePhoneRegister()               // 手机注册
loginWithWechat()                   // 微信登录
validatePhone(phone)                // 验证手机号
startCodeCooldown()                 // 倒计时
```

### 3. API服务 (`miniprogram/api/auth.js`)

与Web端相同的API调用方式

### 4. HTTP工具 (`miniprogram/utils/request.js`)

**特性**:
- 自动Token刷新
- 请求队列管理
- 错误处理和重定向
- Token过期检测

**关键函数**:
```javascript
export const request(options)       // 发起请求
export const getAccessToken()       // 获取Token
export const getUser()              // 获取用户信息
export const clearUserData()        // 清除数据
```

---

## API文档

### 登录API

#### POST /api/v1/auth/login/password
**账号密码登录**

请求:
```json
{
  "username": "john_doe",
  "password": "SecurePass123"
}
```

响应:
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "phone": null,
    "role": "customer",
    "is_active": true,
    "is_superuser": false,
    "phone_verified": false,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

---

#### POST /api/v1/auth/register/password
**账号密码注册**

请求:
```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "SecurePass123",
  "full_name": "New User"
}
```

响应: 同登录响应

---

#### POST /api/v1/auth/send-phone-code
**发送手机验证码**

请求:
```json
{
  "phone": "13800138000",
  "type": "login"  // login | register | reset_password
}
```

响应:
```json
{
  "message": "验证码已发送",
  "phone": "13800138000",
  "expires_in": 300
}
```

---

#### POST /api/v1/auth/login/phone
**手机号登录**

请求:
```json
{
  "phone": "13800138000",
  "code": "123456"
}
```

响应: 同登录响应

---

#### POST /api/v1/auth/login/wechat
**微信登录/注册**

请求:
```json
{
  "code": "021Y0000dj....",
  "userInfo": null
}
```

响应: 同登录响应

---

#### POST /api/v1/auth/refresh-token
**刷新访问令牌**

请求:
```json
{
  "refresh_token": "eyJhbGc..."
}
```

响应:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

---

## 配置说明

### 环境变量配置 (`.env`)

```bash
# FastAPI配置
APP_NAME=Wellness Shop System
APP_VERSION=1.0.0
DEBUG=True
API_PREFIX=/api/v1

# 数据库
DATABASE_URL=postgresql://user:password@localhost:5432/wellness_shop

# JWT配置
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Redis配置
REDIS_URL=redis://localhost:6379/0
CACHE_EXPIRE_SECONDS=300

# 微信配置
WECHAT_APP_ID=your_wechat_app_id
WECHAT_APP_SECRET=your_wechat_app_secret
WECHAT_MCH_ID=your_wechat_mch_id
WECHAT_API_KEY=your_wechat_api_key
WECHAT_TOKEN=wellness_shop_token

# 短信配置
SMS_PROVIDER=aliyun
SMS_ACCESS_KEY_ID=your_sms_key_id
SMS_ACCESS_KEY_SECRET=your_sms_key_secret
SMS_SIGN_NAME=养生店系统
SMS_TEMPLATE_CODE=your_template_code

# CORS配置
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# 日志
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### 前端配置 (`.env.local`)

```
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

---

## 测试指南

### 后端测试

#### 1. 启动后端服务
```bash
cd backend
pip install -r requirements.txt
python init_db.py
uvicorn app.main:app --reload
```

#### 2. 访问API文档
```
http://localhost:8000/docs
```

#### 3. 测试账号登录
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/password \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "TestPass123"}'
```

#### 4. 测试手机登录
```bash
# 第一步：发送验证码
curl -X POST http://localhost:8000/api/v1/auth/send-phone-code \
  -H "Content-Type: application/json" \
  -d '{"phone": "13800138000", "type": "login"}'

# 第二步：用验证码登录
curl -X POST http://localhost:8000/api/v1/auth/login/phone \
  -H "Content-Type: application/json" \
  -d '{"phone": "13800138000", "code": "123456"}'
```

### 前端测试

#### 1. 启动前端开发服务器
```bash
cd frontend
npm install
npm run dev
```

#### 2. 访问登录页面
```
http://localhost:5173/login
```

#### 3. 测试各种登录方式
- 输入账号密码，点击登录
- 点击手机登录标签，输入手机号并获取验证码
- 点击微信登录标签查看二维码

### 小程序测试

#### 1. 打开微信开发者工具
- 选择「小程序」
- 导入项目目录 `miniprogram/`

#### 2. 配置API基础URL
- 修改 `miniprogram/api/auth.js` 中的 `API_BASE_URL`
- 添加服务器域名白名单

#### 3. 测试登录流程
- 在模拟器中打开登录页面
- 测试各种登录方式

---

## 常见问题

### Q: 验证码为什么总是不对？
**A**: 验证码存储在Redis中，需要配置正确的Redis连接。在开发环境中，可以查看后端日志看打印的验证码。

### Q: 微信登录报"授权失败"？
**A**: 需要配置正确的微信AppID和AppSecret。小程序登录需要在微信开发者后台配置服务器地址。

### Q: Token刷新后还是提示"未授权"？
**A**: 检查刷新令牌是否有效，或清除浏览器缓存重新登录。

### Q: 前端发送请求一直超时？
**A**:
- 检查后端是否正常运行
- 检查CORS配置是否正确
- 检查防火墙设置

---

## 最佳实践

### 安全建议
1. **生产环境**：修改 `SECRET_KEY`，使用强密码规则
2. **密码策略**：要求至少8位，包含大小写和数字
3. **Token过期**：短Token (30分钟) + 长RefreshToken (7天)
4. **HTTPS**：生产环境必须使用HTTPS
5. **验证码**：限制发送频率，如60秒内最多3次

### 性能优化
1. **缓存**：使用Redis缓存验证码和用户信息
2. **数据库索引**：在username、phone、email、wechat_openid上建立索引
3. **请求限流**：限制登录/注册请求频率，防止暴力破解
4. **异步任务**：发送短信使用异步任务队列（Celery）

---

## 下一步

完成了完整的登录注册功能后，建议继续完成：

1. **用户管理** - 用户信息编辑、头像上传、密码修改
2. **账户安全** - 两因素认证(2FA)、设备绑定
3. **权限管理** - 基于角色的访问控制(RBAC)、细粒度权限
4. **审计日志** - 记录登录、注册、敏感操作
5. **集成支付宝** - 支付宝账户登录

---

## 支持

遇到问题？检查：
- 后端日志: `backend/logs/app.log`
- 浏览器控制台: F12 → Console
- 小程序调试: 微信开发者工具的Console标签
