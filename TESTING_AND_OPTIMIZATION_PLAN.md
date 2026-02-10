# 测试和优化计划（详细）

**项目**: 养生店管理系统
**日期**: 2026-01-28
**作者**: DeepV Code AI Assistant
**专注范围**: 测试和优化模块

---

## 📋 概述

本文档定义了**测试和优化**阶段的完整计划，包括：
- ✓ 3个后端测试任务
- ✓ 2个前端测试任务
- ✓ 2个样式优化任务

**总计**: 7个任务，预计25小时

---

## 🧪 第一部分：后端测试与优化

### Task T-001: 后端单元测试 (5小时)

**目标**: 编写后端数据模型和业务逻辑的单元测试

#### 测试范围
1. **数据模型测试**
   - User 模型（密码加密、验证）
   - Customer 模型（字段验证）
   - Product 模型（库存计算）
   - Order/OrderItem 模型（金额计算）
   - Employee 模型（绩效计算）
   - 其他模型（6个）

2. **业务逻辑测试**
   - 认证服务 (auth_service.py)
     - 密码哈希和验证
     - JWT 令牌生成和验证
     - 用户认证流程
   - 安全工具 (security.py)
     - 密码加密
     - 权限检查

3. **Schema 验证测试**
   - Pydantic 模式验证
   - 边界值测试
   - 错误消息验证

#### 实现步骤
```
1. 安装测试框架和依赖
   - pytest
   - pytest-asyncio
   - pytest-cov (代码覆盖率)
   - factory-boy (测试数据工厂)

2. 创建测试文件
   tests/
   ├── __init__.py
   ├── conftest.py                 # 测试配置和 fixtures
   ├── test_models/
   │   ├── __init__.py
   │   ├── test_user.py            # User 模型测试
   │   ├── test_customer.py        # Customer 模型测试
   │   ├── test_product.py         # Product 模型测试
   │   ├── test_order.py           # Order 模型测试
   │   ├── test_employee.py        # Employee 模型测试
   │   └── test_*.py               # 其他模型
   ├── test_schemas/
   │   ├── __init__.py
   │   ├── test_user_schema.py     # User Schema 验证
   │   ├── test_customer_schema.py
   │   ├── test_product_schema.py
   │   └── test_*.py
   └── test_services/
       ├── __init__.py
       └── test_auth_service.py    # 认证服务测试

3. 编写测试用例
   - 正常流程测试 (happy path)
   - 边界值测试 (boundary)
   - 异常处理测试 (error cases)
   - 验证规则测试 (validation)

4. 测试覆盖率目标
   - 模型: >= 90%
   - Services: >= 85%
   - Utils: >= 80%
   - 总体: >= 85%
```

#### 预期输出
- ✓ 40+ 个单元测试
- ✓ >= 85% 代码覆盖率
- ✓ pytest 覆盖率报告

---

### Task T-002: 后端集成测试 (5小时)

**目标**: 编写后端 API 端点的集成测试

#### 测试范围
1. **认证 API 测试** (endpoints/auth.py)
   - POST /auth/login - 登录
   - POST /auth/logout - 登出
   - POST /auth/refresh - 刷新 token
   - 权限验证

2. **健康检查测试** (endpoints/health.py)
   - GET /health/status
   - 数据库连接检查

3. **数据库操作测试**
   - CRUD 操作
   - 事务处理
   - 关联关系验证

#### 实现步骤
```
1. 创建集成测试配置
   - 测试数据库配置（SQLite 内存数据库）
   - 测试数据库初始化
   - 测试 fixtures

2. 创建测试文件
   tests/
   ├── test_api/
   │   ├── __init__.py
   │   ├── test_auth.py            # 认证 API 测试
   │   └── test_health.py          # 健康检查测试
   └── test_database/
       ├── __init__.py
       ├── test_crud.py            # CRUD 操作测试
       └── test_transactions.py    # 事务测试

3. 编写测试用例
   - API 端点测试
   - 请求/响应验证
   - 状态码检查
   - 错误响应处理

4. 测试覆盖率
   - API 端点: >= 90%
   - 总体: >= 80%
```

#### 预期输出
- ✓ 20+ 个集成测试
- ✓ API 端点覆盖 >= 90%
- ✓ pytest 集成测试报告

---

### Task T-003: 性能测试和优化 (4小时)

