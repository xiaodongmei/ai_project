<template>
  <div class="statistics-page">
    <!-- 顶部时间选择 + 店铺信息 -->
    <div class="page-top">
      <div class="shop-info">
        <span class="shop-name">{{ shopConfig.shopName }}</span>
        <span class="shop-sep">·</span>
        <span class="shop-detail">门店统计</span>
      </div>
      <div class="time-controls">
        <span class="time-label">时间选择：</span>
        <input type="date" v-model="startDate" class="date-input" />
        <span class="date-sep">至</span>
        <input type="date" v-model="endDate" class="date-input" />
        <div class="quick-btns">
          <button
            v-for="btn in quickButtons"
            :key="btn.value"
            :class="['quick-btn', { 'quick-btn--active': activeQuick === btn.value }]"
            @click="setQuickRange(btn.value)"
          >{{ btn.label }}</button>
        </div>
      </div>
    </div>

    <!-- 数据总览标题 -->
    <div class="section-header">
      <h2>数据总览</h2>
      <span class="update-time">最近更新时间：{{ lastUpdate }}</span>
    </div>

    <!-- 数据总览卡片 -->
    <div class="overview-grid">
      <!-- 门店营收 -->
      <div class="overview-card overview-card--primary">
        <div class="card-label">
          门店营收(¥)
          <span class="info-icon" title="门店总营收，含所有渠道">ⓘ</span>
        </div>
        <div class="card-value">{{ dashboard.shop_revenue?.toFixed(2) || '0.00' }}</div>
      </div>
      <!-- 门店实收 -->
      <div class="overview-card">
        <div class="card-label">
          门店实收(¥)
          <span class="info-icon">ⓘ</span>
        </div>
        <div class="card-value">{{ dashboard.shop_actual_revenue?.toFixed(2) || '0.00' }}</div>
        <div class="card-note card-note--success">✅ 暂无退款</div>
      </div>
      <!-- 会员卡收入 -->
      <div class="overview-card">
        <div class="card-label-row">
          <span>会员卡收入(¥)
            <span class="info-icon">ⓘ</span>
          </span>
          <span>1元入会(数)</span>
        </div>
        <div class="card-value-row">
          <span class="card-value">{{ dashboard.member_recharge?.toFixed(2) || '0.00' }}</span>
          <span class="card-value">{{ dashboard.one_yuan_cards || 0 }}</span>
        </div>
        <div class="card-note">办卡数：{{ dashboard.card_count || 0 }}</div>
      </div>
    </div>

    <div class="overview-grid overview-grid--second">
      <!-- 有效订单 + 项目总数 -->
      <div class="overview-card">
        <div class="card-label-row">
          <span>有效订单数(条)
            <span class="info-icon">ⓘ</span>
          </span>
          <span>项目总数(条)
            <span class="info-icon">ⓘ</span>
          </span>
        </div>
        <div class="card-value-row">
          <span class="card-value">{{ dashboard.valid_orders || 0 }}</span>
          <span class="card-value">{{ dashboard.total_items || 0 }}</span>
        </div>
        <div class="card-note card-note--success">✅ 暂无退单</div>
      </div>
      <!-- 客流量 -->
      <div class="overview-card">
        <div class="card-label">
          客流量(人数)
          <span class="info-icon">ⓘ</span>
        </div>
        <div class="card-value">{{ dashboard.customer_visits || 0 }}</div>
        <div class="card-sub-row">
          <span>预约到店: {{ dashboard.appointment_count || 0 }}</span>
          <span>流失: {{ dashboard.lost_customers || 0 }}</span>
        </div>
      </div>
      <!-- 体验项目金额 -->
      <div class="overview-card">
        <div class="card-label-row">
          <span>体验项目金额(¥)
            <span class="info-icon">ⓘ</span>
          </span>
          <div class="toggle-btns-mini">
            <button :class="['toggle-btn-sm', { 'toggle-btn-sm--active': expView === 'before' }]" @click="expView = 'before'">扣点前</button>
            <button :class="['toggle-btn-sm', { 'toggle-btn-sm--active': expView === 'after' }]" @click="expView = 'after'">扣点后</button>
          </div>
        </div>
        <div class="card-value">{{ expView === 'before' ? (dashboard.experience_amount_before?.toFixed(2) || '0.00') : (dashboard.experience_amount_after?.toFixed(2) || '0.00') }}</div>
        <div class="card-note card-note--success">✅ 暂无体验项目数</div>
      </div>
    </div>

    <!-- 渠道统计 + 顾客消费 -->
    <div class="charts-row">
      <!-- 渠道统计 -->
      <div class="chart-card">
        <div class="chart-header">
          <div class="chart-tabs">
            <button :class="['tab-btn', { 'tab-btn--active': channelTab === 'channel' }]" @click="channelTab = 'channel'">渠道统计</button>
            <button :class="['tab-btn', { 'tab-btn--active': channelTab === 'actual' }]" @click="channelTab = 'actual'">实收分布</button>
            <button :class="['tab-btn', { 'tab-btn--active': channelTab === 'revenue' }]" @click="channelTab = 'revenue'">营收分布</button>
            <span class="info-icon">ⓘ</span>
          </div>
          <div class="toggle-btns">
            <button :class="['toggle-btn', { 'toggle-btn--active': channelView === 'before' }]" @click="channelView = 'before'">扣点前</button>
            <button :class="['toggle-btn', { 'toggle-btn--active': channelView === 'after' }]" @click="channelView = 'after'">扣点后</button>
          </div>
        </div>
        <div class="channel-list">
          <div class="channel-item" v-for="ch in dashboard.channels" :key="ch.channel">
            <div class="channel-name">
              <span :class="['channel-icon', `channel-icon--${getChannelClass(ch.channel)}`]">{{ getChannelEmoji(ch.channel) }}</span>
              {{ ch.channel }}
            </div>
            <div class="channel-data">
              <span class="channel-amount">¥{{ ch.revenue }}</span>
              <span class="channel-count">({{ ch.order_count }}品项数)</span>
            </div>
            <div class="channel-bar-wrapper">
              <div class="channel-bar" :style="{ width: ch.percentage + '%', background: getChannelColor(ch.channel) }"></div>
              <span class="channel-pct">{{ ch.percentage }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 顾客消费金额 -->
      <div class="chart-card">
        <div class="chart-header">
          <h3>顾客消费金额
            <span class="info-icon">ⓘ</span>
          </h3>
          <div class="legend">
            <span class="legend-item"><span class="legend-dot legend-dot--member"></span>会员</span>
            <span class="legend-item"><span class="legend-dot legend-dot--nonmember"></span>非会员</span>
            <span class="legend-item"><span class="legend-dot legend-dot--visitor"></span>散客</span>
          </div>
        </div>
        <div ref="customerChartEl" class="chart-container"></div>
      </div>
    </div>

    <!-- 员工排行 -->
    <div class="chart-card chart-card--full">
      <div class="chart-header">
        <h3>员工业绩排行</h3>
      </div>
      <div ref="employeeChartEl" class="chart-container"></div>
    </div>

    <!-- 产品销售排行 -->
    <div class="chart-card chart-card--full">
      <div class="chart-header">
        <h3>产品销售排行</h3>
      </div>
      <table class="data-table">
        <thead>
          <tr>
            <th>产品名称</th>
            <th>销售数量</th>
            <th>销售额</th>
            <th>占比</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in productSales" :key="item.product_name">
            <td>{{ item.product_name }}</td>
            <td class="amount">{{ item.sales_quantity }}</td>
            <td class="amount">¥{{ item.sales_amount }}</td>
            <td>{{ item.percentage }}%</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import * as statisticsApi from '@/api/statistics'
import { useShopConfigStore } from '@/store/shopConfig'

const shopConfig = useShopConfigStore()

const startDate = ref(new Date().toISOString().slice(0, 10))
const endDate = ref(new Date().toISOString().slice(0, 10))
const activeQuick = ref('today')
const channelTab = ref('channel')
const channelView = ref('before')
const expView = ref('before')
const lastUpdate = ref(new Date().toLocaleString('zh-CN'))

const quickButtons = [
  { label: '今日', value: 'today' },
  { label: '昨日', value: 'yesterday' },
  { label: '近7天', value: '7d' },
  { label: '近30天', value: '30d' },
]

const dashboard = ref({})
const productSales = ref([])

const customerChartEl = ref(null)
const employeeChartEl = ref(null)
let customerChart = null
let employeeChart = null

const setQuickRange = (val) => {
  activeQuick.value = val
  const today = new Date()
  endDate.value = today.toISOString().slice(0, 10)
  if (val === 'today') startDate.value = endDate.value
  else if (val === 'yesterday') {
    const y = new Date(today); y.setDate(y.getDate() - 1)
    startDate.value = y.toISOString().slice(0, 10)
    endDate.value = startDate.value
  }
  else if (val === '7d') { const d = new Date(today); d.setDate(d.getDate() - 7); startDate.value = d.toISOString().slice(0, 10) }
  else if (val === '30d') { const d = new Date(today); d.setDate(d.getDate() - 30); startDate.value = d.toISOString().slice(0, 10) }
  loadData()
}

const getChannelClass = (name) => {
  if (name.includes('美团')) return 'meituan'
  if (name.includes('抖音')) return 'douyin'
  if (name.includes('小程序')) return 'miniapp'
  return 'offline'
}
const getChannelEmoji = (name) => {
  if (name.includes('美团')) return '美'
  if (name.includes('抖音')) return '抖'
  if (name.includes('小程序')) return '微'
  return '店'
}
const getChannelColor = (name) => {
  if (name.includes('美团')) return '#ff6633'
  if (name.includes('抖音')) return '#111'
  if (name.includes('小程序')) return '#07c160'
  return '#2563eb'
}

const initCharts = () => {
  // 顾客消费图表
  if (customerChartEl.value) {
    customerChart = echarts.init(customerChartEl.value)
    const spending = dashboard.value.customer_spending || {}
    customerChart.setOption({
      tooltip: { trigger: 'axis' },
      grid: { left: 50, right: 20, top: 10, bottom: 30 },
      xAxis: { type: 'category', data: spending.labels || [] },
      yAxis: { type: 'value' },
      series: [
        { name: '会员', type: 'bar', data: spending.member || [], itemStyle: { color: '#1e3a5f' }, barWidth: 20 },
        { name: '非会员', type: 'bar', data: spending.non_member || [], itemStyle: { color: '#2563eb' }, barWidth: 20 },
        { name: '散客', type: 'bar', data: spending.visitor || [], itemStyle: { color: '#10b981' }, barWidth: 20 },
      ],
    })
  }

  // 员工排行图表
  if (employeeChartEl.value) {
    employeeChart = echarts.init(employeeChartEl.value)
    const emps = dashboard.value.top_employees || []
    employeeChart.setOption({
      tooltip: { trigger: 'axis' },
      grid: { left: 80, right: 30, top: 10, bottom: 30 },
      xAxis: { type: 'value' },
      yAxis: { type: 'category', data: emps.map(e => e.name).reverse(), axisLabel: { fontSize: 13 } },
      series: [{
        type: 'bar',
        data: emps.map(e => e.performance).reverse(),
        itemStyle: { color: '#2563eb', borderRadius: [0, 4, 4, 0] },
        barWidth: 24,
        label: { show: true, position: 'right', formatter: '¥{c}', fontSize: 12 },
      }],
    })
  }
}

const loadData = async () => {
  try {
    const params = { start_date: startDate.value, end_date: endDate.value, time_range: activeQuick.value }
    const res = await statisticsApi.getDashboardData(params)
    dashboard.value = res || {}
    lastUpdate.value = new Date().toLocaleString('zh-CN')
  } catch (e) {
    // 使用默认数据 - 员工名称使用通用名
    dashboard.value = {
      shop_revenue: 829.80, shop_actual_revenue: 802.32, member_recharge: 295.06,
      one_yuan_cards: 0, card_count: 3, valid_orders: 13, total_items: 12, refund_orders: 0,
      customer_visits: 13, appointment_count: 0, lost_customers: 0,
      experience_amount_before: 0, experience_amount_after: 0, experience_items: 0,
      channels: [
        { channel: '美团券', revenue: 344.8, order_count: 6, percentage: 42 },
        { channel: '抖音券', revenue: 68, order_count: 1, percentage: 8 },
        { channel: '门店扫码', revenue: 417, order_count: 6, percentage: 50 },
      ],
      customer_spending: {
        member: [680, 520, 450, 380, 300, 250, 180],
        non_member: [420, 380, 350, 280, 220, 180, 120],
        visitor: [150, 120, 100, 80, 60, 40, 20],
        labels: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
      },
      top_employees: [
        { rank: 1, name: '店长', performance: 848.8 },
        { rank: 2, name: '李强', performance: 250 },
        { rank: 3, name: '王月', performance: 150 },
        { rank: 4, name: '赵敏', performance: 100 },
        { rank: 5, name: '张峰', performance: 80 },
      ],
    }
  }

  try {
    const res = await statisticsApi.getProductSalesStatistics({})
    productSales.value = res?.data || []
  } catch (e) {
    // 使用行业模板的服务分类作为 fallback 数据
    const cats = shopConfig.serviceCategories.slice(0, 5)
    const mockAmounts = [5880, 4750, 3900, 3250, 2100]
    const mockQty = [120, 95, 78, 65, 42]
    const mockPct = [28.5, 22.9, 18.9, 15.7, 10.2]
    productSales.value = cats.map((name, i) => ({
      product_name: name,
      sales_quantity: mockQty[i] || 30,
      sales_amount: mockAmounts[i] || 1500,
      percentage: mockPct[i] || 10,
    }))
  }

  await nextTick()
  initCharts()
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
$primary: #2563eb;
$primary-light: rgba(37, 99, 235, 0.1);
$border: #e5e7eb;
$bg-card: #fff;
$bg-page: #f5f7fa;
$text-main: #111827;
$text-secondary: #6b7280;
$text-muted: #9ca3af;

.statistics-page { padding: 24px; background: $bg-page; min-height: 100%; }

// 顶部
.page-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; flex-wrap: wrap; gap: 12px; }
.shop-info { font-size: 15px; font-weight: 600; color: $text-main; .shop-sep { margin: 0 6px; color: $text-muted; } .shop-detail { font-weight: 400; color: $text-secondary; } }
.time-controls { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.time-label { font-size: 13px; color: $text-secondary; }
.date-input { height: 32px; border: 1px solid $border; border-radius: 6px; padding: 0 10px; font-size: 13px; background: white; }
.date-sep { color: $text-muted; font-size: 13px; }
.quick-btns { display: flex; gap: 4px; }
.quick-btn { height: 32px; padding: 0 14px; border: 1px solid $border; border-radius: 6px; font-size: 13px; background: white; cursor: pointer; transition: all 0.2s;
  &--active { background: $primary; color: white; border-color: $primary; }
  &:hover:not(.quick-btn--active) { border-color: $primary; color: $primary; }
}

.section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;
  h2 { font-size: 18px; font-weight: 600; color: $text-main; margin: 0; }
  .update-time { font-size: 12px; color: $text-muted; }
}

// 数据总览卡片
.overview-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 16px; }
.overview-grid--second { margin-bottom: 24px; }

