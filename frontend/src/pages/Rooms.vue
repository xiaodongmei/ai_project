<template>
  <div class="rooms-page">
    <!-- 顶部总览 -->
    <div class="summary-bar">
      <div class="summary-item">
        <span class="summary-label">房间</span>
        <span class="summary-value">{{ summary.rooms?.available || 0 }}<span class="summary-unit">/{{ summary.rooms?.total || 0 }} 空</span></span>
      </div>
      <div class="summary-item">
        <span class="summary-label">床位</span>
        <span class="summary-value">{{ summary.beds?.available || 0 }}<span class="summary-unit">/{{ summary.beds?.total || 0 }} 空</span></span>
      </div>
      <div class="summary-item">
        <span class="summary-label">VIP</span>
        <span class="summary-value summary-value--vip">{{ summary.vip?.available || 0 }}<span class="summary-unit">/{{ summary.vip?.total || 0 }} 可用</span></span>
      </div>
      <div class="summary-item">
        <span class="summary-label">技师</span>
        <span class="summary-value">{{ summary.technicians?.idle || 0 }}<span class="summary-unit">/{{ summary.technicians?.total || 0 }} 空闲</span></span>
      </div>
      <div class="summary-item" v-if="summary.technicians?.finishing_soon">
        <span class="summary-label">即将结束</span>
        <span class="summary-value summary-value--warn">{{ summary.technicians.finishing_soon }}</span>
      </div>
      <button class="btn-refresh" @click="loadData">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="refresh-icon"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>
        刷新
      </button>
    </div>

    <!-- 楼层筛选 -->
    <div class="floor-filter">
      <button
        v-for="f in floorOptions"
        :key="f.value"
        :class="['floor-btn', { 'floor-btn--active': selectedFloor === f.value }]"
        @click="selectedFloor = f.value"
      >{{ f.label }}</button>
    </div>

    <!-- 房间卡片网格 -->
    <div class="rooms-grid">
      <div
        v-for="room in filteredRooms"
        :key="room.id"
        :class="['room-card', { 'room-card--occupied': !room.is_available, 'room-card--vip': room.is_vip }]"
      >
        <!-- 房间头部 -->
        <div class="room-header">
          <div class="room-number-info">
            <span class="room-number">{{ room.room_number }}</span>
            <span class="room-name">{{ room.name }}</span>
            <span v-if="room.is_vip" class="vip-badge">VIP</span>
          </div>
          <span :class="['room-status', room.is_available ? 'room-status--free' : 'room-status--busy']">
            {{ room.is_available ? '空闲' : '使用中' }}
          </span>
        </div>

        <!-- 房间类型和价格 -->
        <div class="room-meta">
          <span>{{ room.type }} · {{ room.capacity }}床位</span>
          <span>¥{{ room.price_per_hour }}/h</span>
        </div>

        <!-- 床位列表 -->
        <div class="beds-list">
          <div
            v-for="bed in room.beds"
            :key="bed.id"
            :class="['bed-item', `bed-item--${bed.status}`]"
          >
            <div class="bed-header">
              <span class="bed-name">{{ bed.name }}</span>
              <span :class="['bed-status', `bed-status--${bed.status}`]">
                {{ bedStatusText(bed.status) }}
              </span>
            </div>

            <!-- 占用中显示详细信息 -->
            <template v-if="bed.status === 'occupied' && bed.customer">
              <div class="bed-customer">
                <span class="customer-name">
                  {{ bed.customer.name }}
                  <span v-if="bed.customer.is_vip" class="vip-tag">VIP</span>
                </span>
                <span class="customer-phone">{{ bed.customer.phone }}</span>
              </div>
              <div class="bed-service" v-if="bed.service">
                <span class="service-name">{{ bed.service.name }}</span>
                <span class="service-time">{{ bed.service.start_time }} - {{ bed.service.end_time }}</span>
              </div>
              <!-- 进度条 -->
              <div class="progress-track" v-if="bed.service">
                <div
                  class="progress-fill"
                  :style="{ width: bed.service.progress + '%' }"
                  :class="{ 'progress-fill--finishing': bed.service.progress >= 80 }"
                ></div>
                <span class="progress-text">{{ bed.service.progress }}%</span>
              </div>
              <!-- 技师 -->
              <div class="bed-technician" v-if="bed.technician">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="tech-icon"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                <span>{{ bed.technician.name }}</span>
                <span :class="['tech-status', `tech-status--${bed.technician.status}`]">
                  {{ techStatusText(bed.technician.status) }}
                </span>
              </div>
              <!-- 快速操作按钮 -->
              <div class="bed-actions">
                <button class="action-btn action-btn--swap" @click="openChangeTech(room, bed)" title="换技师">换技师</button>
                <button class="action-btn action-btn--extend" @click="extendService(room.id, bed.id)" title="延长">延长</button>
                <button class="action-btn action-btn--checkout" @click="checkoutBed(room.id, bed.id)" title="结账">结账</button>
              </div>
            </template>

            <!-- 清洁中 -->
            <template v-else-if="bed.status === 'cleaning'">
              <div class="cleaning-note">正在清洁整理中...</div>
            </template>

            <!-- 空闲 -->
            <template v-else>
              <button class="open-bed-btn" @click="openBed(room, bed)">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="open-icon"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                开床
              </button>
            </template>
          </div>
        </div>
      </div>
    </div>

    <!-- 技师列表面板 -->
    <div class="technician-panel">
      <h3 class="panel-title">技师状态</h3>
      <div class="tech-list">
        <div v-for="tech in technicians" :key="tech.id" class="tech-card">
          <div class="tech-avatar">{{ tech.name.charAt(0) }}</div>
          <div class="tech-info">
            <span class="tech-name">{{ tech.name }}</span>
            <span class="tech-specialty">{{ tech.specialty }}</span>
          </div>
          <span :class="['tech-badge', `tech-badge--${tech.status}`]">
            {{ techStatusText(tech.status) }}
          </span>
          <span class="tech-room" v-if="tech.current_room">{{ tech.current_room }}房</span>
        </div>
      </div>
    </div>

    <!-- 换技师弹窗 -->
    <div v-if="showChangeTechDialog" class="dialog-overlay" @click.self="showChangeTechDialog = false">
      <div class="dialog-box">
        <div class="dialog-header">
          <h3>更换技师</h3>
          <button class="dialog-close" @click="showChangeTechDialog = false">✕</button>
        </div>
        <div class="dialog-body">
          <p class="dialog-info">{{ changeTechTarget.room?.room_number }}房 {{ changeTechTarget.bed?.name }} - 当前技师：{{ changeTechTarget.bed?.technician?.name }}</p>
          <div class="tech-options">
            <button
              v-for="tech in availableTechnicians"
              :key="tech.id"
              class="tech-option"
              @click="confirmChangeTech(tech.name)"
            >
              <span class="tech-opt-name">{{ tech.name }}</span>
              <span class="tech-opt-spec">{{ tech.specialty }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { roomsApi } from '@/api/rooms'

const rooms = ref([])
const technicians = ref([])
const summary = ref({})
const selectedFloor = ref('all')
const showChangeTechDialog = ref(false)
const changeTechTarget = ref({ room: null, bed: null })

const floorOptions = computed(() => {
  const floors = [...new Set(rooms.value.map(r => r.floor).filter(Boolean))].sort()
  return [{ label: '全部楼层', value: 'all' }, ...floors.map(f => ({ label: `${f}F`, value: f }))]
})

const filteredRooms = computed(() => {
  if (selectedFloor.value === 'all') return rooms.value
  return rooms.value.filter(r => r.floor === selectedFloor.value)
})

const availableTechnicians = computed(() => {
  return technicians.value.filter(t => t.status === 'idle')
})

const bedStatusText = (s) => ({ available: '空闲', occupied: '使用中', cleaning: '清洁中' }[s] || s)
const techStatusText = (s) => ({ working: '服务中', finishing: '即将结束', idle: '空闲' }[s] || s)

const loadData = async () => {
  try {
    const roomsRes = await roomsApi.getRooms({ limit: 100 })
    rooms.value = roomsRes?.data || []
  } catch (e) {
    rooms.value = []
  }

  try {
    const techRes = await roomsApi.getTechnicians?.() || { data: [] }
    technicians.value = techRes?.data || []
  } catch (e) {
    technicians.value = []
  }

  try {
    const sumRes = await roomsApi.getSummary?.() || {}
    summary.value = sumRes || {}
  } catch (e) {
    // 从本地数据计算
    const total = rooms.value.length
    const available = rooms.value.filter(r => r.is_available).length
    const vipTotal = rooms.value.filter(r => r.is_vip).length
    const vipAvail = rooms.value.filter(r => r.is_vip && r.is_available).length
    const allBeds = rooms.value.flatMap(r => r.beds || [])
    summary.value = {
      rooms: { total, available, occupied: total - available },
      vip: { total: vipTotal, available: vipAvail },
      beds: { total: allBeds.length, available: allBeds.filter(b => b.status === 'available').length, occupied: allBeds.filter(b => b.status === 'occupied').length, cleaning: allBeds.filter(b => b.status === 'cleaning').length },
      technicians: { total: technicians.value.length, idle: technicians.value.filter(t => t.status === 'idle').length, working: technicians.value.filter(t => t.status !== 'idle').length, finishing_soon: technicians.value.filter(t => t.status === 'finishing').length },
    }
  }
}

const openBed = async (room, bed) => {
  try {
    await roomsApi.openBed?.(room.id, bed.id, {
      customer: { name: '新顾客', is_vip: false, phone: '***' },
      service: { name: '待选择服务', progress: 0 },
      technician: { name: '待分配', status: 'working' },
    })
    ElMessage.success(`${room.room_number}房 ${bed.name} 已开床`)
    await loadData()
  } catch (e) {
    ElMessage.error('开床失败')
  }
}

const checkoutBed = async (roomId, bedId) => {
  try {
    await roomsApi.checkoutBed?.(roomId, bedId)
    ElMessage.success('结账成功')
    await loadData()
  } catch (e) {
    ElMessage.error('结账失败')
  }
}

const extendService = async (roomId, bedId) => {
  try {
    await roomsApi.extendService?.(roomId, bedId, { minutes: 30 })
    ElMessage.success('已延长30分钟')
    await loadData()
  } catch (e) {
    ElMessage.error('延长失败')
  }
}

const openChangeTech = (room, bed) => {
  changeTechTarget.value = { room, bed }
  showChangeTechDialog.value = true
}

const confirmChangeTech = async (techName) => {
  try {
    const { room, bed } = changeTechTarget.value
    await roomsApi.changeTechnician?.(room.id, bed.id, { technician_name: techName })
    ElMessage.success(`已更换技师为 ${techName}`)
    showChangeTechDialog.value = false
    await loadData()
  } catch (e) {
    ElMessage.error('更换技师失败')
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
$primary: #2563eb;
$primary-light: rgba(37, 99, 235, 0.1);
$green: #10b981;
$green-light: rgba(16, 185, 129, 0.1);
$orange: #f59e0b;
$orange-light: rgba(245, 158, 11, 0.1);
$red: #ef4444;
$red-light: rgba(239, 68, 68, 0.1);
$border: #e5e7eb;
$bg-card: #fff;
$bg-page: #f5f7fa;
$text-main: #111827;
$text-secondary: #6b7280;
$text-muted: #9ca3af;
$purple: #8b5cf6;

.rooms-page { padding: 24px; background: $bg-page; min-height: 100%; }

// 总览条
.summary-bar {
  display: flex; align-items: center; gap: 24px; padding: 16px 20px; background: white; border: 1px solid $border; border-radius: 12px; margin-bottom: 16px;
}
.summary-item { display: flex; flex-direction: column; }
.summary-label { font-size: 12px; color: $text-muted; margin-bottom: 4px; }
.summary-value { font-size: 24px; font-weight: 700; color: $text-main;
  &--vip { color: $purple; }
  &--warn { color: $orange; }
}
.summary-unit { font-size: 13px; font-weight: 400; color: $text-secondary; margin-left: 2px; }
.btn-refresh { margin-left: auto; display: flex; align-items: center; gap: 6px; padding: 8px 16px; border: 1px solid $border; border-radius: 8px; background: white; font-size: 13px; cursor: pointer; transition: all 0.2s;
  &:hover { border-color: $primary; color: $primary; }
  .refresh-icon { width: 14px; height: 14px; }
}

// 楼层筛选
.floor-filter { display: flex; gap: 8px; margin-bottom: 16px; }
.floor-btn { padding: 6px 16px; border: 1px solid $border; border-radius: 8px; background: white; font-size: 13px; cursor: pointer; transition: all 0.2s;
  &--active { background: $primary; color: white; border-color: $primary; }
  &:hover:not(.floor-btn--active) { border-color: $primary; color: $primary; }
}

// 房间卡片
.rooms-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 16px; margin-bottom: 24px; }

.room-card {
  background: white; border: 1px solid $border; border-radius: 12px; padding: 16px; transition: box-shadow 0.2s;
  &:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.06); }
  &--occupied { border-left: 4px solid $orange; }
  &--vip { border-left: 4px solid $purple; }
  &--vip.room-card--occupied { border-left: 4px solid $purple; }
}