**目标**: 性能分析和优化

#### 优化范围
1. **数据库查询优化**
   - 识别 N+1 查询问题
   - 添加数据库索引
   - 查询优化
   - 使用 eager loading

2. **缓存优化**
   - Redis 集成
   - 查询结果缓存
   - 缓存失效策略

3. **性能监控**
   - 添加性能日志
   - 查询耗时统计
   - 慢查询追踪

#### 实现步骤
```
1. 性能分析
   - 使用 sqlalchemy 查询计时
   - 使用 Python cProfile 分析
   - 使用 pytest-benchmark

2. 优化措施
   - 添加数据库索引
   - 优化 ORM 查询
   - 实现查询缓存
   - 异步优化

3. 创建文件
   backend/app/core/
   ├── performance.py              # 性能监控工具
   ├── cache.py                    # 缓存管理

   tests/
   └── test_performance/
       ├── __init__.py
       └── test_queries.py         # 查询性能测试

4. 性能目标
   - 平均 API 响应时间 < 200ms
   - 95% 请求 < 500ms
   - 数据库查询 < 100ms
```

#### 预期输出
- ✓ 性能优化建议文档
- ✓ 优化后的数据库索引
- ✓ 缓存实现代码
- ✓ 性能基准测试报告

---

## 🎨 第二部分：前端测试与优化

### Task T-004: 前端组件单元测试 (3小时)

**目标**: 使用 Vitest 和 Vue Test Utils 编写组件测试

#### 测试范围
1. **页面组件测试**
   - Login.vue - 登录页面
   - Dashboard.vue - 仪表板
   - Customers.vue - 顾客管理
   - Products.vue - 产品管理

2. **公共组件测试**
   - MetricCard.vue - 指标卡片
   - 图表组件（4个）
   - 布局组件（3个）
   - CustomerDialog.vue

3. **API 客户端测试**
   - HTTP 拦截器
   - API 调用测试
   - 错误处理

#### 实现步骤
```
1. 安装测试框架
   - Vitest
   - Vue Test Utils
   - Happy DOM 或 jsdom
   - @testing-library/vue (可选)

2. 配置 Vite
   - vite.config.js - 添加 Vitest 配置
   - vitest.config.js (可选)

3. 创建测试文件
   frontend/src/
   ├── __tests__/
   │   ├── __snapshots__/
   │   ├── components/
   │   │   ├── MetricCard.spec.js
   │   │   ├── RevenueChart.spec.js
   │   │   └── *.spec.js
   │   ├── pages/
   │   │   ├── Login.spec.js
   │   │   ├── Dashboard.spec.js
   │   │   ├── Customers.spec.js
   │   │   └── Products.spec.js
   │   ├── api/
   │   │   └── client.spec.js
   │   └── utils/
   │       └── date.spec.js

4. 编写测试用例
   - 组件挂载测试
   - Props 验证
   - 事件发出测试
   - 用户交互测试
   - 快照测试

5. 测试覆盖率目标
   - 组件: >= 80%
   - 页面: >= 75%
   - 总体: >= 75%
```

#### 预期输出
- ✓ 30+ 个组件测试
- ✓ >= 75% 代码覆盖率
- ✓ 快照文件
- ✓ Vitest 覆盖率报告

---

### Task T-005: 前端集成测试 (3小时)

**目标**: 测试页面流程和 API 交互

#### 测试范围
1. **路由测试**
   - 路由导航
   - 路由守卫
   - 权限检查
   - 重定向

2. **状态管理测试**
   - Pinia store 测试
   - 用户状态更新
   - 认证状态保存

3. **端到端流程测试**
   - 登录流程
   - 页面导航流程
   - 数据加载流程

#### 实现步骤
```
1. 创建集成测试文件
   frontend/src/__tests__/
   ├── integration/
   │   ├── login.spec.js          # 登录流程
   │   ├── navigation.spec.js     # 路由导航
   │   └── store.spec.js          # 状态管理
   └── e2e/ (可选)
       └── workflows.spec.js

2. 配置测试环境
   - Mock API 调用
   - 模拟 localStorage
   - 模拟路由

3. 编写测试用例
   - 完整用户流程
   - 页面交互流程
   - 状态更新流程

4. 测试覆盖率
   - 路由: 100%
   - 主要流程: >= 80%
```

