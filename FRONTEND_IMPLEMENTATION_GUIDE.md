# Vue Web 前端 - 实现指南

## 项目概述

这是养生店管理系统的 Vue 3 前端实现，采用 Composition API 和现代化的项目结构。

## 目录结构

```
frontend/
├── src/
│   ├── api/                    # API 服务层
│   │   ├── auth.js            # 认证接口
│   │   ├── client.js          # HTTP 客户端
│   │   ├── customers.js       # 顾客管理接口
│   │   ├── products.js        # 产品管理接口
│   │   ├── orders.js          # 订单管理接口
│   │   ├── employees.js       # 员工管理接口
│   │   └── statistics.js      # 统计分析接口
│   ├── components/             # 组件目录
│   │   ├── Sidebar.vue        # 左侧导航栏
│   │   ├── HeaderBar.vue      # 顶部导航栏
│   │   ├── MetricCard.vue     # 指标卡片
│   │   ├── charts/            # 图表组件
│   │   │   ├── RevenueChart.vue
│   │   │   ├── ChannelChart.vue
│   │   │   ├── EmployeeRankingChart.vue
│   │   │   └── ProductRankingChart.vue
│   │   ├── dialogs/           # 对话框组件
│   │   │   └── CustomerDialog.vue
│   │   └── drawers/           # 抽屉组件
│   │       └── CustomerDrawer.vue
│   ├── layouts/                # 布局组件
│   │   └── MainLayout.vue     # 主布局容器
│   ├── pages/                  # 页面组件
│   │   ├── Login.vue          # 登录页
│   │   ├── Dashboard.vue      # 仪表板
│   │   ├── Customers.vue      # 顾客管理
│   │   ├── Products.vue       # 产品管理
│   │   ├── Orders.vue         # 订单管理 (待完成)
│   │   ├── Employees.vue      # 员工管理 (待完成)
│   │   └── Statistics.vue     # 数据统计 (待完成)
│   ├── router/                 # 路由配置
│   │   └── index.js
│   ├── store/                  # Pinia 状态管理
│   │   └── user.js
│   ├── styles/                 # 全局样式
│   │   ├── variables.scss     # CSS 变量
│   │   ├── global.scss        # 全局样式
│   │   └── mixins.scss        # SCSS 混合函数
│   ├── utils/                  # 工具函数
│   │   └── date.js            # 日期处理
│   ├── App.vue                # 根组件
│   └── main.js                # 入口文件
├── public/                     # 静态资源
├── index.html                 # HTML 入口
├── vite.config.js             # Vite 配置
├── package.json               # 项目依赖
└── .eslintrc.cjs              # ESLint 配置
```

## 已完成的功能

### ✓ 认证系统
- 登录页面（完整实现）
- Token 管理（localStorage）
- 路由守卫保护
- 自动重定向

### ✓ 仪表板
- 8个关键指标卡片
- 收入趋势线图表
- 渠道分布饼图表
- 员工排行柱状图
- 产品销售排行
- 最近订单表格
- 日期范围选择
- 数据刷新功能

### ✓ 顾客管理
- 顾客列表（搜索、筛选、分页）
- 新增/编辑顾客
- 删除顾客
- 顾客详情查看
- 消费记录展示
- 状态切换
- 数据导出

### ✓ 产品管理
- 产品列表（搜索、筛选、分页）
- 产品分类管理
- 新增/编辑产品
- 库存管理
- 删除产品
- 状态切换
- 数据导出

### ✓ 布局系统
- 响应式主布局
- 侧边栏导航
- 顶部导航栏（用户菜单、通知、搜索）
- 面包屑导航
- 用户登出

### ✓ 公共组件
- MetricCard 指标卡片
- 4个 ECharts 图表组件
- CustomerDialog 对话框
- CustomerDrawer 详情抽屉

### ✓ 样式系统
- CSS 变量定义（45+个）
- 全局样式（SCSS）
- SCSS 混合函数（30+个）
- Element Plus 主题覆盖
- 响应式设计工具类

### ✓ 工具函数
- 日期格式化
- 相对时间显示
- 日期范围获取

## 待完成的功能

### 优先级 P0（立即开始）

#### 1. 订单管理模块
- [ ] Orders.vue 页面
- [ ] OrderDialog.vue 对话框
- [ ] OrderPaymentDialog.vue 支付对话框
- [ ] OrderDrawer.vue 详情抽屉

#### 2. 员工管理模块
- [ ] Employees.vue 页面
- [ ] EmployeeDialog.vue 对话框
- [ ] EmployeeDrawer.vue 详情抽屉

#### 3. 数据统计模块
- [ ] Statistics.vue 页面
- [ ] 日收入趋势图表
- [ ] 周对比图表
- [ ] 客流量统计图表
- [ ] 渠道分析图表

#### 4. 产品管理对话框
- [ ] ProductDialog.vue
- [ ] CategoryDialog.vue
- [ ] StockDialog.vue

### 优先级 P1（之后）

#### 5. 通用公共组件
- [ ] Table.vue 数据表格组件
- [ ] SearchForm.vue 搜索表单
- [ ] Pagination.vue 分页组件
- [ ] Modal.vue 模态框
- [ ] ConfirmDialog.vue 确认框
- [ ] Upload.vue 上传组件

#### 6. 其他功能
- [ ] Profile.vue 个人资料页
- [ ] Settings.vue 系统设置页
- [ ] 权限管理系统
- [ ] 操作日志

## 开发指南

### 创建新页面

