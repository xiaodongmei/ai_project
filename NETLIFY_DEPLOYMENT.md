# 📦 Netlify 部署指南

## ✅ 准备工作已完成

已为你的项目配置好以下文件：

1. ✅ `frontend/netlify.toml` - Netlify 构建配置
2. ✅ `frontend/public/_redirects` - SPA 路由重定向规则
3. ✅ `frontend/.env.production` - 生产环境变量
4. ✅ `frontend/src/api/client.js` - API 基础路径支持环境变量
5. ✅ 构建测试通过 - `dist` 文件夹已生成

---

## 🚀 部署方式

### 方式一：通过 Netlify 网站手动部署（推荐新手）

1. **登录 Netlify**
   - 访问：https://app.netlify.com/projects/air-game-751fb2/overview
   - 登录你的账号

2. **部署设置**
   - 点击 `Deploys` 标签
   - 点击 `Deploy site` 按钮
   - 选择 `Deploy manually`

3. **上传构建文件**
   - 将 `frontend/dist` 文件夹拖拽到上传区域
   - 或点击选择 `frontend/dist` 文件夹

4. **等待部署完成**
   - 部署进度会实时显示
   - 完成后会显示部署 URL

---

### 方式二：通过 Git 自动部署（推荐）

#### 步骤 1：连接 Git 仓库

1. 在 Netlify 项目页面，点击 `Site configuration` → `Build & deploy`
2. 点击 `Link repository`
3. 选择你的 Git 提供商（GitHub/GitLab/Bitbucket）
4. 授权并选择你的仓库

#### 步骤 2：配置构建设置

在 Netlify 后台设置以下参数：

```
Base directory: frontend
Build command: npm run build
Publish directory: frontend/dist
```

#### 步骤 3：设置环境变量

在 `Site configuration` → `Environment variables` 中添加：

```
VITE_API_BASE_URL=https://your-backend-api.com/api/v1
```

**重要：** 请将 `your-backend-api.com` 替换为你的实际后端 API 地址

#### 步骤 4：触发部署

推送代码到 Git 仓库：

\`\`\`bash
cd /Users/xiaodongmei/Desktop/xdm_2026_agent/ys/wellness-shop-system
git add .
git commit -m "配置 Netlify 部署"
git push origin main
\`\`\`

---

### 方式三：使用 Netlify CLI 部署

#### 安装 Netlify CLI

\`\`\`bash
npm install -g netlify-cli
\`\`\`

#### 登录 Netlify

\`\`\`bash
netlify login
\`\`\`

#### 部署到生产环境

\`\`\`bash
cd /Users/xiaodongmei/Desktop/xdm_2026_agent/ys/wellness-shop-system/frontend
npm run build
netlify deploy --prod --dir=dist
\`\`\`

选择你的站点：`air-game-751fb2`

---

## 🔧 重要配置说明

### 1. 后端 API 地址配置

**开发环境：** 使用本地代理 `http://localhost:8000/api/v1`

**生产环境：** 需要设置环境变量 `VITE_API_BASE_URL`

有两种方式设置：

**方式 A：在 Netlify 后台设置（推荐）**
- 进入 `Site configuration` → `Environment variables`
- 添加 `VITE_API_BASE_URL` = 你的后端API地址

**方式 B：修改 `.env.production` 文件**
- 编辑 `frontend/.env.production`
- 修改 `VITE_API_BASE_URL=https://your-backend-api.com/api/v1`

### 2. 跨域问题处理

如果后端 API 和前端不在同一域名，需要在后端配置 CORS：

\`\`\`python
# backend/app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-netlify-site.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
\`\`\`

---

## 📋 部署检查清单

- [ ] 构建成功（`npm run build` 无错误）
- [ ] 配置了正确的后端 API 地址
- [ ] 后端配置了 CORS 允许前端域名
- [ ] 测试登录功能
- [ ] 测试路由跳转（刷新页面不报 404）
- [ ] 检查所有页面功能正常

---

## 🎯 快速部署命令（推荐）

如果你想立即部署，运行以下命令：

\`\`\`bash
# 进入前端目录
cd /Users/xiaodongmei/Desktop/xdm_2026_agent/ys/wellness-shop-system/frontend

# 构建生产版本
npm run build

# 安装 Netlify CLI（如果还没安装）
npm install -g netlify-cli

# 登录 Netlify
netlify login

# 部署到生产环境
netlify deploy --prod --dir=dist
\`\`\`

在命令行提示中选择：`air-game-751fb2` 站点

---

## 🔗 部署后的访问地址

部署成功后，你的网站将可以通过以下地址访问：

- **主域名：** `https://air-game-751fb2.netlify.app`
- **自定义域名：** 可在 Netlify 后台 `Domain settings` 中配置

---

## ⚠️ 常见问题

### 1. 刷新页面出现 404

**原因：** SPA 路由配置问题

**解决：** 已配置 `_redirects` 文件，重新部署即可

### 2. API 请求失败

**原因：** 后端 API 地址未配置或跨域问题

**解决：**
- 检查 `VITE_API_BASE_URL` 环境变量
- 确保后端配置了 CORS

### 3. 登录后显示"未登录"

**原因：** 已修复，使用 `userStore` 管理状态

**验证：** 重新登录测试

---

## 📞 需要帮助？

如有部署问题，请提供：
- Netlify 部署日志
- 浏览器控制台错误信息
- 具体报错截图

祝部署顺利！🎉