#### 预期输出
- ✓ 15+ 个集成测试
- ✓ >= 80% 流程覆盖率
- ✓ Vitest 集成测试报告

---

## 🎯 第三部分：样式和响应式优化

### Task T-006: 完善 CSS 样式系统 (3小时)

**目标**: 建立完整的 CSS 变量系统和全局样式

#### 优化内容
1. **CSS 变量定义**
   ```scss
   // frontend/src/styles/variables.scss

   // 色彩系统
   $primary-color: #409EFF;
   $success-color: #67C26A;
   $warning-color: #E6A23C;
   $danger-color: #F56C6C;
   $error-color: #F56C6C;
   $info-color: #909399;

   // 灰度
   $color-white: #FFFFFF;
   $color-black: #000000;
   $color-gray-1: #F5F7FA;      // 背景
   $color-gray-2: #EBF0F5;      // 次背景
   $color-gray-3: #DFE4E8;      // 边框
   $color-gray-4: #BFBFBF;      // 文本

   // 间距系统
   $spacing-xs: 4px;
   $spacing-sm: 8px;
   $spacing-md: 16px;
   $spacing-lg: 24px;
   $spacing-xl: 32px;
   $spacing-xxl: 48px;

   // 圆角
   $radius-sm: 2px;
   $radius-md: 4px;
   $radius-lg: 8px;

   // 字体
   $font-size-xs: 12px;
   $font-size-sm: 14px;
   $font-size-base: 16px;
   $font-size-lg: 18px;
   $font-size-xl: 20px;

   // 阴影
   $shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
   $shadow-md: 0 2px 8px rgba(0, 0, 0, 0.15);
   $shadow-lg: 0 4px 12px rgba(0, 0, 0, 0.2);

   // 过渡
   $transition-fast: 0.15s ease;
   $transition-normal: 0.3s ease;
   $transition-slow: 0.5s ease;

   // 断点
   $breakpoint-xs: 480px;
   $breakpoint-sm: 768px;
   $breakpoint-md: 992px;
   $breakpoint-lg: 1200px;
   $breakpoint-xl: 1408px;
   ```

2. **混合函数 (Mixins)**
   ```scss
   // frontend/src/styles/mixins.scss

   // 响应式设计
   @mixin respond-to($breakpoint) {
     @if $breakpoint == 'xs' { @media (max-width: 480px) { @content; } }
     @else if $breakpoint == 'sm' { @media (max-width: 768px) { @content; } }
     @else if $breakpoint == 'md' { @media (max-width: 992px) { @content; } }
     @else if $breakpoint == 'lg' { @media (max-width: 1200px) { @content; } }
   }

   // 文本截断
   @mixin text-truncate($lines: 1) {
     @if $lines == 1 {
       overflow: hidden;
       text-overflow: ellipsis;
       white-space: nowrap;
     } @else {
       display: -webkit-box;
       -webkit-box-orient: vertical;
       -webkit-line-clamp: $lines;
       overflow: hidden;
     }
   }

   // Flex 布局
   @mixin flex-center {
     display: flex;
     align-items: center;
     justify-content: center;
   }

   @mixin flex-between {
     display: flex;
     align-items: center;
     justify-content: space-between;
   }

   // 绝对居中
   @mixin absolute-center {
     position: absolute;
     top: 50%;
     left: 50%;
     transform: translate(-50%, -50%);
   }

   // 卡片样式
   @mixin card($padding: $spacing-lg) {
     background: $color-white;
     border-radius: $radius-lg;
     box-shadow: $shadow-md;
     padding: $padding;
   }
   ```

3. **全局样式重置**
   ```scss
   // frontend/src/styles/global.scss

   * {
     margin: 0;
     padding: 0;
     box-sizing: border-box;
   }

   html, body {
     width: 100%;
     height: 100%;
     font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
     font-size: $font-size-base;
     line-height: 1.5;
     color: #333;
     background: #f5f7fa;
   }

   // Element Plus 主题覆盖
   :root {
     --el-color-primary: #409EFF;
     --el-color-success: #67C26A;
     --el-color-warning: #E6A23C;
     --el-color-danger: #F56C6C;
     --el-border-radius-base: 4px;
     --el-border-radius-small: 2px;
     --el-border-radius-round: 20px;
   }
   ```

