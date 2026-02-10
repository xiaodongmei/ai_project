# 养生店管理系统 - 前端 Dockerfile
# 构建阶段
FROM node:20-alpine AS builder

WORKDIR /app

# 复制 package.json 和 package-lock.json
COPY package*.json ./

# 安装依赖（使用淘宝镜像源）
RUN npm ci --registry=https://registry.npmmirror.com

# 复制源代码
COPY . .

# 构建时使用相对路径，让 nginx 反向代理处理 API 请求
ENV VITE_API_BASE_URL=/api/v1

# 构建应用
RUN npm run build

# 运行阶段
FROM nginx:alpine

# 复制 nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 从构建阶段复制构建结果
COPY --from=builder /app/dist /usr/share/nginx/html

# 暴露端口
EXPOSE 80

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]
