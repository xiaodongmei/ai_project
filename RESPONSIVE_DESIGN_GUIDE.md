# 响应式设计适配指南

## 🎯 概述

本文档定义了前端项目的响应式设计实现方案，支持从超小屏幕到超大屏幕的完整适配。

---

## 📱 断点定义

| 断点 | 范围 | 设备类型 | 用途 |
|-----|------|---------|------|
| **xs** | < 480px | 手机竖屏 | 最小化布局 |
| **sm** | 480px - 767px | 手机横屏/小平板 | 堆叠布局 |
| **md** | 768px - 991px | 平板设备 | 两列布局 |
| **lg** | 992px - 1199px | 小桌面 | 标准桌面布局 |
| **xl** | 1200px - 1407px | 桌面 | 宽屏布局 |
| **2xl** | >= 1408px | 宽屏桌面/4K | 超宽布局 |

### CSS Media Queries

```scss
// 使用提供的 mixin
@include respond-to('sm') {
  // 768px 及以下的样式
}

// 或直接使用 media query
@media (max-width: 767px) {
  // 样式
}
```

---

## 🏗️ 布局适配方案

### 1. MainLayout 响应式调整

#### 桌面布局 (>= 992px)

```vue
<template>
  <div class="main-layout">
    <aside class="sidebar"><!-- 左侧导航栏 --></aside>
    <main class="main-content">
      <header class="header-bar"><!-- 顶部栏 --></header>
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
}

.sidebar {
  width: 250px;
  background: white;
  border-right: 1px solid #ddd;
  overflow-y: auto;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.header-bar {
  height: 60px;
  border-bottom: 1px solid #ddd;
}

.content-wrapper {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}
</style>
```

#### 平板布局 (768px - 991px)

```scss
@include respond-to('md') {
  .main-layout {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    height: 60px;
    border-right: none;
    border-bottom: 1px solid #ddd;
    padding: 0 20px;

    // 导航项横排显示
    .nav-items {
      display: flex;
      flex-direction: row;
    }
  }

  .main-content {
    flex: 1;
  }

  .header-bar {
    display: none; // 或者合并到侧边栏
  }

  .content-wrapper {
    padding: 16px;
  }
}
```

#### 手机布局 (< 768px)

```scss
@include respond-to('sm') {
  .main-layout {
    flex-direction: column;
  }

  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    width: 250px;
    height: 100vh;
    z-index: 999;
    transform: translateX(-100%);
    transition: transform 0.3s ease;

    &.open {
      transform: translateX(0);
    }
  }

  .main-content {
    flex: 1;
  }

  .hamburger-menu {
    position: fixed;
    top: 10px;
    left: 10px;
    z-index: 1000;
  }

  .content-wrapper {
    padding: 12px;
  }
}
```

---

## 📊 表格响应式适配

### 桌面表格 (>= 768px)

```vue
<template>
  <table class="table">
    <thead>
      <tr>
        <th>ID</th>
        <th>名称</th>
        <th>邮箱</th>
        <th>电话</th>
        <th>操作</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="item in items" :key="item.id">
        <td>{{ item.id }}</td>
        <td>{{ item.name }}</td>
        <td>{{ item.email }}</td>
        <td>{{ item.phone }}</td>
        <td>
          <button>编辑</button>
          <button>删除</button>
        </td>
      </tr>
    </tbody>
  </table>
</template>
```

### 移动端卡片视图 (< 768px)

```vue
<template>
  <div class="table-mobile">
    <div v-for="item in items" :key="item.id" class="card-item">
      <div class="card-row">
        <span class="label">ID:</span>
        <span class="value">{{ item.id }}</span>
      </div>
      <div class="card-row">
        <span class="label">名称:</span>
        <span class="value">{{ item.name }}</span>
      </div>
      <div class="card-row">
        <span class="label">邮箱:</span>
        <span class="value text-truncate">{{ item.email }}</span>
      </div>
      <div class="card-row">
        <span class="label">电话:</span>
        <span class="value">{{ item.phone }}</span>
      </div>
      <div class="card-actions">
        <button>编辑</button>
        <button>删除</button>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.card-item {
  margin-bottom: 16px;
  padding: 16px;
  background: white;
  border-radius: 8px;
  border: 1px solid #ddd;
}

.card-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;

  &:last-child {
    border-bottom: none;
  }
}

.label {
  font-weight: 500;
  color: #666;
  min-width: 60px;
}

.value {
  flex: 1;
  text-align: right;
  color: #333;
}

.card-actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;

  button {
    flex: 1;
  }
}
</style>
```

