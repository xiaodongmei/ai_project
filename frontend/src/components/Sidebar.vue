<template>
  <aside class="sidebar">
    <!-- Logo -->
    <div class="sidebar-logo">
      <router-link to="/dashboard" class="logo-link">
        <div class="logo-icon-wrapper">
          <svg class="logo-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z" />
            <path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12" />
          </svg>
        </div>
        <span class="logo-text">养生堂</span>
      </router-link>
    </div>

    <!-- 导航菜单 -->
    <nav class="sidebar-nav">
      <div class="nav-items">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          :class="['nav-item', { 'nav-item--active': isActive(item.path) }]"
        >
          <el-icon class="nav-icon"><component :is="item.icon" /></el-icon>
          <span class="nav-label">{{ item.label }}</span>
        </router-link>
      </div>
    </nav>

    <!-- 底部帮助 -->
    <div class="sidebar-footer">
      <button class="nav-item nav-item--help">
        <svg class="nav-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10" />
          <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
          <line x1="12" y1="17" x2="12.01" y2="17" />
        </svg>
        <span class="nav-label">帮助</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { useRoute } from 'vue-router'
import {
  CreditCard,
  OfficeBuilding,
  User,
  Calendar,
  Tickets,
  Goods,
  Avatar,
  DataAnalysis,
} from '@element-plus/icons-vue'

const route = useRoute()

const menuItems = [
  { icon: CreditCard, label: '收银', path: '/dashboard' },
  { icon: OfficeBuilding, label: '房间', path: '/rooms' },
  { icon: User, label: '顾客', path: '/customers' },
  { icon: Calendar, label: '预约', path: '/appointments' },
  { icon: Tickets, label: '订单', path: '/orders' },
  { icon: Goods, label: '产品', path: '/products' },
  { icon: Avatar, label: '员工', path: '/employees' },
  { icon: DataAnalysis, label: '统计', path: '/statistics' },
]

const isActive = (path) => {
  return route.path === path
}
</script>

<style scoped lang="scss">
$sidebar-bg: #1e40af;
$sidebar-width: 106px;

.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  z-index: 40;
  width: $sidebar-width;
  height: 100vh;
  background: linear-gradient(180deg, #2563eb 0%, #1e40af 100%);
  display: flex;
  flex-direction: column;
}

// Logo
.sidebar-logo {
  height: 88px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  text-decoration: none;
  transition: opacity 0.2s;

  &:hover {
    opacity: 0.85;
  }
}

.logo-icon-wrapper {
  width: 44px;
  height: 44px;
  background: rgba(255, 255, 255, 0.18);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;

  .logo-svg {
    width: 26px;
    height: 26px;
    color: white;
  }
}

.logo-text {
  font-size: 13px;
  font-weight: 600;
  color: white;
}

// Navigation
.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: 12px 0;

  &::-webkit-scrollbar {
    width: 0;
  }
}

.nav-items {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  width: 100%;
  padding: 14px 8px;
  color: rgba(255, 255, 255, 0.65);
  text-decoration: none;
  border: none;
  background: none;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;

  &:hover {
    background: rgba(255, 255, 255, 0.08);
    color: white;
  }

  &--active {
    background: rgba(255, 255, 255, 0.15);
    color: white;
  }
}

.nav-icon {
  width: 26px;
  height: 26px;
  font-size: 26px;
}

.nav-icon-svg {
  width: 24px;
  height: 24px;
}

.nav-label {
  font-size: 13px;
  font-weight: 500;
  line-height: 1;
}

// Footer
.sidebar-footer {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding: 8px 0;
}

.nav-item--help {
  width: 100%;
  padding: 12px 8px;
}
</style>
