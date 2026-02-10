<template>
  <div class="dashboard-container">
    <div class="dashboard-content">
      <!-- 欢迎区域 + 操作按钮 -->
      <div class="welcome-section">
        <div class="welcome-text">
          <h1>欢迎回来，管理员</h1>
          <p>这是今日的店铺运营概况</p>
        </div>
        <div class="welcome-actions">
          <button class="btn-outline">
            <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
              <line x1="16" y1="2" x2="16" y2="6" />
              <line x1="8" y1="2" x2="8" y2="6" />
              <line x1="3" y1="10" x2="21" y2="10" />
            </svg>
            今日
          </button>
          <button class="btn-primary">
            <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="23 6 13.5 15.5 8.5 10.5 1 18" />
              <polyline points="17 6 23 6 23 12" />
            </svg>
            查看报表
          </button>
        </div>
      </div>

      <!-- 数据指标卡片 -->
      <div class="stats-grid">
        <div class="stat-card" v-for="stat in statsData" :key="stat.title">
          <div class="stat-info">
            <p class="stat-label">{{ stat.title }}</p>
            <p class="stat-value">{{ stat.value }}</p>
            <p :class="['stat-change', `stat-change--${stat.changeType}`]">
              <span v-if="stat.changeType === 'positive'">↑</span>
              <span v-if="stat.changeType === 'negative'">↓</span>
              {{ stat.change }}
            </p>
          </div>
          <div :class="['stat-icon-box', `stat-icon-box--${stat.color}`]">
            <component :is="stat.icon" class="stat-icon" />
          </div>
        </div>
      </div>

      <!-- 主内容区域: 最近订单 + 今日预约 -->
      <div class="main-grid">
        <!-- 最近订单 -->
        <div class="card card-orders">
          <div class="card-header">
            <h2 class="card-title">最近订单</h2>
            <button class="btn-link">
              查看全部
              <svg class="btn-icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="7" y1="17" x2="17" y2="7" />
                <polyline points="7 7 17 7 17 17" />
              </svg>
            </button>
          </div>
          <div class="card-body">
            <div class="order-list">
              <div class="order-item" v-for="order in recentOrders" :key="order.id">
                <div class="order-left">
                  <div class="avatar">{{ order.customer.charAt(0) }}</div>
                  <div class="order-info">
                    <p class="order-name">{{ order.customer }}</p>
                    <p class="order-service">{{ order.service }}</p>
                  </div>
                </div>
                <div class="order-right">
                  <div class="order-amount-time">
                    <p class="order-amount">¥{{ order.amount }}</p>
                    <p class="order-time">
                      <svg class="time-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10" />
                        <polyline points="12 6 12 12 16 14" />
                      </svg>
                      {{ order.time }}
                    </p>
                  </div>
                  <span :class="['order-status', `order-status--${order.statusType}`]">
                    {{ order.status }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 今日预约 -->
        <div class="card card-appointments">
          <div class="card-header">
            <h2 class="card-title">今日预约</h2>
            <span class="badge">{{ upcomingAppointments.length }} 个</span>
          </div>
          <div class="card-body">
            <div class="appointment-list">
              <div class="appointment-item" v-for="(apt, index) in upcomingAppointments" :key="index">
                <div class="appointment-time-box">
                  <span class="appointment-label">预约</span>
                  <span class="appointment-time">{{ apt.time }}</span>
                </div>
                <div class="appointment-info">
                  <p class="appointment-name">{{ apt.customer }}</p>
                  <p class="appointment-detail">{{ apt.service }} · {{ apt.therapist }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 热门服务 -->
      <div class="card card-products">
        <div class="card-header">
          <h2 class="card-title">热门服务</h2>
          <button class="btn-link">
            查看全部
            <svg class="btn-icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="7" y1="17" x2="17" y2="7" />
              <polyline points="7 7 17 7 17 17" />
            </svg>
          </button>
        </div>
        <div class="card-body">
          <div class="products-grid">
            <div class="product-item" v-for="(product, index) in topProducts" :key="index">
              <div class="product-header">
                <span class="product-rank">#{{ index + 1 }}</span>
                <span class="product-badge">{{ product.sales }} 单</span>
              </div>
              <h4 class="product-name">{{ product.name }}</h4>
              <p class="product-revenue">营收: ¥{{ product.revenue.toLocaleString() }}</p>
              <div class="progress-track">
                <div class="progress-fill" :style="{ width: product.progress + '%' }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { shallowRef } from 'vue'
import { Coin, ShoppingCart, UserFilled, Calendar } from '@element-plus/icons-vue'

const statsData = [
  {
    title: '今日营收',
    value: '¥8,520',
    change: '较昨日 +18.2%',
    changeType: 'positive',
    icon: shallowRef(Coin),
    color: 'blue',
  },
  {
    title: '今日订单',
    value: '42',
    change: '较昨日 +12.5%',
    changeType: 'positive',
    icon: shallowRef(ShoppingCart),
    color: 'green',
  },
  {
    title: '到店顾客',
    value: '38',
    change: '较昨日 -5.2%',
    changeType: 'negative',
    icon: shallowRef(UserFilled),
    color: 'orange',
  },
  {
    title: '预约数量',
    value: '15',
    change: '下午时段',
    changeType: 'neutral',
    icon: shallowRef(Calendar),
    color: 'gold',
  },
]

const recentOrders = [
  { id: 'ORD001', customer: '王芳', service: '足部按摩', amount: 298, status: '已完成', statusType: 'completed', time: '10:30' },
  { id: 'ORD002', customer: '张三', service: '艾灸理疗', amount: 388, status: '进行中', statusType: 'progress', time: '11:00' },
  { id: 'ORD003', customer: '李四', service: '推拿按摩', amount: 258, status: '待处理', statusType: 'pending', time: '11:30' },
  { id: 'ORD004', customer: '刘洋', service: '精油SPA', amount: 598, status: '已完成', statusType: 'completed', time: '14:00' },
]

const upcomingAppointments = [
  { customer: '陈静', service: '艾灸理疗', time: '14:30', therapist: '李师傅' },
  { customer: '赵明', service: '推拿按摩', time: '15:00', therapist: '王师傅' },
  { customer: '钱薇', service: '精油SPA', time: '15:30', therapist: '张师傅' },
]

const topProducts = [
  { name: '艾灸理疗套餐', sales: 156, revenue: 60528, progress: 85 },
  { name: '足部按摩', sales: 142, revenue: 42316, progress: 78 },
  { name: '精油SPA', sales: 98, revenue: 58604, progress: 65 },
  { name: '推拿按摩', sales: 87, revenue: 22446, progress: 55 },
]
</script>

<style scoped lang="scss">
// ===== 颜色变量 =====
$primary: #2563eb;
$primary-light: rgba(37, 99, 235, 0.1);
$primary-lighter: rgba(37, 99, 235, 0.06);
$green: #10b981;
$green-light: rgba(16, 185, 129, 0.12);
$orange: #f59e0b;
$orange-light: rgba(245, 158, 11, 0.12);
$gold: #d97706;
$gold-light: rgba(217, 119, 6, 0.1);
$red: #ef4444;
$text-main: #111827;
$text-secondary: #6b7280;
$text-muted: #9ca3af;
$border: #e5e7eb;
$bg-card: #ffffff;
$bg-muted: #f9fafb;
$bg-page: #f5f7fa;

.dashboard-container {
  padding: 24px;
  background: $bg-page;
  min-height: 100%;
}

.dashboard-content {
  max-width: 1400px;
  margin: 0 auto;
}

// ===== 欢迎区域 =====
.welcome-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.welcome-text {
  h1 {
    font-size: 28px;
    font-weight: 700;
    color: $text-main;
    margin: 0 0 6px 0;
    line-height: 1.3;
  }

  p {
    font-size: 15px;
    color: $text-secondary;
    margin: 0;
  }
}

.welcome-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-outline {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: white;
  border: 1px solid $border;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  color: $text-main;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    border-color: $primary;
    color: $primary;
    background: $primary-lighter;
  }
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 20px;
  background: $primary;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  color: white;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: #1d4ed8;
  }
}

