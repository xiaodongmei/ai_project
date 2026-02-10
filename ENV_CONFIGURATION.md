# 环境变量配置指南

完整的环境变量配置文档，包括所有可用的配置选项和说明。

## 目录

1. [快速开始](#快速开始)
2. [应用配置](#应用配置)
3. [数据库配置](#数据库配置)
4. [Redis 配置](#redis-配置)
5. [认证配置](#认证配置)
6. [支付配置](#支付配置)
7. [邮件配置](#邮件配置)
8. [日志配置](#日志配置)
9. [第三方服务](#第三方服务)
10. [开发与生产配置](#开发与生产配置)

---

## 快速开始

### 获取配置模板

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑 .env 文件
nano .env
```

### 验证配置

```bash
# 后端验证
cd backend
python check_env.py

# 前端会自动从 .env 中读取 VITE_* 前缀的变量
```

### 环境变量优先级

1. `.env` 文件（项目根目录）
2. 系统环境变量
3. 代码中的默认值

---

## 应用配置

### 基础配置

```bash
# 应用名称
APP_NAME=wellness-shop-system

# 应用版本
APP_VERSION=1.0.0

# 调试模式（开发环境设为 True，生产环境设为 False）
DEBUG=True

# 密钥（JWT 加密和会话管理，生成强随机密钥）
# 使用 python -c "import secrets; print(secrets.token_urlsafe(40))" 生成
SECRET_KEY=your-super-secret-key-change-this-in-production-12345678

# API 前缀
API_PREFIX=/api/v1

# 服务器地址（Docker 环境使用 0.0.0.0）
SERVER_HOST=0.0.0.0

# 服务器端口
SERVER_PORT=8000

# 允许的来源（CORS 配置，JSON 数组格式）
CORS_ORIGINS=["http://localhost", "http://localhost:5173", "http://localhost:3000"]
```

**生成强密钥：**
```bash
python -c "import secrets; print(secrets.token_urlsafe(40))"
# 输出示例：
# V_c3XwZYvPkQ_5ZjL0zP7A3q4BcDeEfGhIjKlMnOpQ
```

---

## 数据库配置

### PostgreSQL 连接

```bash
# 数据库类型（通常为 postgresql）
DATABASE_TYPE=postgresql

# 数据库主机名
DATABASE_HOST=localhost
# Docker 环境：postgres

# 数据库端口
DATABASE_PORT=5432

# 数据库名称
DATABASE_DB=wellness_shop
# 或使用环境变量名 POSTGRES_DB

# 数据库用户名
DATABASE_USER=postgres
# 或使用环境变量名 POSTGRES_USER

# 数据库密码
DATABASE_PASSWORD=postgres123
# 或使用环境变量名 POSTGRES_PASSWORD

# 或使用完整的 DATABASE_URL（可选）
# DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/wellness_shop
```

### 数据库连接选项

```bash
# 连接池大小
DATABASE_POOL_SIZE=10

# 连接空闲超时（秒）
DATABASE_POOL_RECYCLE=3600

# 最大溢出连接数
DATABASE_MAX_OVERFLOW=20

# 启用连接池预加载
DATABASE_POOL_PRE_PING=True

# SQL 回显（调试用，不要在生产环境启用）
DATABASE_ECHO=False
```

### 创建 PostgreSQL 数据库

```bash
# 使用 psql
psql -U postgres -c "CREATE DATABASE wellness_shop;"

# 或使用 Docker
docker run --rm postgres:15 \
  psql -h postgres -U postgres -c "CREATE DATABASE wellness_shop;"

# 设置字符编码
psql -U postgres -c "CREATE DATABASE wellness_shop ENCODING 'UTF8';"
```

---

## Redis 配置

### Redis 连接

```bash
# Redis 主机名
REDIS_HOST=localhost
# Docker 环境：redis

# Redis 端口
REDIS_PORT=6379

# Redis 密码（如果需要）
REDIS_PASSWORD=redis123

# Redis 数据库编号（0-15）
REDIS_DB=0

# 或使用完整的 REDIS_URL
# REDIS_URL=redis://default:redis123@localhost:6379/0
```

### Redis 连接选项

```bash
# SSL 连接（生产环境推荐）
REDIS_SSL=False

# 连接超时（秒）
REDIS_SOCKET_TIMEOUT=5

# 连接重试次数
REDIS_RETRY_ON_TIMEOUT=3

# 连接池大小
REDIS_CONNECTION_POOL_SIZE=10
```

### Redis 应用

缓存用途：
- JWT Token 黑名单
- 会话存储
- 缓存热数据
- 实时统计数据

```bash
# 缓存过期时间（秒）
CACHE_EXPIRATION=3600

# Token 黑名单过期时间
TOKEN_BLACKLIST_EXPIRATION=86400

# 会话过期时间
SESSION_EXPIRATION=2592000  # 30 天
```

---

## 认证配置

### JWT 配置

```bash
# JWT 秘钥（与 SECRET_KEY 相同，或单独设置）
JWT_SECRET_KEY=your-jwt-secret-key

# JWT 算法
JWT_ALGORITHM=HS256
# 或 RS256, ES256 等

# JWT Token 过期时间（分钟）
JWT_EXPIRATION_MINUTES=60

# JWT 刷新 Token 过期时间（天）
JWT_REFRESH_EXPIRATION_DAYS=7

# Token 前缀
JWT_TOKEN_PREFIX=Bearer
```

### 密码配置

```bash
# 密码最小长度
PASSWORD_MIN_LENGTH=8

# 密码是否需要大写字母
PASSWORD_REQUIRE_UPPERCASE=True

# 密码是否需要特殊字符
PASSWORD_REQUIRE_SPECIAL=True

# 密码过期时间（天，0 表示不过期）
PASSWORD_EXPIRATION_DAYS=0

# 密码历史记录（防止重复使用）
PASSWORD_HISTORY_COUNT=3
```

### 登录配置

```bash
# 登录尝试次数限制
MAX_LOGIN_ATTEMPTS=5

# 账户锁定时间（分钟）
ACCOUNT_LOCK_TIME=15

# 登录记录保留时间（天）
LOGIN_HISTORY_RETENTION_DAYS=90

# 是否启用 2FA（双因素认证）
TWO_FACTOR_AUTH_ENABLED=False
```

---

## 支付配置

### 微信支付

```bash
# 微信支付应用 ID
WECHAT_APP_ID=wx1234567890abcdef

# 微信支付应用密钥
WECHAT_APP_SECRET=abcdef1234567890abcdef1234567890

# 微信商户号
WECHAT_MCH_ID=1234567890

# 微信商户密钥
WECHAT_MCH_KEY=abcdef1234567890abcdef1234567890

# 微信 API 密钥（V3）
WECHAT_API_KEY_V3=abcdef1234567890abcdef1234567890

# 微信支付证书路径
WECHAT_CERT_PATH=/path/to/cert.pem
WECHAT_KEY_PATH=/path/to/key.pem

# 微信支付 SSL 验证
WECHAT_SSL_VERIFY=True

# 微信回调 URL
WECHAT_CALLBACK_URL=https://your-domain.com/api/v1/payments/wechat/callback
```

### 支付宝

```bash
# 支付宝应用 ID
ALIPAY_APP_ID=2016123456789012

# 支付宝应用私钥
ALIPAY_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----

# 支付宝公钥
ALIPAY_PUBLIC_KEY=-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----

# 支付宝网关
ALIPAY_GATEWAY=https://openapi.alipay.com/gateway.do

# 沙箱模式（测试）
ALIPAY_SANDBOX=False

# 支付宝回调 URL
ALIPAY_CALLBACK_URL=https://your-domain.com/api/v1/payments/alipay/callback
```

### 支付配置公用

```bash
# 支付超时时间（分钟）
PAYMENT_TIMEOUT_MINUTES=15

# 最小支付金额
PAYMENT_MIN_AMOUNT=0.01

# 最大支付金额
PAYMENT_MAX_AMOUNT=999999.99

# 支付成功重试次数
PAYMENT_RETRY_COUNT=3

# 支付记录保留时间（天）
PAYMENT_RECORD_RETENTION_DAYS=365
```

---

## 邮件配置

### SMTP 配置

```bash
# SMTP 服务器地址
SMTP_SERVER=smtp.gmail.com
# 常用服务器：
# smtp.qq.com (QQ 邮箱)
# smtp.163.com (网易邮箱)
# smtp.aliyun.com (阿里邮箱)

# SMTP 端口
SMTP_PORT=587
# TLS: 587, SSL: 465, 标准: 25

# SMTP 用户名/邮箱
SMTP_USERNAME=your-email@gmail.com

# SMTP 密码/应用密码
SMTP_PASSWORD=your-app-password

# 是否使用 TLS
SMTP_USE_TLS=True

# 是否使用 SSL
SMTP_USE_SSL=False

# 邮件发送者地址
SMTP_FROM_EMAIL=noreply@wellness-shop.com

# 邮件发送者名称
SMTP_FROM_NAME=养生店管理系统
```

### 邮件模板

```bash
# 是否启用邮件功能
EMAIL_ENABLED=True

# 邮件模板路径
EMAIL_TEMPLATE_PATH=/app/templates/emails

# 发送邮件时是否等待（同步/异步）
EMAIL_ASYNC=True

# 邮件发送队列名称
EMAIL_QUEUE_NAME=email
```

### 邮件用途

```bash
# 是否发送注册确认邮件
SEND_REGISTRATION_EMAIL=True

# 是否发送密码重置邮件
SEND_RESET_PASSWORD_EMAIL=True

# 是否发送订单确认邮件
SEND_ORDER_CONFIRMATION_EMAIL=True

# 是否发送发货通知邮件
SEND_SHIPMENT_EMAIL=True

# 是否发送账单邮件
SEND_INVOICE_EMAIL=True
```

---

## 日志配置

### 日志级别

```bash
# 日志级别（DEBUG, INFO, WARNING, ERROR, CRITICAL）
LOG_LEVEL=INFO

# 数据库查询日志级别
LOG_LEVEL_DB=WARNING

# 请求日志级别
LOG_LEVEL_REQUEST=INFO

# 日志文件路径
LOG_FILE_PATH=/app/logs/app.log

# 日志文件最大大小（字节，10MB）
LOG_FILE_MAX_BYTES=10485760

# 日志文件备份个数
LOG_FILE_BACKUP_COUNT=10
```

### Sentry 错误追踪

```bash
# Sentry DSN（用于错误捕获和报告）
SENTRY_DSN=https://xxxxx@sentry.io/xxxxx

# Sentry 环境
SENTRY_ENVIRONMENT=production
# 或 development, staging

# Sentry 采样率（0-1，1 表示 100%）
SENTRY_TRACES_SAMPLE_RATE=0.1

# Sentry 错误采样率
SENTRY_ERROR_SAMPLE_RATE=1.0

# Sentry 发布版本
SENTRY_RELEASE=1.0.0
```

---

## 第三方服务

### 美团（外卖）

```bash
# 美团应用 ID
MEITUAN_APP_ID=your-app-id

# 美团应用密钥
MEITUAN_APP_SECRET=your-app-secret

# 美团商户 ID
MEITUAN_MERCHANT_ID=your-merchant-id

# 美团回调 URL
MEITUAN_CALLBACK_URL=https://your-domain.com/api/v1/orders/meituan/callback
```

### 抖音（小程序）

```bash
# 抖音应用 ID
DOUYIN_APP_ID=your-app-id

# 抖音应用密钥
DOUYIN_APP_SECRET=your-app-secret

# 抖音商户 ID
DOUYIN_MERCHANT_ID=your-merchant-id

# 抖音回调 URL
DOUYIN_CALLBACK_URL=https://your-domain.com/api/v1/orders/douyin/callback
```

### 微信小程序

```bash
# 微信小程序应用 ID
WECHAT_MINI_APP_ID=wx1234567890abcdef

# 微信小程序应用密钥
WECHAT_MINI_APP_SECRET=abcdef1234567890abcdef1234567890
```

### 文件存储（AWS S3）

```bash
# AWS 访问密钥 ID
AWS_ACCESS_KEY_ID=your-access-key

# AWS 秘钥
AWS_SECRET_ACCESS_KEY=your-secret-key

# S3 桶名称
AWS_STORAGE_BUCKET_NAME=wellness-shop-bucket

# S3 区域
AWS_STORAGE_REGION=us-east-1

# S3 自定义域名（可选）
AWS_STORAGE_CUSTOM_DOMAIN=cdn.example.com

# S3 是否使用 HTTPS
AWS_S3_USE_SSL=True
```

---

## 开发与生产配置

### 开发环境 (.env.dev)

```bash
# 应用
DEBUG=True
SECRET_KEY=dev-secret-key-not-for-production

# 数据库
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_DB=wellness_shop_dev
DATABASE_USER=postgres
DATABASE_PASSWORD=dev-password

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# CORS
CORS_ORIGINS=["http://localhost", "http://localhost:5173", "http://localhost:3000"]

# 邮件
SMTP_USERNAME=dev@example.com
SMTP_PASSWORD=dev-password

# 日志
LOG_LEVEL=DEBUG

# 禁用 Sentry
SENTRY_DSN=
```

### 生产环境 (.env.prod)

```bash
# 应用
DEBUG=False
SECRET_KEY=<use-strong-random-key>

# 数据库
DATABASE_HOST=<production-db-host>
DATABASE_PORT=5432
DATABASE_DB=wellness_shop
DATABASE_USER=<secure-username>
DATABASE_PASSWORD=<strong-password>

# Redis
REDIS_HOST=<production-redis-host>
REDIS_PORT=6379
REDIS_PASSWORD=<strong-password>

# CORS
CORS_ORIGINS=["https://your-domain.com", "https://www.your-domain.com"]

# 邮件
SMTP_USERNAME=<production-email>
SMTP_PASSWORD=<production-password>

# 日志
LOG_LEVEL=INFO

# Sentry
SENTRY_DSN=<your-sentry-dsn>
SENTRY_ENVIRONMENT=production
SENTRY_RELEASE=1.0.0

# 支付（生产配置）
WECHAT_APP_ID=<production-wechat-id>
WECHAT_APP_SECRET=<production-wechat-secret>
ALIPAY_APP_ID=<production-alipay-id>
```

### Staging 环境 (.env.staging)

```bash
# 介于开发和生产之间的配置
DEBUG=False
SECRET_KEY=<staging-secret-key>

# 数据库
DATABASE_HOST=<staging-db-host>

# CORS（允许测试域名）
CORS_ORIGINS=["https://staging.your-domain.com", "http://localhost:5173"]

# Sentry
SENTRY_ENVIRONMENT=staging
SENTRY_TRACES_SAMPLE_RATE=0.5  # 采样 50%
```

---

## 配置加载

### 优先级顺序

```python
# 1. 系统环境变量
import os
os.environ['DEBUG']  # 最高优先级

# 2. .env 文件（当前目录）
from dotenv import load_dotenv
load_dotenv('.env')  # 加载 .env 文件

# 3. 代码默认值
DEBUG = os.getenv('DEBUG', 'False') == 'True'  # 默认 False
```

### Python 配置示例

```python
# app/core/config.py

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 应用配置
    app_name: str = "wellness-shop-system"
    app_version: str = "1.0.0"
    debug: bool = False
    secret_key: str
    api_prefix: str = "/api/v1"

    # 数据库配置
    database_url: Optional[str] = None
    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "wellness_shop"
    database_user: str = "postgres"
    database_password: str

    # Redis 配置
    redis_url: Optional[str] = None
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: Optional[str] = None

    # JWT 配置
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

---

## 安全建议

### 密钥管理

```bash
# 永远不要在 Git 中提交真实密钥
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore

# 使用 .env.example 作为模板
cp .env.example .env

# 使用强随机密钥
python -c "import secrets; print(secrets.token_urlsafe(40))"
```

### 环境变量敏感信息

- 不要提交包含实际值的 `.env`
- 使用 `.env.example` 作为模板
- 在服务器上单独管理敏感配置
- 使用密钥管理服务（如 AWS Secrets Manager）

### 密码安全

```bash
# 不要在代码中写死密码
# 不好：
DATABASE_PASSWORD=admin123

# 好：使用环境变量
DATABASE_PASSWORD=${PROD_DB_PASSWORD}

# 或使用密钥管理服务
```

---

## 常见问题

### Q: 如何动态修改配置而不重启应用？

```python
# 使用 Redis 存储动态配置
redis_client.set('config:email_enabled', 'true')

# 在应用中读取
is_email_enabled = redis_client.get('config:email_enabled') == b'true'
```

### Q: 环境变量值不被读取？

```bash
# 1. 确保 .env 文件在项目根目录
ls -la .env

# 2. 确保使用了 load_dotenv()
from dotenv import load_dotenv
load_dotenv()

# 3. 检查变量名大小写
# 环境变量通常为大写
DATABASE_PASSWORD=xxx

# 4. 检查是否有空格
# 错误：KEY = value
# 正确：KEY=value
```

### Q: Docker 环境中环境变量不工作？

```bash
# 在 docker-compose.yml 中显式设置
environment:
  - DATABASE_HOST=postgres
  - DATABASE_PASSWORD=${DATABASE_PASSWORD}

# 或使用 env_file
env_file:
  - .env
```

---

## 参考资源

- [Pydantic Settings 文档](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [PostgreSQL 连接字符串](https://www.postgresql.org/docs/current/libpq-connstring.html)
- [Redis 连接 URL](https://redis-py.readthedocs.io/en/stable/)
- [微信支付文档](https://pay.weixin.qq.com/wiki/doc/apiv3/index.shtml)
- [支付宝开放平台](https://open.alipay.com/)

---

**最后更新:** 2024年1月
**版本:** 1.0.0
