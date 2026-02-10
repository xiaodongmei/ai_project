# Vue Web 前端 - 快速启动指南

## 系统要求

- Node.js >= 14.0
- npm >= 6.0 或 yarn >= 1.22

## 快速启动（3 分钟）

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

### 3. 打开浏览器

访问 `http://localhost:5173`

## 默认登录信息

登录页面已实现，您可以输入任何用户名和密码进行测试。系统会调用后端 API 进行认证。

## 项目结构速览

```
frontend/src/
├── pages/              # 页面组件（4 个已完成）
├── components/         # 公共组件（6 个已完成）
├── layouts/            # 布局组件（1 个已完成）
├── api/                # API 服务（7 个已完成）
├── router/             # 路由配置
├── store/              # 状态管理
├── styles/             # 样式文件
├── utils/              # 工具函数
└── App.vue
```

## 已完成的功能

### ✓ 页面
- 登录页面 (`/login`)
- 仪表板 (`/dashboard`)
- 顾客管理 (`/customers`)
- 产品管理 (`/products`)

### ✓ 组件
- 主布局容器
- 侧边栏导航
- 顶部导航栏
- 指标卡片
- ECharts 图表（4 种）
- 对话框和抽屉

### ✓ 功能
- 用户登录/登出
- 数据列表（分页、搜索、筛选）
- 新增/编辑/删除数据
- 数据详情查看
- 数据导出
- 图表展示

## 常用命令

### 开发

```bash
npm run dev          # 启动开发服务器
```

### 构建

```bash
npm run build        # 生产构建
npm run preview      # 预览构建结果
```

### 代码检查

```bash
npm run lint         # ESLint 检查
```

## 项目配置

### API 地址

修改 `vite.config.js` 中的 proxy 配置：

```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8000',  // 改为您的后端地址
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/api/, '/api/v1'),
  },
}
```

### 环境变量

创建 `.env.local` 文件：

```
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_TITLE=养生店管理系统
```

## 开发工作流

### 新增页面

1. 在 `src/pages/` 创建 Vue 文件
2. 在 `src/router/index.js` 添加路由
3. 在 `src/components/Sidebar.vue` 添加菜单

### 新增组件

1. 在 `src/components/` 创建 Vue 文件
2. 使用时导入即可

### 新增 API

1. 在 `src/api/` 创建服务文件
2. 导出接口函数
3. 在页面或组件中调用

### 样式编写

使用 SCSS 变量和混合函数：

```vue
<style scoped lang="scss">
@import '@/styles/variables';
@import '@/styles/mixins';

.my-component {
  @include flex-center;
  padding: $space-lg;
  color: $text-primary;
  background: $bg-light;
  border: 1px solid $border-color;
  border-radius: $border-radius-base;
  @include transition;

  &:hover {
    background: $white;
    @include box-shadow($shadow-md);
  }

  @include respond-to('md') {
    // 移动端样式
  }
}
</style>
```

## 前端功能概览

### 登录页面
- 用户名/邮箱和密码登录
- 记住账号功能
- 错误提示
- 响应式设计

### 仪表板
展示 8 个关键指标和 4 个图表：
- 店铺营收（¥829.80）
- 店铺实收（¥802.32）
- 会员充值（¥295.06）
- 客流量（13 人）
- 有效订单数（13 个）
- 项目总数（12 个）
- 新增顾客（5 人）
- 成交率（72.5%）

### 顾客管理
- 顾客列表（支持分页、搜索、筛选）
- 新增顾客
- 编辑顾客信息
- 删除顾客
- 查看顾客详情
- 查看消费记录
- 查看会员信息
- 导出数据

### 产品管理
- 产品列表（支持分页、搜索、分类筛选）
- 分类管理
- 新增产品（框架）
- 编辑产品（框架）
- 库存管理（框架）
- 删除产品
- 导出数据

## 文件说明

### 重要文件

| 文件 | 用途 | 说明 |
|-----|------|------|
| `src/main.js` | 应用入口 | 导入全局样式和 Element Plus |
| `src/router/index.js` | 路由配置 | 定义所有路由和守卫 |
| `src/App.vue` | 根组件 | 路由出口 |
| `vite.config.js` | Vite 配置 | 代理、别名等 |
| `package.json` | 项目配置 | 依赖和脚本 |

### 样式文件

| 文件 | 用途 | 说明 |
|-----|------|------|
| `styles/variables.scss` | CSS 变量 | 45+ 个颜色、尺寸、字体变量 |
| `styles/global.scss` | 全局样式 | 元素重置、工具类、主题覆盖 |
| `styles/mixins.scss` | 混合函数 | 40+ 个 SCSS 混合函数 |

## 常见问题

### Q: 访问页面显示 404 错误
A: 检查后端 API 是否正常运行，查看浏览器控制台的网络请求错误。

### Q: 样式不正常显示
A: 确保已导入 `src/styles/global.scss`，检查 Element Plus 是否正确导入。

### Q: 如何修改菜单项
A: 编辑 `src/components/Sidebar.vue` 中的菜单配置。

### Q: 如何添加新的 API 接口
A: 在 `src/api/` 中的相应文件添加接口函数，然后在页面或组件中导入使用。

### Q: 如何自定义主题色
A: 修改 `src/styles/variables.scss` 中的颜色变量，或在 `src/styles/global.scss` 中覆盖 Element Plus 变量。

## 下一步

### 完成待做项

查看 `FRONTEND_TODO.md` 了解待完成功能：

1. **订单管理** - Orders.vue 页面和相关组件
2. **员工管理** - Employees.vue 页面和相关组件
3. **数据统计** - Statistics.vue 页面和统计图表
4. **通用组件** - Table、SearchForm、Modal 等

### 学习资源

- [Vue 3 官方文档](https://vuejs.org/)
- [Element Plus 文档](https://element-plus.org/)
- [ECharts 文档](https://echarts.apache.org/)
- [Pinia 文档](https://pinia.vuejs.org/)

## 开发建议

### 最佳实践
1. 使用 Composition API 的 `<script setup>` 语法
2. 为每个组件添加 Props 和 Emits 定义
3. 使用样式变量和混合函数保持一致性
4. 添加必要的代码注释
5. 定期提交代码

### 性能优化
1. 使用路由懒加载（已配置）
2. 对大列表使用虚拟滚动
3. 减少不必要的重新渲染
4. 优化图片资源
5. 使用 CDN 加速

### 代码质量
1. 遵循 ESLint 规则
2. 使用 Prettier 格式化代码
3. 编写单元测试
4. 添加类型注解（可选）

## 部署

### 构建生产版本

```bash
npm run build
```

### 输出目录

构建后的文件在 `dist/` 目录

### 部署到服务器

```bash
# 1. 复制 dist 文件到服务器
scp -r dist/* user@server:/path/to/deploy

# 2. 配置 Nginx
# 参考 FRONTEND_IMPLEMENTATION_GUIDE.md 中的 Nginx 配置
```

## 获取帮助

- 查看 `FRONTEND_PROGRESS.md` 了解完成情况
- 查看 `FRONTEND_IMPLEMENTATION_GUIDE.md` 了解详细开发指南
- 查看 `FRONTEND_TODO.md` 了解待完成任务
- 查看 `FRONTEND_SUMMARY.md` 了解项目总结

## 联系方式

如有问题或建议，请联系开发团队。

---

**快速启动指南**
最后更新: 2026-01-28