```vue
<template>
  <main-layout>
    <div class="page-name">
      <!-- 页面内容 -->
    </div>
  </main-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import MainLayout from '@/layouts/MainLayout.vue'
import * as api from '@/api/moduleName'

// 数据
const loading = ref(false)
const data = ref([])

// 方法
const loadData = async () => {
  loading.value = true
  try {
    const response = await api.getList()
    data.value = response
  } catch (error) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

// 生命周期
onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
// 页面样式
</style>
```

### 创建新组件

```vue
<template>
  <div class="component-name">
    <!-- 组件内容 -->
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// Props
const props = defineProps({
  title: String,
  value: [String, Number],
})

// Emits
const emit = defineEmits(['update:value', 'change'])

// 响应式数据
const loading = ref(false)

// 计算属性
const displayValue = computed(() => {
  return props.value || '-'
})

// 方法
const handleClick = () => {
  emit('change')
}
</script>

<style scoped lang="scss">
// 组件样式
</style>
```

### API 调用示例

```javascript
// 在页面或组件中使用
import * as customersApi from '@/api/customers'

// 获取列表
const response = await customersApi.getCustomers({
  skip: 0,
  limit: 20,
  search: 'keyword'
})

// 创建
await customersApi.createCustomer({
  name: '张三',
  phone: '13800138000'
})

// 更新
await customersApi.updateCustomer(id, {
  name: '李四'
})

// 删除
await customersApi.deleteCustomer(id)
```

### 状态管理示例

```javascript
import { useUserStore } from '@/store/user'

export default {
  setup() {
    const userStore = useUserStore()

    // 访问状态
    const user = userStore.user
    const isAuthenticated = userStore.isAuthenticated

    // 调用 action
    const handleLogout = () => {
      userStore.logout()
    }

    return { user, isAuthenticated, handleLogout }
  }
}
```

## 样式使用指南

### CSS 变量

```scss
// 在组件中使用
.component {
  color: $text-primary;
  background-color: $bg-light;
  border: 1px solid $border-color;
  border-radius: $border-radius-base;
  box-shadow: $shadow-base;
  transition: $transition-base;
  padding: $space-lg;
}
```

### SCSS 混合函数

```scss
.flex-container {
  @include flex-center; // 居中
}

.text {
  @include text-truncate; // 单行截断
  @include text-multiline-truncate(3); // 3行截断
}

.card {
  @include card-style(6px, 16px); // 卡片样式
}

// 响应式
@include respond-to('md') {
  // 768px 及以下
}

@include respond-at-least('lg') {
  // 992px 及以上
}
```

## 项目依赖

```json
{
  "vue": "^3.3.13",
  "vue-router": "^4.2.5",
  "pinia": "^2.1.6",
  "axios": "^1.6.5",
  "element-plus": "^2.4.4",
  "echarts": "^5.4.3",
  "date-fns": "^2.30.0",
  "sass": "^1.70.0"
}
```

## 开发和构建

### 开发模式

```bash
cd frontend
npm install
npm run dev
```

访问 `http://localhost:5173`

### 生产构建

```bash
npm run build
```

### 代码检查

```bash
npm run lint
```

## 路由配置

当前路由结构：

```
/login                    - 登录页
/ (MainLayout)
  ├── /dashboard          - 仪表板
  ├── /customers          - 顾客管理
  ├── /products           - 产品管理
  ├── /orders             - 订单管理
  ├── /employees          - 员工管理
  └── /statistics         - 数据统计
```

## 性能优化建议

### 代码分割
```javascript
// 路由懒加载已实现
component: () => import('../pages/Dashboard.vue')
```

### 图片优化
- 使用 WebP 格式
- 设置合适的尺寸
- 添加 loading 占位符

### 缓存策略
- 利用浏览器缓存
- API 响应缓存
- Pinia 状态管理缓存

### 虚拟列表
对于大数据列表使用虚拟列表库（如 vue-virtual-list）

## 常见问题

### Q: 如何修改 API 地址？
A: 修改 `vite.config.js` 中的 proxy 配置

### Q: 如何添加新的菜单项？
A: 编辑 `src/components/Sidebar.vue` 中的菜单配置

### Q: 如何修改 Element Plus 主题？
A: 编辑 `src/styles/global.scss` 中的 `:root` CSS 变量

### Q: 如何处理 API 错误？
A: 在 `src/api/client.js` 中已配置统一的错误处理

## 测试

### 单元测试（待实现）
```bash
npm run test:unit
```

### E2E 测试（待实现）
```bash
npm run test:e2e
```

## 部署

### 构建
```bash
npm run build
```

### 推送到 CDN
将 `dist/` 目录中的文件上传到 CDN

### Nginx 配置
```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        root /var/www/wellness-shop-system/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
    }
}
```

## 文档链接

- [Vue 3 官方文档](https://vuejs.org/)
- [Vue Router 文档](https://router.vuejs.org/)
- [Pinia 文档](https://pinia.vuejs.org/)
- [Element Plus 文档](https://element-plus.org/)
- [ECharts 文档](https://echarts.apache.org/)

## 贡献指南

### 代码风格
- 遵循 Airbnb JavaScript 规范
- 使用 ESLint 和 Prettier
- 添加必要的代码注释

### 提交信息
```
feat: 添加新功能
fix: 修复 bug
docs: 更新文档
style: 代码格式化
refactor: 代码重构
perf: 性能优化
test: 添加测试
```

## 版本历史

- v1.0.0 (2026-01-28) - 初始版本，完成登录、仪表板、顾客和产品管理

## 维护者

- 开发团队

## 许可证

MIT

---

**最后更新**: 2026-01-28
**前端完成度**: 约 40%
**下一个目标**: 完成订单、员工、统计模块