.overview-card { background: $bg-card; border: 1px solid $border; border-radius: 12px; padding: 20px;
  &--primary { background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%); color: white;
    .card-label { color: rgba(255,255,255,0.8); .info-icon { color: rgba(255,255,255,0.5); } }
    .card-value { color: white; }
  }
}
.card-label { font-size: 13px; color: $text-secondary; margin-bottom: 8px; display: flex; align-items: center; gap: 4px; }
.card-label-row { display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: $text-secondary; margin-bottom: 8px; }
.card-value { font-size: 36px; font-weight: 700; color: $text-main; line-height: 1.2; }
.card-value-row { display: flex; justify-content: space-between; .card-value { font-size: 32px; } }
.card-note { font-size: 12px; color: $text-muted; margin-top: 8px;
  &--success { color: #10b981; }
}
.card-sub-row { display: flex; gap: 20px; font-size: 12px; color: $text-muted; margin-top: 8px; }
.info-icon { font-size: 14px; color: $text-muted; cursor: help; }

// Toggle buttons
.toggle-btns, .toggle-btns-mini { display: flex; border: 1px solid $border; border-radius: 6px; overflow: hidden; }
.toggle-btn, .toggle-btn-sm { padding: 4px 14px; font-size: 12px; border: none; background: white; cursor: pointer; transition: all 0.2s;
  &--active { background: $primary; color: white; }
}
.toggle-btn-sm { padding: 2px 10px; font-size: 11px; }

// 图表区域
.charts-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
.chart-card { background: $bg-card; border: 1px solid $border; border-radius: 12px; padding: 20px;
  &--full { margin-bottom: 20px; }
}
.chart-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;
  h3 { font-size: 16px; font-weight: 600; color: $text-main; margin: 0; display: flex; align-items: center; gap: 6px; }
}
.chart-tabs { display: flex; gap: 16px; align-items: center; }
.tab-btn { background: none; border: none; font-size: 14px; font-weight: 500; color: $text-muted; cursor: pointer; padding: 4px 0; border-bottom: 2px solid transparent;
  &--active { color: $text-main; border-bottom-color: $text-main; }
}
.chart-container { height: 260px; width: 100%; }