4. **实用类 (Utilities)**
   ```scss
   // 显示/隐藏
   .hidden { display: none !important; }
   .visible { display: block !important; }

   // 文本对齐
   .text-left { text-align: left; }
   .text-center { text-align: center; }
   .text-right { text-align: right; }

   // 溢出处理
   .truncate { @include text-truncate(); }
   .truncate-2 { @include text-truncate(2); }

   // 间距工具
   @for $i from 1 through 12 {
     .mt-#{$i * 2} { margin-top: $i * 2px; }
     .mb-#{$i * 2} { margin-bottom: $i * 2px; }
     .ml-#{$i * 2} { margin-left: $i * 2px; }
     .mr-#{$i * 2} { margin-right: $i * 2px; }
     .pt-#{$i * 2} { padding-top: $i * 2px; }
     .pb-#{$i * 2} { padding-bottom: $i * 2px; }
     .pl-#{$i * 2} { padding-left: $i * 2px; }
     .pr-#{$i * 2} { padding-right: $i * 2px; }
   }

   // Flex 工具
   .flex { display: flex; }
   .flex-1 { flex: 1; }
   .flex-center { @include flex-center; }
   .flex-between { @include flex-between; }
   ```

#### 实现步骤
```
1. 创建或更新样式文件
   frontend/src/styles/
   ├── variables.scss             # CSS 变量
   ├── mixins.scss                # SCSS 混合函数
   ├── global.scss                # 全局样式
   ├── utilities.scss             # 实用类
   ├── themes/                    # 主题文件夹
   │   ├── light.scss            # 亮色主题
   │   └── dark.scss             # 暗色主题（可选）
   └── reset.scss                # CSS 重置

2. 更新 main.js
   import './styles/global.scss'

3. 更新组件样式
   - 使用 CSS 变量替代硬编码值
   - 使用 mixin 简化代码
   - 使用实用类

4. 主题定制
   - 支持主题切换
   - 保存主题偏好
```

#### 预期输出
- ✓ 完整的 CSS 变量系统
- ✓ SCSS 混合函数库
- ✓ 全局样式和重置
- ✓ 实用类和工具函数

---

### Task T-007: 响应式设计适配 (2小时)

**目标**: 实现完整的响应式设计，支持移动端和平板端

#### 响应式范围
1. **布局适配**
   ```
   >= 1200px (桌面): 完整布局
   992px - 1199px (小桌面): 微调
   768px - 991px (平板): 堆叠布局
   480px - 767px (小屏): 单列布局
   < 480px (手机): 紧凑布局
   ```

2. **组件适配**
   - 导航栏：响应式菜单（汉堡菜单）
   - 表格：响应式卡片视图
   - 表单：单列表单
   - 图表：自适应宽度

#### 实现步骤
```
1. MainLayout 适配
   - 侧边栏: 桌面显示，小屏隐藏（抽屉式）
   - 顶部栏: 调整高度和间距
   - 内容区: 响应式填充

2. 表格适配
   - 桌面: 完整表格
   - 平板: 可滚动表格
   - 手机: 卡片视图（竖排显示）

3. 表单适配
   - 桌面: 多列表单
   - 手机: 单列表单

4. 图表适配
   - 自适应高度和宽度
   - 响应式图例位置

5. 文本适配
   - 字体大小自适应
   - 行高和间距调整

6. 测试设备
   - iPhone SE (375px)
   - iPhone 12 (390px)
   - iPad (768px)
   - iPad Pro (1024px)
   - 桌面 (1920px)
```

#### 实现例子
```vue
<!-- MainLayout.vue 示例 -->
<template>
  <div class="main-layout">
    <!-- 汉堡菜单 (仅在小屏显示) -->
    <button
      class="hamburger-menu"
      @click="sidebarOpen = !sidebarOpen"
      v-show="isMobile"
    >
      <el-icon><Menu /></el-icon>
    </button>

    <!-- 侧边栏 (移动端隐藏) -->
    <aside
      class="sidebar"
      :class="{ open: sidebarOpen && isMobile }"
    >
      <Sidebar />
    </aside>

    <!-- 主内容 -->
    <main class="main-content">
      <HeaderBar />
      <div class="content-wrapper">
        <router-view />
      </div>
    </main>
  </div>
</template>

<style lang="scss" scoped>
.main-layout {
  display: flex;
  height: 100vh;

  .hamburger-menu {
    position: fixed;
    top: 20px;
    left: 20px;
    z-index: 1000;
    background: white;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 8px;
    cursor: pointer;
  }

  .sidebar {
    width: 250px;
    background: white;
    border-right: 1px solid #ddd;
    overflow-y: auto;
    transition: transform 0.3s ease;

    @include respond-to('sm') {
      position: fixed;
      left: 0;
      top: 0;
      height: 100vh;
      z-index: 999;
      transform: translateX(-100%);

      &.open {
        transform: translateX(0);
      }
    }
  }

  .main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;

    @include respond-to('sm') {
      margin-left: 0;
    }
  }

  .content-wrapper {
    flex: 1;
    overflow-y: auto;
    padding: 20px;

    @include respond-to('sm') {
      padding: 10px;
    }
  }
}
</style>
```

