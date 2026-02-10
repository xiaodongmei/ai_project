# 部署检查清单

在部署养生店管理系统到生产环境前，使用此清单确保所有准备工作已完成。

## 目录

1. [部署前检查](#部署前检查)
2. [代码准备](#代码准备)
3. [基础设施准备](#基础设施准备)
4. [安全加固](#安全加固)
5. [性能优化](#性能优化)
6. [数据库准备](#数据库准备)
7. [监控和日志](#监控和日志)
8. [部署步骤](#部署步骤)
9. [部署后验证](#部署后验证)
10. [回滚计划](#回滚计划)

---

## 部署前检查

### 环境信息

- [ ] 确认目标服务器操作系统和版本
- [ ] 确认服务器 CPU 和内存规格
- [ ] 确认服务器磁盘空间（至少 20GB）
- [ ] 确认网络连接和带宽
- [ ] 确认备案情况（中国大陆需要备案）
- [ ] 确认 SSL 证书已准备（域名 SSL）

### 前置软件

- [ ] 已安装 Docker 和 Docker Compose
- [ ] 已安装 PostgreSQL 13+（如果不使用 Docker）
- [ ] 已安装 Redis 6+（如果不使用 Docker）
- [ ] 已安装 Nginx 或其他反向代理
- [ ] Python 版本 >= 3.9（后端）
- [ ] Node.js 版本 >= 16（前端）

### 项目准备

- [ ] 所有代码已 Push 到 Git 仓库
- [ ] 所有测试通过（`npm run test`、`pytest`）
- [ ] 代码已经过 Code Review
- [ ] 没有任何 TODO 或 FIXME 注释
- [ ] 依赖文件已更新（requirements.txt、package.json）
- [ ] README 和文档已更新

---

## 代码准备

### 后端代码

- [ ] 生成版本号并更新 `APP_VERSION`
- [ ] 所有 DEBUG 日志已移除或关闭
- [ ] 密钥和敏感信息已从代码中移除
- [ ] 错误处理已完善
- [ ] 日志级别设置为 INFO 或 WARNING
- [ ] 所有外部依赖已明确指定版本
- [ ] 运行 `black app/`、`isort app/` 格式化代码
- [ ] 运行 `flake8 app/` 检查代码质量
- [ ] 生成数据库迁移脚本
- [ ] 测试数据库迁移（在本地测试）

**检查命令：**
```bash
cd backend

# 格式化
black app/
isort app/

# 质量检查
flake8 app/
pylint app/

# 安全检查
bandit -r app/

# 依赖检查
pip audit

# 运行测试
pytest
```

### 前端代码

- [ ] 生成生产构建（`npm run build`）
- [ ] 构建大小正常（< 500KB gzipped）
- [ ] 所有控制台警告已解决
- [ ] 所有页面已测试（功能和性能）
- [ ] 响应式设计已验证
- [ ] 跨浏览器兼容性已测试
- [ ] 所有 console.log 已移除
- [ ] 代码已通过 ESLint 检查
- [ ] 敏感 API 密钥已从代码移除
- [ ] 环境变量已配置正确

**检查命令：**
```bash
cd frontend

# 检查代码
npm run lint

# 构建生产版本
npm run build

# 检查构建大小
ls -lh dist/

# 检查 source map（生产环境应禁用）
grep "sourcemap" vite.config.js
```

### 版本和 Changelog

- [ ] 版本号已更新（语义版本管理）
- [ ] CHANGELOG.md 已更新
- [ ] Git 标签已创建（`git tag v1.0.0`）
- [ ] 发布说明已准备

---

## 基础设施准备

### 服务器配置

- [ ] 时间同步已配置（NTP）
- [ ] 防火墙规则已配置（仅开放必要端口）
- [ ] SSH 密钥已配置（禁用密码登录）
- [ ] sudo 权限已配置
- [ ] 磁盘使用警告已配置
- [ ] 自动更新已配置（安全补丁）

**防火墙规则示例（UFW）：**
```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### Docker 配置

- [ ] Docker daemon 配置已优化
- [ ] 日志驱动已配置（避免磁盘爆满）
- [ ] 镜像仓库已配置
- [ ] 卷管理已配置
- [ ] 网络配置已完善

**Docker 日志配置 (/etc/docker/daemon.json)：**
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

### 反向代理配置

- [ ] Nginx/Apache 已安装并配置
- [ ] SSL 证书已配置
- [ ] HTTPS 重定向已配置
- [ ] 静态文件缓存已配置
- [ ] 压缩已启用（gzip）
- [ ] 反向代理超时已配置
- [ ] 负载均衡已配置（如需要）

---

## 安全加固

### 密钥管理

- [ ] 生成强随机 SECRET_KEY（40+ 字符）
- [ ] 生成强随机 JWT_SECRET_KEY
- [ ] 数据库密码强度 >= 16 字符，包含大小写字母、数字、特殊字符
- [ ] Redis 密码已设置
- [ ] 所有密钥已存储在安全位置（不在 Git 中）
- [ ] 轮换密钥计划已制定

### 访问控制

- [ ] CORS 配置已限制（仅允许特定域名）
- [ ] API 认证已启用（JWT）
- [ ] 敏感端点已添加权限检查
- [ ] 速率限制已配置
- [ ] DDoS 防护已启用

**CORS 配置示例：**
```python
CORS_ORIGINS = ["https://your-domain.com", "https://www.your-domain.com"]
```

### 数据保护

- [ ] 数据库连接使用 SSL/TLS
- [ ] 密码使用 bcrypt 加密存储
- [ ] 敏感数据字段已加密
- [ ] PII 数据访问已日志记录
- [ ] 定期备份已计划
- [ ] 数据保留政策已制定

### HTTP 安全头

- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options: SAMEORIGIN
- [ ] X-XSS-Protection: 1; mode=block
- [ ] Strict-Transport-Security: max-age=31536000
- [ ] Content-Security-Policy 已配置
- [ ] Referrer-Policy: strict-origin-when-cross-origin

**Nginx 配置示例：**
```nginx
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Strict-Transport-Security "max-age=31536000" always;
```

### 依赖安全

- [ ] 已检查已知漏洞（`pip audit`、`npm audit`）
- [ ] 依赖已更新到最新安全版本
- [ ] 安全补丁已应用
- [ ] 自动安全扫描已配置

---

## 性能优化

### 数据库优化

- [ ] 索引已创建并优化
- [ ] 慢查询已识别并优化
- [ ] 连接池已配置
- [ ] 查询缓存已配置（Redis）
- [ ] 分析和统计查询已优化
- [ ] 备份和恢复计划已制定

### 缓存策略

- [ ] Redis 缓存已配置
- [ ] 静态文件缓存已配置（HTTP 缓存头）
- [ ] API 响应缓存已配置
- [ ] CDN 已配置（如需要）

### 前端优化

- [ ] 代码分割已实现
- [ ] 懒加载已实现
- [ ] 图片优化已完成
- [ ] 构建大小已优化
- [ ] Source map 已禁用（生产）

### 后端优化

- [ ] 数据库连接池已优化
- [ ] 异步处理已实现（I/O 密集操作）
- [ ] 中间件顺序已优化
- [ ] 内存泄漏已排查

---

## 数据库准备

### 初始化

- [ ] 数据库已创建
- [ ] 用户账户已创建（非 root）
- [ ] 表结构已初始化
- [ ] 初始数据已导入（如需要）
- [ ] 索引已创建
- [ ] 权限已配置

**数据库初始化命令：**
```bash
# 本地初始化
cd backend
python init_db.py

# Docker 初始化
docker-compose exec backend python init_db.py
```

### 备份计划

- [ ] 完整备份计划已制定（每日）
- [ ] 增量备份计划已制定（每小时）
- [ ] 备份脚本已测试
- [ ] 备份存储位置已确认
- [ ] 恢复程序已测试
- [ ] 备份加密已配置

**备份脚本示例：**
```bash
#!/bin/bash
BACKUP_DIR="/backups/wellness-shop"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U postgres wellness_shop | gzip > $BACKUP_DIR/db_$DATE.sql.gz
```

### 监控配置

- [ ] 数据库监控已配置
- [ ] 查询性能监控已配置
- [ ] 连接数监控已配置
- [ ] 磁盘使用监控已配置
- [ ] 告警规则已设置

---

## 监控和日志

### 日志配置

- [ ] 应用日志已配置（日志级别：INFO）
- [ ] 访问日志已配置
- [ ] 错误日志已配置
- [ ] 日志轮转已配置
- [ ] 日志聚合已配置（ELK、Loki 等）
- [ ] 敏感信息过滤已配置（不记录密码等）

### 监控工具

- [ ] Prometheus 已部署（指标收集）
- [ ] Grafana 已部署（可视化）
- [ ] AlertManager 已配置（告警）
- [ ] 告警规则已设置
- [ ] Uptime 监控已配置
- [ ] 性能监控已配置

### 错误追踪

- [ ] Sentry 已配置（错误捕获）
- [ ] 告警规则已设置
- [ ] 错误响应率阈值已设置

---

## 部署步骤

### 部署前

- [ ] 所有检查项已完成
- [ ] 备份已创建
- [ ] 回滚计划已准备
- [ ] 部署文档已更新
- [ ] 团队沟通已完成
- [ ] 部署窗口已确定

### 部署

1. **准备阶段**
   - [ ] SSH 连接到服务器
   - [ ] 拉取最新代码
   - [ ] 构建 Docker 镜像
   - [ ] 运行数据库迁移（在较低环境测试）

2. **上线阶段**
   - [ ] 停止当前应用（或使用蓝绿部署）
   - [ ] 备份当前数据库
   - [ ] 应用数据库迁移
   - [ ] 启动新应用
   - [ ] 验证应用启动成功

3. **验证阶段**
   - [ ] 健康检查通过
   - [ ] 关键功能已验证
   - [ ] 日志无错误
   - [ ] 监控数据正常

**部署命令示例：**
```bash
# 拉取最新代码
git pull origin main

# 构建镜像
docker-compose build

# 运行迁移
docker-compose exec backend python init_db.py

# 启动应用
docker-compose up -d

# 验证状态
docker-compose ps
docker-compose logs
```

---

## 部署后验证

### 功能测试

- [ ] 登录功能正常
- [ ] 所有主要页面可访问
- [ ] 创建、读取、更新、删除操作正常
- [ ] 搜索和过滤功能正常
- [ ] 支付流程可以完成
- [ ] 导出报表功能正常

**测试脚本示例：**
```bash
# 健康检查
curl https://your-domain.com/health

# API 测试
curl https://your-domain.com/api/v1/info

# 登录测试
curl -X POST https://your-domain.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'
```

### 性能测试

- [ ] 首页加载时间 < 3 秒
- [ ] API 响应时间 < 500ms（平均）
- [ ] 数据库查询耗时 < 100ms（平均）
- [ ] 错误率 < 0.1%
- [ ] 无 5xx 错误

### 安全验证

- [ ] SSL/TLS 证书有效
- [ ] 没有不安全的 HTTP 请求
- [ ] 密码不在日志中
- [ ] API 密钥不在客户端代码中
- [ ] CORS 配置正确

### 监控验证

- [ ] 所有监控指标正常
- [ ] 日志正确输出
- [ ] 告警系统工作
- [ ] 性能指标在预期范围内

---

## 回滚计划

### 回滚触发条件

- [ ] 严重功能异常（无法登录、数据错误）
- [ ] 性能严重下降（API 响应 > 5s）
- [ ] 错误率 > 5%
- [ ] 数据库无法访问
- [ ] 应用频繁崩溃

### 回滚步骤

1. **准备阶段**
   - 通知所有相关人员
   - 准备回滚脚本
   - 验证备份完整性

2. **执行回滚**
   ```bash
   # 停止当前版本
   docker-compose stop

   # 恢复旧版本
   git checkout <previous-version>
   docker-compose build

   # 恢复数据库
   # 使用备份：pg_restore -d wellness_shop backup.dump

   # 启动应用
   docker-compose up -d
   ```

3. **验证回滚**
   - 确认应用正常启动
   - 验证数据完整性
   - 运行关键测试

4. **事后分析**
   - 记录所有错误和日志
   - 分析根本原因
   - 制定改进方案

### 备份和恢复

- [ ] 备份策略已定义
- [ ] 备份已定期测试
- [ ] 恢复流程已文档化
- [ ] 恢复时间目标（RTO）已定义
- [ ] 恢复点目标（RPO）已定义

---

## 部署后维护

### 日常维护

- [ ] 日志已检查（无异常）
- [ ] 性能指标已检查
- [ ] 备份已验证
- [ ] 安全补丁已检查
- [ ] 依赖更新已检查

### 定期任务

- [ ] 每周性能分析
- [ ] 每月安全审计
- [ ] 每季度容量规划
- [ ] 每年架构审查

### 故障处理

- [ ] 故障响应流程已定义
- [ ] 值班安排已制定
- [ ] 故障升级流程已定义
- [ ] 故障通知模板已准备

---

## 检查完成情况

### 检查总计

- **总项数**: 150+ 项
- **必须完成**: 所有红旗项 ✓
- **强烈建议**: 所有蓝旗项 ✓
- **可选**: 其他绿旗项

### 签核

- [ ] 开发负责人确认
- [ ] 运维负责人确认
- [ ] 产品负责人确认
- [ ] 技术总监批准

**签核信息：**
```
开发负责人: _________________ 日期: _______
运维负责人: _________________ 日期: _______
产品负责人: _________________ 日期: _______
技术总监:   _________________ 日期: _______
```

---

## 参考资源

- [部署指南](./DEPLOYMENT.md)
- [API 文档](./API_DOCUMENTATION.md)
- [数据库指南](./DATABASE_GUIDE.md)
- [环境配置](./ENV_CONFIGURATION.md)

---

**最后更新:** 2024年1月
**版本:** 1.0.0
**检查日期:** ___________
