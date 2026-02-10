# 🔗 连接 Netlify 前端到本地后端指南

## ✅ 当前状态

- ✅ **前端已部署：** https://yangsheng-game-751fb2.netlify.app
- ✅ **后端已启动：** http://localhost:8000
- ✅ **CORS 已配置：** 允许 Netlify 域名访问

---

## 🚀 方案一：使用 ngrok（推荐，最简单）

### 1. 安装 ngrok

**macOS (使用 Homebrew):**
```bash
brew install ngrok/ngrok/ngrok
```

**或手动下载：**
1. 访问 https://ngrok.com/download
2. 下载 macOS 版本
3. 解压到任意目录
4. 添加到 PATH 或直接使用

### 2. 注册账号（免费）

访问：https://dashboard.ngrok.com/signup
注册后获取 authtoken

### 3. 配置 authtoken

```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

### 4. 启动内网穿透

```bash
ngrok http 8000
```

你会看到类似输出：
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8000
```

### 5. 更新 Netlify 环境变量

1. 访问 Netlify 项目：https://app.netlify.com/sites/yangsheng-game-751fb2/configuration/env
2. 添加环境变量：
   - Key: `VITE_API_BASE_URL`
   - Value: `https://abc123.ngrok.io/api/v1` （替换为你的 ngrok URL）

### 6. 重新部署 Netlify

在 Netlify 后台点击 `Deploys` → `Trigger deploy` → `Deploy site`

### 7. 访问测试

打开：https://yangsheng-game-751fb2.netlify.app/login

---

## 🚀 方案二：使用 Cloudflare Tunnel（永久免费）

### 1. 安装 cloudflared

```bash
brew install cloudflare/cloudflare/cloudflared
```

### 2. 启动隧道

```bash
cloudflared tunnel --url http://localhost:8000
```

会显示：
```
Your quick tunnel is: https://xyz.trycloudflare.com
```

### 3. 更新 Netlify 环境变量

同上，将 `VITE_API_BASE_URL` 设置为 Cloudflare 提供的 URL + `/api/v1`

---

## 🚀 方案三：使用 localtunnel

### 1. 安装

```bash
npm install -g localtunnel
```

### 2. 启动隧道

```bash
lt --port 8000 --subdomain yangsheng-backend
```

### 3. 更新 Netlify 环境变量

同上设置 `VITE_API_BASE_URL`

---

## ⚡ 快速启动命令（推荐 ngrok）

### Terminal 1 - 启动后端
```bash
cd /Users/xiaodongmei/Desktop/xdm_2026_agent/ys/wellness-shop-system/backend
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Terminal 2 - 启动 ngrok
```bash
ngrok http 8000
```

### Terminal 3 - 更新 Netlify（可选）
```bash
# 复制 ngrok 提供的 URL，然后更新前端环境变量
# 方式1：在 Netlify 后台手动配置
# 方式2：使用以下命令重新构建前端（如果需要）

cd /Users/xiaodongmei/Desktop/xdm_2026_agent/ys/wellness-shop-system/frontend

# 临时设置环境变量并构建
VITE_API_BASE_URL=https://YOUR_NGROK_URL/api/v1 npm run build

# 使用 Netlify CLI 部署
netlify deploy --prod --dir=dist
```

---

## 🎯 完整工作流程

### 步骤 1：启动本地后端
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 步骤 2：启动 ngrok
```bash
ngrok http 8000
```

**记录显示的 URL**，例如：`https://abc123.ngrok.io`

### 步骤 3：配置 Netlify 环境变量

访问：https://app.netlify.com/sites/yangsheng-game-751fb2/configuration/env

添加或更新：
- **Variable:** `VITE_API_BASE_URL`
- **Value:** `https://abc123.ngrok.io/api/v1`

### 步骤 4：触发重新部署

点击 `Deploys` → `Trigger deploy` → `Clear cache and deploy site`

### 步骤 5：测试

访问：https://yangsheng-game-751fb2.netlify.app/login

尝试登录，检查是否能成功连接到本地后端。

---

## 🔍 验证连接

### 1. 检查后端健康状态

```bash
curl https://YOUR_NGROK_URL/api/v1/health
```

应该返回：
```json
{"status":"ok","app":"Wellness Shop System","version":"1.0.0"}
```

### 2. 检查前端控制台

打开浏览器开发者工具 → Network 标签

登录时应该看到请求发送到 ngrok URL

### 3. 检查 CORS

如果看到 CORS 错误，确认：
- ✅ 后端 `config.py` 中已添加 Netlify 域名
- ✅ 后端服务已重启

---

## ⚠️ 注意事项

### ngrok 免费版限制
- ✅ 每次启动 URL 会变化（需要重新配置 Netlify）
- ✅ 每分钟 40 个请求
- ✅ 连接会在 2 小时后断开

### 避免 URL 变化的方法
1. **ngrok 付费版**（$8/月）- 固定域名
2. **使用 Cloudflare Tunnel**（永久免费，但 URL 也会变）
3. **部署后端到云服务器**（推荐长期方案）

---

## 🎉 成功标志

当你看到：
- ✅ ngrok 显示请求日志
- ✅ 前端可以成功登录
- ✅ 数据可以正常加载

恭喜！连接成功！

---

## 🐛 故障排查

### 问题 1：前端仍然请求 localhost:8000

**原因：** 环境变量未生效

**解决：**
1. 确认在 Netlify 后台设置了 `VITE_API_BASE_URL`
2. 触发重新部署（Clear cache and deploy）
3. 等待部署完成后刷新页面

### 问题 2：CORS 错误

**解决：**
```bash
# 重启后端服务
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 问题 3：ngrok 连接中断

**解决：**
- 重新启动 ngrok
- 更新 Netlify 环境变量为新的 URL
- 重新部署

---

## 📞 需要帮助？

如遇问题，请提供：
1. ngrok 输出的 URL
2. 浏览器控制台错误信息
3. Netlify 部署日志

祝顺利连接！🎉