#### 预期输出
- ✓ 响应式布局组件
- ✓ 移动端菜单
- ✓ 响应式表格和表单
- ✓ 响应式图表
- ✓ 适配多种设备尺寸的样式

---

## 📊 测试和优化摘要

| 任务 | 类型 | 预计时间 | 优先级 | 状态 |
|-----|------|---------|--------|------|
| T-001 | 后端单元测试 | 5h | High | 待开始 |
| T-002 | 后端集成测试 | 5h | High | 待开始 |
| T-003 | 后端性能优化 | 4h | High | 待开始 |
| T-004 | 前端组件测试 | 3h | High | 待开始 |
| T-005 | 前端集成测试 | 3h | High | 待开始 |
| T-006 | CSS 样式系统 | 3h | Medium | 待开始 |
| T-007 | 响应式设计 | 2h | Medium | 待开始 |
| **总计** | | **25h** | | **0/7** |

---

## 🚀 执行顺序

### 第1阶段 (5-6小时) - 后端测试
1. **Task T-001**: 后端单元测试
   - 建立测试基础结构
   - 编写模型和服务测试
   - 验证测试覆盖率

2. **Task T-002**: 后端集成测试
   - 编写 API 端点测试
   - 测试数据库操作
   - 验证端点响应

### 第2阶段 (3-4小时) - 后端优化
3. **Task T-003**: 性能优化
   - 数据库查询优化
   - 缓存实现
   - 性能基准测试

### 第3阶段 (6小时) - 前端测试
4. **Task T-004**: 前端组件测试
   - 配置 Vitest
   - 编写组件测试
   - 验证测试覆盖率

5. **Task T-005**: 前端集成测试
   - 路由和状态管理测试
   - 用户流程测试

### 第4阶段 (5小时) - 前端优化
6. **Task T-006**: CSS 样式系统
   - 定义 CSS 变量
   - 创建混合函数
   - 全局样式和实用类

7. **Task T-007**: 响应式设计
   - 布局适配
   - 组件适配
   - 多设备测试

---

## 📝 注意事项

1. **测试框架选择**
   - 后端: pytest (已有 pytest.ini)
   - 前端: Vitest (适合 Vite 项目)

2. **代码覆盖率目标**
   - 后端: >= 85%
   - 前端: >= 75%

3. **性能目标**
   - API 响应时间 < 200ms (平均)
   - 页面加载时间 < 3s
   - 首屏渲染 < 1s

4. **浏览器兼容性**
   - Chrome >= 90
   - Firefox >= 88
   - Safari >= 14
   - Edge >= 90

5. **响应式断点**
   使用统一的断点定义，避免冲突

---

## 📚 参考资源

### 后端测试
- [pytest 官方文档](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [FastAPI 测试](https://fastapi.tiangolo.com/tutorial/testing/)

### 前端测试
- [Vitest 官方文档](https://vitest.dev/)
- [Vue Test Utils](https://test-utils.vuejs.org/)
- [Testing Library](https://testing-library.com/docs/vue-testing-library/intro)

### 样式和设计
- [SCSS 官方文档](https://sass-lang.com/documentation)
- [Element Plus 主题定制](https://element-plus.org/zh-CN/guide/dev-guide.html#%E4%B8%BB%E9%A2%98%E8%AE%BE%E8%AE%A1)
- [响应式设计最佳实践](https://web.dev/responsive-web-design-basics/)

---

**版本**: 1.0
**最后更新**: 2026-01-28
**作者**: DeepV Code AI
**状态**: 计划已制定，待实施