### SCSS 隐藏/显示表格

```scss
.table {
  @include respond-to('sm') {
    display: none;
  }
}

.table-mobile {
  display: none;

  @include respond-to('sm') {
    display: block;
  }
}
```

---

## 📝 表单响应式适配

### 桌面表单 (多列)

```vue
<template>
  <form class="form-grid">
    <div class="form-group">
      <label>姓名</label>
      <input type="text" />
    </div>
    <div class="form-group">
      <label>邮箱</label>
      <input type="email" />
    </div>
    <div class="form-group">
      <label>电话</label>
      <input type="tel" />
    </div>
    <div class="form-group">
      <label>地址</label>
      <input type="text" />
    </div>
  </form>
</template>

<style lang="scss" scoped>
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
</style>
```

### 移动表单 (单列)

```scss
@include respond-to('md') {
  .form-grid {
    grid-template-columns: 1fr;
  }
}

@include respond-to('sm') {
  .form-grid {
    gap: 12px;
  }

  .form-group {
    label {
      font-size: 14px;
      margin-bottom: 6px;
    }

    input {
      padding: 8px 10px;
      font-size: 16px; // iOS 防止自动缩放
    }
  }
}
```

---

## 📈 图表响应式适配

### ECharts 容器

```vue
<template>
  <div class="chart-container">
    <div ref="chartRef" class="chart"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onResized } from 'vue'
import * as echarts from 'echarts'

const chartRef = ref(null)
let chart = null

onMounted(() => {
  chart = echarts.init(chartRef.value)
  chart.setOption(getOption())

  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    chart.resize()
  })
})
</script>

<style lang="scss" scoped>
.chart-container {
  width: 100%;
  height: 400px;

  @include respond-to('md') {
    height: 300px;
  }

  @include respond-to('sm') {
    height: 250px;
  }
}

.chart {
  width: 100%;
  height: 100%;
}
</style>
```

---

## 🔤 字体和间距响应式调整

### 字号自适应

```scss
h1 {
  font-size: 32px;

  @include respond-to('md') {
    font-size: 28px;
  }

  @include respond-to('sm') {
    font-size: 24px;
  }

  @include respond-to('xs') {
    font-size: 20px;
  }
}

p {
  font-size: 16px;
  line-height: 1.6;

  @include respond-to('sm') {
    font-size: 14px;
    line-height: 1.5;
  }
}
```

### 间距自适应

```scss
.container {
  padding: 32px;

  @include respond-to('lg') {
    padding: 24px;
  }

  @include respond-to('md') {
    padding: 16px;
  }

  @include respond-to('sm') {
    padding: 12px;
  }
}

.section {
  margin-bottom: 24px;

  @include respond-to('sm') {
    margin-bottom: 16px;
  }
}
```

---

## 🧭 导航菜单响应式

### 桌面导航 (竖排)

```vue
<template>
  <aside class="sidebar">
    <nav class="nav">
      <router-link to="/" class="nav-item">
        <i class="icon-dashboard"></i>
        <span>仪表板</span>
      </router-link>
      <router-link to="/customers" class="nav-item">
        <i class="icon-customers"></i>
        <span>顾客管理</span>
      </router-link>
      <!-- 更多菜单项 -->
    </nav>
  </aside>
</template>

<style lang="scss" scoped>
.sidebar {
  width: 250px;
}

.nav {
  display: flex;
  flex-direction: column;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  color: #666;
  text-decoration: none;
  transition: all 0.3s;

  &:hover,
  &.router-link-active {
    background: #f0f0f0;
    color: #409EFF;
  }

  span {
    display: block;
  }
}
</style>
```

### 平板导航 (水平)

```scss
@include respond-to('md') {
  .sidebar {
    width: 100%;
    height: auto;
  }

  .nav {
    flex-direction: row;
    overflow-x: auto;
    flex-wrap: nowrap;
  }

  .nav-item {
    flex-shrink: 0;
    flex-direction: column;
    text-align: center;
    border-right: 1px solid #f0f0f0;

    span {
      font-size: 12px;
      margin-top: 4px;
    }
  }
}
```

