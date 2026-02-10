<template>
  <div class="appointments-page">
    <div class="page-header-row">
      <h1>预约管理</h1>
      <button class="btn-primary" @click="ElMessage.info('功能开发中')">新建预约</button>
    </div>

    <div class="appointments-card">
      <div class="card-header">
        <div class="tabs">
          <button v-for="tab in tabs" :key="tab.id" :class="['tab', { 'tab--active': activeTab === tab.id }]" @click="activeTab = tab.id">
            {{ tab.label }}
            <span v-if="tab.badge" class="tab-badge">{{ tab.badge }}</span>
          </button>
        </div>
        <div class="date-info">{{ today }}</div>
      </div>

      <div class="appointments-list">
        <div class="appointment-row" v-for="apt in appointments" :key="apt.id">
          <div class="apt-time">
            <span class="time-label">预约</span>
            <span class="time-value">{{ apt.time }}</span>
          </div>
          <div class="apt-info">
            <span class="apt-customer">{{ apt.customer }}</span>
            <span class="apt-vip" v-if="apt.is_vip">VIP</span>
          </div>
          <div class="apt-service">{{ apt.service }}</div>
          <div class="apt-technician">{{ apt.technician }}</div>
          <span :class="['apt-status', `apt-status--${apt.statusType}`]">{{ apt.status }}</span>
          <div class="apt-actions">
            <button class="action-link" @click="ElMessage.info('查看详情')">详情</button>
            <button class="action-link" @click="ElMessage.info('确认到店')">确认</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const activeTab = ref('today')
const today = new Date().toLocaleDateString('zh-CN')

const tabs = [
  { id: 'today', label: '今日预约', badge: 5 },
  { id: 'upcoming', label: '未来预约' },
  { id: 'history', label: '历史预约' },
]

const appointments = [
  { id: 1, time: '14:30', customer: '陈静', is_vip: true, service: '艾灸理疗 · 60min', technician: '李师傅', status: '待到店', statusType: 'pending' },
  { id: 2, time: '15:00', customer: '赵明', is_vip: false, service: '推拿按摩 · 60min', technician: '王师傅', status: '已到店', statusType: 'arrived' },
  { id: 3, time: '15:30', customer: '钱薇', is_vip: false, service: '精油SPA · 90min', technician: '张师傅', status: '待到店', statusType: 'pending' },
  { id: 4, time: '16:00', customer: '王芳', is_vip: true, service: '足部按摩 · 60min', technician: '杨枫', status: '已确认', statusType: 'confirmed' },
  { id: 5, time: '16:30', customer: '刘洋', is_vip: false, service: '肩颈理疗 · 45min', technician: '惠珠秀', status: '待确认', statusType: 'waiting' },
]
</script>

<style scoped lang="scss">
$primary: #2563eb;
$primary-light: rgba(37, 99, 235, 0.1);
$border: #e5e7eb;
$text-main: #111827;
$text-secondary: #6b7280;
$text-muted: #9ca3af;
$green: #10b981;
$orange: #f59e0b;

.appointments-page { padding: 24px; background: #f5f7fa; min-height: 100%; }
.page-header-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;
  h1 { font-size: 22px; font-weight: 600; color: $text-main; margin: 0; }
}
.btn-primary { padding: 8px 20px; background: $primary; color: white; border: none; border-radius: 8px; font-size: 14px; cursor: pointer; }

.appointments-card { background: white; border: 1px solid $border; border-radius: 12px; overflow: hidden; }
.card-header { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; border-bottom: 1px solid $border; }
.tabs { display: flex; gap: 24px; }
.tab { background: none; border: none; font-size: 14px; font-weight: 500; color: $text-muted; cursor: pointer; padding: 4px 0; border-bottom: 2px solid transparent;
  &--active { color: $text-main; border-bottom-color: $primary; }
}
.tab-badge { background: $primary; color: white; border-radius: 10px; font-size: 11px; padding: 1px 7px; margin-left: 4px; }
.date-info { font-size: 13px; color: $text-muted; }

.appointments-list { }
.appointment-row { display: flex; align-items: center; gap: 16px; padding: 16px 20px; border-bottom: 1px solid #f3f4f6;
  &:last-child { border-bottom: none; }
  &:hover { background: #f9fafb; }
}
.apt-time { width: 56px; height: 56px; border-radius: 10px; background: $primary-light; color: $primary; display: flex; flex-direction: column; align-items: center; justify-content: center; flex-shrink: 0;
  .time-label { font-size: 10px; font-weight: 500; }
  .time-value { font-size: 16px; font-weight: 700; }
}
.apt-info { display: flex; align-items: center; gap: 6px; min-width: 100px; }
.apt-customer { font-size: 14px; font-weight: 500; color: $text-main; }
.apt-vip { font-size: 10px; padding: 1px 6px; background: #8b5cf6; color: white; border-radius: 6px; }
.apt-service { font-size: 13px; color: $text-secondary; flex: 1; }
.apt-technician { font-size: 13px; color: $text-secondary; min-width: 80px; }
.apt-status { font-size: 12px; padding: 3px 10px; border-radius: 8px; white-space: nowrap;
  &--pending { background: rgba(245, 158, 11, 0.1); color: #b45309; }
  &--arrived { background: rgba(16, 185, 129, 0.1); color: $green; }
  &--confirmed { background: $primary-light; color: $primary; }
  &--waiting { background: #f3f4f6; color: $text-muted; }
}
.apt-actions { display: flex; gap: 8px; }
.action-link { background: none; border: none; font-size: 13px; color: $primary; cursor: pointer; &:hover { text-decoration: underline; } }
</style>