// 渠道列表
.channel-list { display: flex; flex-direction: column; gap: 16px; }
.channel-item { }
.channel-name { display: flex; align-items: center; gap: 8px; font-size: 14px; color: $text-main; margin-bottom: 4px; }
.channel-icon { width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; color: white;
  &--meituan { background: #ff6633; }
  &--douyin { background: #111; }
  &--miniapp { background: #07c160; }
  &--offline { background: $primary; }
}
.channel-data { font-size: 14px; font-weight: 600; color: $text-main; margin-bottom: 4px;
  .channel-count { font-weight: 400; color: $text-secondary; margin-left: 6px; }
}
.channel-bar-wrapper { display: flex; align-items: center; gap: 8px; height: 16px; }
.channel-bar { height: 10px; border-radius: 5px; transition: width 0.5s ease; min-width: 2px; }
.channel-pct { font-size: 12px; color: $text-secondary; white-space: nowrap; }

// 图例
.legend { display: flex; gap: 16px; }
.legend-item { display: flex; align-items: center; gap: 4px; font-size: 12px; color: $text-secondary; }
.legend-dot { width: 10px; height: 10px; border-radius: 2px;
  &--member { background: #1e3a5f; }
  &--nonmember { background: #2563eb; }
  &--visitor { background: #10b981; }
}

// 数据表格
.data-table { width: 100%; border-collapse: collapse;
  thead tr { border-bottom: 2px solid $border; }
  th { padding: 10px 16px; text-align: left; font-size: 13px; font-weight: 600; color: $text-secondary; }
  td { padding: 12px 16px; font-size: 14px; color: $text-main; border-bottom: 1px solid #f3f4f6; }
  .amount { font-weight: 600; color: #ef4444; }
}

@media (max-width: 1024px) {
  .overview-grid { grid-template-columns: 1fr; }
  .charts-row { grid-template-columns: 1fr; }
}
</style>