.room-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.room-number-info { display: flex; align-items: center; gap: 8px; }
.room-number { font-size: 18px; font-weight: 700; color: $text-main; }
.room-name { font-size: 14px; color: $text-secondary; }
.vip-badge { padding: 2px 8px; background: linear-gradient(135deg, #8b5cf6, #6d28d9); color: white; border-radius: 10px; font-size: 10px; font-weight: 600; }
.room-status { font-size: 12px; font-weight: 500; padding: 3px 10px; border-radius: 10px;
  &--free { background: $green-light; color: $green; }
  &--busy { background: $orange-light; color: #b45309; }
}
.room-meta { font-size: 12px; color: $text-muted; display: flex; justify-content: space-between; margin-bottom: 12px; }

// 床位
.beds-list { display: flex; flex-direction: column; gap: 10px; }
.bed-item {
  padding: 12px; border-radius: 10px; border: 1px solid $border;
  &--available { background: #f9fafb; }
  &--occupied { background: #fffbeb; border-color: #fde68a; }
  &--cleaning { background: #eff6ff; border-color: #bfdbfe; }
}
.bed-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px; }
.bed-name { font-size: 13px; font-weight: 600; color: $text-main; }
.bed-status { font-size: 11px; padding: 2px 8px; border-radius: 8px;
  &--available { background: $green-light; color: $green; }
  &--occupied { background: $orange-light; color: #b45309; }
  &--cleaning { background: rgba(37, 99, 235, 0.1); color: $primary; }
}

// 客户信息
.bed-customer { display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px; }
.customer-name { font-size: 14px; font-weight: 500; color: $text-main; display: flex; align-items: center; gap: 6px; }
.vip-tag { font-size: 10px; padding: 1px 6px; background: $purple; color: white; border-radius: 6px; }
.customer-phone { font-size: 12px; color: $text-muted; }

// 服务信息
.bed-service { display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px; }
.service-name { font-size: 13px; color: $primary; font-weight: 500; }
.service-time { font-size: 12px; color: $text-muted; }

// 进度条
.progress-track { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; height: 8px; background: #e5e7eb; border-radius: 4px; position: relative; overflow: visible; }
.progress-fill { height: 100%; border-radius: 4px; background: $green; transition: width 0.5s;
  &--finishing { background: $orange; }
}
.progress-text { font-size: 11px; color: $text-muted; white-space: nowrap; margin-left: 4px; position: absolute; right: -32px; }

// 技师
.bed-technician { display: flex; align-items: center; gap: 6px; font-size: 12px; color: $text-secondary; margin-bottom: 8px;
  .tech-icon { width: 14px; height: 14px; }
}
.tech-status { font-size: 11px; padding: 1px 6px; border-radius: 6px; margin-left: auto;
  &--working { background: $green-light; color: $green; }
  &--finishing { background: $orange-light; color: #b45309; }
}

// 操作按钮
.bed-actions { display: flex; gap: 6px; }
.action-btn { padding: 4px 12px; border-radius: 6px; font-size: 12px; border: 1px solid $border; background: white; cursor: pointer; transition: all 0.15s;
  &--swap { &:hover { color: $primary; border-color: $primary; } }
  &--extend { &:hover { color: $orange; border-color: $orange; } }
  &--checkout { &:hover { color: $green; border-color: $green; background: $green-light; } }
}

// 开床按钮
.open-bed-btn { display: flex; align-items: center; justify-content: center; gap: 6px; width: 100%; padding: 10px; border: 1px dashed $border; border-radius: 8px; background: none; color: $primary; font-size: 13px; cursor: pointer; transition: all 0.2s;
  .open-icon { width: 16px; height: 16px; }
  &:hover { background: $primary-light; border-color: $primary; }
}

// 清洁提示
.cleaning-note { font-size: 12px; color: $primary; padding: 4px 0; }

// 技师面板
.technician-panel { background: white; border: 1px solid $border; border-radius: 12px; padding: 20px; }
.panel-title { font-size: 16px; font-weight: 600; color: $text-main; margin: 0 0 14px 0; }
.tech-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 10px; }
.tech-card { display: flex; align-items: center; gap: 10px; padding: 10px 12px; border: 1px solid $border; border-radius: 10px; }
.tech-avatar { width: 36px; height: 36px; border-radius: 50%; background: $primary-light; color: $primary; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 600; flex-shrink: 0; }
.tech-info { flex: 1; min-width: 0; }
.tech-name { font-size: 14px; font-weight: 500; color: $text-main; display: block; }
.tech-specialty { font-size: 11px; color: $text-muted; }
.tech-badge { font-size: 11px; padding: 2px 8px; border-radius: 8px; white-space: nowrap;
  &--idle { background: $green-light; color: $green; }
  &--working { background: $orange-light; color: #b45309; }
  &--finishing { background: $red-light; color: $red; }
}
.tech-room { font-size: 11px; color: $text-muted; }

// 弹窗
.dialog-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; z-index: 100; }
.dialog-box { background: white; border-radius: 12px; width: 400px; max-height: 80vh; overflow-y: auto; }
.dialog-header { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; border-bottom: 1px solid $border;
  h3 { margin: 0; font-size: 16px; }
}
.dialog-close { background: none; border: none; font-size: 20px; cursor: pointer; color: $text-muted; }
.dialog-body { padding: 20px; }
.dialog-info { font-size: 14px; color: $text-secondary; margin: 0 0 16px 0; }
.tech-options { display: flex; flex-direction: column; gap: 8px; }
.tech-option { display: flex; justify-content: space-between; padding: 12px 16px; border: 1px solid $border; border-radius: 8px; background: white; cursor: pointer; transition: all 0.2s;
  &:hover { border-color: $primary; background: $primary-light; }
}
.tech-opt-name { font-size: 14px; font-weight: 500; color: $text-main; }
.tech-opt-spec { font-size: 12px; color: $text-muted; }

@media (max-width: 768px) {
  .rooms-grid { grid-template-columns: 1fr; }
  .summary-bar { flex-wrap: wrap; gap: 16px; }
}
</style>