### 手机导航 (抽屉)

```scss
@include respond-to('sm') {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    width: 80%;
    height: 100vh;
    z-index: 999;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    background: white;
    box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);

    &.open {
      transform: translateX(0);
    }
  }

  .nav {
    flex-direction: column;
  }

  .nav-item {
    flex-direction: row;
    border-right: none;
    border-bottom: 1px solid #f0f0f0;
    text-align: left;
  }
}
```

---

## 📱 触摸屏优化

### 按钮大小

```scss
// 桌面：默认 36px
button {
  min-height: 36px;
  padding: 8px 16px;
}

// 移动设备：建议 44px（Apple 建议）
@include respond-to('sm') {
  button {
    min-height: 44px;
    padding: 10px 16px;
    font-size: 16px; // iOS 防止自动缩放
  }
}
```

### 链接点击区域

```scss
a {
  padding: 8px;

  @include respond-to('sm') {
    padding: 12px; // 增大触摸区域
    min-height: 44px;
    display: flex;
    align-items: center;
  }
}
```

### 禁用 iOS 放大

```html
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
```

---

## 🖼️ 图片和媒体响应式

### 响应式图片

```vue
<template>
  <picture>
    <source media="(max-width: 767px)" srcset="image-mobile.jpg">
    <source media="(min-width: 768px)" srcset="image-desktop.jpg">
    <img src="image-desktop.jpg" alt="Description">
  </picture>
</template>
```

### 背景图片

```scss
.hero {
  background-image: url('/images/hero-desktop.jpg');
  background-size: cover;
  background-position: center;
  height: 500px;

  @include respond-to('md') {
    background-image: url('/images/hero-tablet.jpg');
    height: 400px;
  }

  @include respond-to('sm') {
    background-image: url('/images/hero-mobile.jpg');
    height: 300px;
  }
}
```

---

## 🧪 测试响应式设计

### 使用浏览器开发者工具

1. 打开 Chrome DevTools（F12）
2. 点击设备切换按钮（Ctrl+Shift+M）
3. 选择不同的设备预设
4. 手动调整宽度测试

### 测试断点

```bash
# 测试 xs 断点 (320px)
# 测试 sm 断点 (480px)
# 测试 md 断点 (768px)
# 测试 lg 断点 (992px)
# 测试 xl 断点 (1200px)
# 测试 2xl 断点 (1408px)
```

### 设备清单

- iPhone SE (375px)
- iPhone 12 (390px)
- iPhone 14 Pro (393px)
- Pixel 5 (393px)
- iPad (768px)
- iPad Air (1024px)
- iPad Pro (1024px)
- 桌面 (1920px)
- 4K (2560px)

---

## 🚀 最佳实践

### 1. 移动优先

从小屏幕开始设计，逐步增强功能：

```scss
// 基础移动样式
.card {
  padding: 12px;
  font-size: 14px;
}

// 增强平板样式
@media (min-width: 768px) {
  .card {
    padding: 16px;
    font-size: 16px;
  }
}

// 增强桌面样式
@media (min-width: 1200px) {
  .card {
    padding: 20px;
    font-size: 18px;
  }
}
```

### 2. 灵活单位

使用相对单位而非固定像素：

```scss
// ✓ 好
width: 100%;
padding: 1rem;
font-size: 1.5em;

// ✗ 避免
width: 1200px;
padding: 16px;
font-size: 18px;
```

### 3. Flexbox 和 Grid

使用现代布局方案：

```scss
// 使用 Flexbox
.container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

// 使用 Grid
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
}
```

### 4. 图片优化

确保图片在各种屏幕上都快速加载：

```vue
<img
  src="image.jpg"
  srcset="image-small.jpg 480w, image-medium.jpg 768w, image-large.jpg 1200w"
  sizes="(max-width: 480px) 100vw, (max-width: 768px) 50vw, 33vw"
  alt="Description"
>
```

---

## 📚 参考资源

- [MDN Responsive Design](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design)
- [Web.dev Responsive Design](https://web.dev/responsive-web-design-basics/)
- [CSS-Tricks Guide to Flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- [CSS-Tricks Complete Guide to Grid](https://css-tricks.com/snippets/css/complete-guide-grid/)

---

**最后更新**: 2026-01-28
**作者**: DeepV Code AI
**状态**: 响应式设计指南已完成