.btn-icon {
  width: 16px;
  height: 16px;
}

.btn-icon-sm {
  width: 14px;
  height: 14px;
}

// ===== 数据卡片 =====
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;

  @media (max-width: 1200px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 640px) {
    grid-template-columns: 1fr;
  }
}

.stat-card {
  position: relative;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 24px;
  background: $bg-card;
  border: 1px solid $border;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s;

  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    border-color: rgba(37, 99, 235, 0.2);

    .stat-icon-box {
      transform: scale(1.1);
    }

    &::after {
      opacity: 1;
    }
  }

  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, rgba(37, 99, 235, 0.2), transparent);
    opacity: 0;
    transition: opacity 0.3s;
  }
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.stat-label {
  font-size: 15px;
  font-weight: 500;
  color: $text-secondary;
  margin: 0;
}

.stat-value {
  font-size: 36px;
  font-weight: 700;
  color: $text-main;
  margin: 0;
  letter-spacing: -0.5px;
  line-height: 1.2;
}

.stat-change {
  font-size: 13px;
  font-weight: 500;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 2px;

  &--positive {
    color: $primary;
  }

  &--negative {
    color: $red;
  }

  &--neutral {
    color: $text-muted;
  }
}

.stat-icon-box {
  width: 52px;
  height: 52px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: transform 0.3s;

  &--blue {
    background: $primary-light;
    color: $primary;
  }

  &--green {
    background: $green-light;
    color: $green;
  }

  &--orange {
    background: $orange-light;
    color: $orange;
  }

  &--gold {
    background: $gold-light;
    color: $gold;
  }

  .stat-icon {
    width: 26px;
    height: 26px;
  }
}

