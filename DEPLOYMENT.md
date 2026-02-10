# 部署指南

完整的养生店管理系统部署文档，涵盖本地开发、Docker 容器化部署和生产环境部署。

## 目录

1. [快速开始](#快速开始)
2. [Docker 部署](#docker-部署)
3. [生产环境部署](#生产环境部署)
4. [数据库迁移](#数据库迁移)
5. [常见问题](#常见问题)
6. [故障排查](#故障排查)

---

## 快速开始

### 前置要求

- Python 3.9+
- Node.js 16+
- PostgreSQL 13+
- Redis 6+
- Docker & Docker Compose（可选，但推荐）

### 本地开发环境设置

#### 1. 克隆项目

```bash
git clone <repository-url>
cd wellness-shop-system
```

#### 2. 复制环境变量配置

```bash
cp .env.example .env
# 根据本地环境修改 .env 文件
```

#### 3. 启动后端服务

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
# venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_db.py

# 启动服务
uvicorn app.main:app --reload
```

**输出示例：**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

#### 4. 启动前端服务

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

**输出示例：**
```
➜  Local:   http://localhost:5173/
```

#### 5. 访问应用

- 前端: http://localhost:5173
- 后端 API 文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

---

## Docker 部署

### 使用 Docker Compose 快速启动（推荐）

#### 1. 配置环境变量

```bash
cp .env.example .env
# 修改 .env 文件中的敏感信息
```

#### 2. 构建并启动所有服务

```bash
# 构建镜像（首次运行必需）
docker-compose build

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

#### 3. 初始化数据库（首次运行）

```bash
# 进入后端容器
docker-compose exec backend bash

# 运行初始化脚本
python init_db.py

# 退出容器
exit
```

#### 4. 访问服务

- 前端: http://localhost
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs

### 单独构建 Docker 镜像

#### 后端镜像

```bash
cd backend

# 构建镜像
docker build -t wellness-backend:latest .

# 运行容器
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:password@host:5432/db" \
  -e REDIS_URL="redis://host:6379/0" \
  --name wellness-backend \
  wellness-backend:latest

# 查看日志
docker logs wellness-backend

# 停止容器
docker stop wellness-backend
```

#### 前端镜像

```bash
cd frontend

# 构建镜像
docker build -t wellness-frontend:latest .

# 运行容器
docker run -d \
  -p 80:80 \
  -e VITE_API_BASE_URL="http://localhost:8000/api/v1" \
  --name wellness-frontend \
  wellness-frontend:latest

# 查看日志
docker logs wellness-frontend

# 停止容器
docker stop wellness-frontend
```

### Docker 常用命令

```bash
# 查看所有镜像
docker images

# 查看所有容器
docker ps -a

# 进入容器 shell
docker exec -it <container-id> bash

# 查看容器日志（实时）
docker logs -f <container-id>

# 查看容器资源使用情况
docker stats

# 删除镜像
docker rmi <image-id>

# 删除容器
docker rm <container-id>

# 清理未使用资源
docker system prune -a
```

---

## 生产环境部署

### 系统要求

- 操作系统：Ubuntu 20.04 LTS 或 CentOS 8+
- CPU：2+ 核心
- 内存：4GB+
- 磁盘：20GB+
- 带宽：1Mbps+

### 方案一：使用 Docker Compose（推荐）

#### 1. 服务器准备

```bash
# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 验证安装
docker --version
docker-compose --version
```

#### 2. 部署应用

```bash
# 上传项目代码到服务器
scp -r ./wellness-shop-system root@your-server:/opt/

# SSH 连接到服务器
ssh root@your-server

# 进入项目目录
cd /opt/wellness-shop-system

# 配置环境变量
cp .env.example .env
nano .env  # 编辑 .env 文件
```

#### 3. 生产环境 .env 配置示例

```bash
# 应用配置
APP_NAME=wellness-shop-system
APP_VERSION=1.0.0
DEBUG=False
SECRET_KEY=<random-40-character-secret-key>
JWT_EXPIRATION_MINUTES=1440

# 数据库
POSTGRES_DB=wellness_shop
POSTGRES_USER=<strong-username>
POSTGRES_PASSWORD=<strong-password>
DATABASE_URL=postgresql://<username>:<password>@postgres:5432/wellness_shop

# Redis
REDIS_PASSWORD=<strong-redis-password>
REDIS_URL=redis://default:<password>@redis:6379/0

# CORS 配置
CORS_ORIGINS=["https://your-domain.com", "https://www.your-domain.com"]

# 前端 API 地址
VITE_API_BASE_URL=https://api.your-domain.com/api/v1

# 支付配置（如需集成）
WECHAT_APP_ID=<your-wechat-app-id>
WECHAT_APP_SECRET=<your-wechat-app-secret>

# Email 配置
SMTP_SERVER=smtp.your-email-provider.com
SMTP_PORT=587
SMTP_USERNAME=<your-email>
SMTP_PASSWORD=<your-app-password>
```

#### 4. 启动服务

```bash
# 构建镜像
docker-compose build

# 后台启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 初始化数据库
docker-compose exec backend python init_db.py
```

#### 5. 配置 Nginx 反向代理

```bash
# 安装 Nginx
sudo apt-get update
sudo apt-get install -y nginx certbot python3-certbot-nginx

# 创建 Nginx 配置文件
sudo nano /etc/nginx/sites-available/wellness-shop

# 添加以下配置：
```

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # 重定向 HTTP 到 HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL 证书配置
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # 启用 gzip 压缩
    gzip on;
    gzip_types text/plain text/css text/js text/xml text/javascript application/json application/javascript application/xml+rss;

    # 前端
    location / {
        proxy_pass http://localhost:80;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # 后端 API
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
}
```

```bash
# 启用配置
sudo ln -s /etc/nginx/sites-available/wellness-shop /etc/nginx/sites-enabled/

# 测试 Nginx 配置
sudo nginx -t

# 启动 Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# 配置 SSL 证书（使用 Let's Encrypt）
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

#### 6. 验证部署

```bash
# 检查服务健康状态
curl https://your-domain.com/health
curl https://api.your-domain.com/health

# 查看容器日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 方案二：使用 Kubernetes 部署（高级）

详见 [Kubernetes 部署指南](./docs/KUBERNETES_DEPLOYMENT.md)

---

## 数据库迁移

### 初始化数据库

```bash
# 进入后端目录
cd backend

# 运行初始化脚本
python init_db.py
```

### 使用 Alembic 进行数据库迁移

```bash
# 生成迁移脚本
alembic revision --autogenerate -m "description"

# 应用迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1

# 查看迁移历史
alembic current
alembic history
```

### 数据库备份

```bash
# 备份 PostgreSQL 数据库
docker-compose exec postgres pg_dump -U postgres wellness_shop > backup.sql

# 恢复数据库
docker-compose exec -T postgres psql -U postgres wellness_shop < backup.sql

# 备份 Redis 数据
docker-compose exec redis redis-cli BGSAVE
docker-compose exec redis redis-cli LASTSAVE
```

---

## 常见问题

### Q: 如何更新应用代码？

```bash
# 拉取最新代码
git pull origin main

# 重建镜像（如果有依赖变化）
docker-compose build

# 重启服务
docker-compose restart

# 或使用 up 命令（自动重建）
docker-compose up -d
```

### Q: 如何扩展应用（多实例）？

```bash
# 使用 docker-compose scale 命令
docker-compose up -d --scale backend=3
```

### Q: 如何查看应用日志？

```bash
# 查看所有服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs backend

# 实时查看日志
docker-compose logs -f backend

# 查看最后 100 行日志
docker-compose logs --tail=100 backend
```

### Q: 如何临时关闭某个服务？

```bash
# 停止服务
docker-compose stop backend

# 启动服务
docker-compose start backend

# 重启服务
docker-compose restart backend
```

### Q: 如何清理 Docker 资源？

```bash
# 删除已停止的容器
docker-compose rm

# 删除不使用的镜像
docker image prune

# 删除所有未使用资源
docker system prune -a
```

---

## 故障排查

### 问题 1: 数据库连接失败

**症状：** `OperationalError: could not translate host name "postgres" to address`

**解决方案：**
```bash
# 检查 PostgreSQL 容器状态
docker-compose ps postgres

# 检查容器日志
docker-compose logs postgres

# 重启 PostgreSQL 容器
docker-compose restart postgres

# 检查网络连接
docker-compose exec backend ping postgres
```

### 问题 2: Redis 连接失败

**症状：** `ConnectionError: Error 111 connecting to redis:6379`

**解决方案：**
```bash
# 检查 Redis 容器
docker-compose ps redis

# 检查 Redis 日志
docker-compose logs redis

# 验证密码配置
docker-compose exec redis redis-cli -a <password> ping
```

### 问题 3: 前端无法访问 API

**症状：** `CORS error` 或 `404 Not Found`

**解决方案：**
1. 检查 `.env` 中的 `CORS_ORIGINS` 配置
2. 验证 `VITE_API_BASE_URL` 是否正确
3. 检查后端是否正在运行：`curl http://localhost:8000/health`
4. 查看浏览器控制台的 Network 标签查看具体错误

```bash
# 重新构建前端
docker-compose build frontend

# 重启前端服务
docker-compose restart frontend
```

### 问题 4: 端口被占用

**症状：** `Address already in use` 或 `Bind for 0.0.0.0:8000 failed`

**解决方案：**
```bash
# 查找占用端口的进程
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# 杀死进程
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# 或修改 docker-compose.yml 中的端口映射
# 将 8000:8000 改为 8001:8000
```

### 问题 5: 内存不足

**症状：** 容器频繁重启或被杀死

**解决方案：**
```bash
# 检查容器资源使用情况
docker stats

# 增加 Docker 内存限制（编辑 docker-compose.yml）
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 2G

# 清理不必要的镜像和容器
docker system prune -a
```

### 问题 6: 权限问题

**症状：** `Permission denied` 错误

**解决方案：**
```bash
# 检查文件权限
ls -la backend/

# 修改文件权限
chmod -R 755 backend/
chmod -R 755 frontend/

# 或者在 docker-compose.yml 中指定用户
services:
  backend:
    user: "1000:1000"
```

---

## 监控和维护

### 日志管理

```bash
# 查看容器日志大小
docker inspect --format='{{.LogPath}}' <container-id>

# 清理日志（Docker 内置）
# 编辑 /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

### 定期备份

```bash
# 创建备份脚本 backup.sh
#!/bin/bash
BACKUP_DIR="/backups/wellness-shop"
DATE=$(date +%Y%m%d_%H%M%S)

# 备份数据库
docker-compose exec -T postgres pg_dump -U postgres wellness_shop | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# 备份 Redis
docker-compose exec redis redis-cli BGSAVE
docker cp wellness_redis:/data/dump.rdb $BACKUP_DIR/redis_$DATE.rdb

echo "Backup completed: $DATE"
```

### 性能优化

```bash
# 启用 Docker swarm mode（多节点部署）
docker swarm init

# 或使用 Kubernetes 进行容器编排
# 详见 K8s 部署指南
```

---

## 安全建议

1. **更改默认密码**
   - PostgreSQL 密码
   - Redis 密码
   - JWT 密钥

2. **启用 SSL/TLS**
   - 使用 Let's Encrypt 配置 HTTPS
   - 配置安全的 Nginx 反向代理

3. **定期更新依赖**
   ```bash
   # Python 依赖更新
   pip list --outdated
   pip install --upgrade <package>

   # Node 依赖更新
   npm outdated
   npm update
   ```

4. **设置防火墙**
   ```bash
   # 仅允许必要的端口
   sudo ufw allow 22/tcp   # SSH
   sudo ufw allow 80/tcp   # HTTP
   sudo ufw allow 443/tcp  # HTTPS
   sudo ufw enable
   ```

5. **定期备份**
   - 设置 cron 任务自动备份数据库
   - 验证备份的完整性

6. **监控和告警**
   - 使用 Docker 日志驱动收集日志
   - 配置告警规则
   - 定期审查日志

---

## 参考资源

- [Docker 官方文档](https://docs.docker.com/)
- [FastAPI 部署指南](https://fastapi.tiangolo.com/deployment/)
- [Vue 3 生产构建](https://vuejs.org/guide/best-practices/production-deployment.html)
- [Nginx 反向代理](https://nginx.org/en/docs/)
- [PostgreSQL 文档](https://www.postgresql.org/docs/)

---

## 获取帮助

如遇到部署问题，请：

1. 检查 [故障排查](#故障排查) 部分
2. 查看相关日志文件
3. 参考项目文档
4. 提交 Issue 或联系技术支持

---

**最后更新:** 2024年1月
**维护者:** 项目团队