// ===== 卡片通用 =====
.card {
  background: $bg-card;
  border: 1px solid $border;
  border-radius: 12px;
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px 12px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: $text-main;
  margin: 0;
}

.card-body {
  padding: 0 24px 24px;
}

.btn-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: none;
  border: none;
  font-size: 14px;
  font-weight: 500;
  color: $primary;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background 0.2s;

  &:hover {
    background: $primary-lighter;
  }
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  background: $primary-light;
  color: $primary;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
}

// ===== 主内容网格 =====
.main-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
  margin-bottom: 24px;

  @media (max-width: 1024px) {
    grid-template-columns: 1fr;
  }
}

// ===== 最近订单 =====
.order-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.order-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: $bg-muted;
  border: 1px solid $border;
  border-radius: 10px;
  transition: background 0.2s;

  &:hover {
    background: #f3f4f6;
  }
}

.order-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: $primary-light;
  color: $primary;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 600;
  flex-shrink: 0;
}

.order-info {
  .order-name {
    font-size: 15px;
    font-weight: 500;
    color: $text-main;
    margin: 0 0 4px 0;
  }

  .order-service {
    font-size: 13px;
    color: $text-secondary;
    margin: 0;
  }
}

.order-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.order-amount-time {
  text-align: right;

  .order-amount {
    font-size: 15px;
    font-weight: 600;
    color: $text-main;
    margin: 0 0 4px 0;
  }

  .order-time {
    font-size: 13px;
    color: $text-muted;
    margin: 0;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 4px;

    .time-icon {
      width: 12px;
      height: 12px;
    }
  }
}

.order-status {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;

  &--completed {
    background: $primary-light;
    color: $primary;
  }

  &--progress {
    background: rgba(245, 158, 11, 0.12);
    color: #b45309;
  }

  &--pending {
    background: #f3f4f6;
    color: $text-secondary;
  }
}

// ===== 今日预约 =====
.appointment-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.appointment-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px;
  border: 1px solid $border;
  border-radius: 10px;
  transition: background 0.2s;

  &:hover {
    background: $bg-muted;
  }
}

.appointment-time-box {
  width: 56px;
  height: 56px;
  border-radius: 10px;
  background: $primary-light;
  color: $primary;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.appointment-label {
  font-size: 11px;
  font-weight: 500;
}

.appointment-time {
  font-size: 16px;
  font-weight: 700;
}

.appointment-info {
  flex: 1;
  min-width: 0;

  .appointment-name {
    font-size: 15px;
    font-weight: 500;
    color: $text-main;
    margin: 0 0 4px 0;
  }

  .appointment-detail {
    font-size: 13px;
    color: $text-secondary;
    margin: 0;
  }
}

// ===== 热门服务 =====
.products-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;

  @media (max-width: 1200px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 640px) {
    grid-template-columns: 1fr;
  }
}

.product-item {
  padding: 20px;
  background: $bg-muted;
  border: 1px solid $border;
  border-radius: 10px;
  transition: background 0.2s;

  &:hover {
    background: #f3f4f6;
  }
}

.product-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.product-rank {
  font-size: 24px;
  font-weight: 700;
  color: $primary;
}

.product-badge {
  display: inline-flex;
  padding: 3px 10px;
  background: $primary-light;
  color: $primary;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.product-name {
  font-size: 15px;
  font-weight: 500;
  color: $text-main;
  margin: 0 0 8px 0;
}

.product-revenue {
  font-size: 13px;
  color: $text-secondary;
  margin: 0 0 14px 0;
}

.progress-track {
  height: 6px;
  background: #e5e7eb;
  border-radius: 3px;
  overflow: hidden;

  .progress-fill {
    height: 100%;
    background: $primary;
    border-radius: 3px;
    transition: width 0.5s ease;
  }
}

// ===== 响应式 =====
@media (max-width: 768px) {
  .dashboard-container {
    padding: 16px;
  }

  .welcome-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .stat-value {
    font-size: 28px;
  }
}
</style>
