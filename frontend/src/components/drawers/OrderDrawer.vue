<template>
  <el-drawer
    :model-value="modelValue"
    title="订单详情"
    size="50%"
    @close="handleClose"
  >
    <div v-if="loading" class="loading">
      <el-skeleton :rows="5" />
    </div>

    <div v-else-if="order" class="order-detail">
      <!-- 基本信息 -->
      <el-card class="detail-card">
        <template #header>
          <span>基本信息</span>
        </template>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="订单号">{{ order.order_no }}</el-descriptions-item>
          <el-descriptions-item label="顾客名称">{{ order.customer_name }}</el-descriptions-item>
          <el-descriptions-item label="服务员">{{ order.employee_name }}</el-descriptions-item>
          <el-descriptions-item label="订单状态">
            <el-tag :type="getStatusType(order.status)">
              {{ getStatusLabel(order.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">
            {{ formatDate(order.created_at) }}
          </el-descriptions-item>
          <el-descriptions-item label="完成时间" v-if="order.completed_at">
            {{ formatDate(order.completed_at) }}
          </el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 服务项目 -->
      <el-card class="detail-card">
        <template #header>
          <span>服务项目</span>
        </template>
        <div v-if="order.service_items && order.service_items.length > 0">
          <el-tag v-for="item in order.service_items" :key="item" style="margin-right: 8px; margin-bottom: 8px">
            {{ item }}
          </el-tag>
        </div>
        <div v-else class="empty-state">暂无服务项目</div>
      </el-card>

      <!-- 金额信息 -->
      <el-card class="detail-card">
        <template #header>
          <span>金额信息</span>
        </template>
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="stat-item">
              <p class="stat-label">订单金额</p>
              <p class="stat-value">¥{{ order.amount || 0 }}</p>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="stat-item">
              <p class="stat-label">折扣</p>
              <p class="stat-value">¥{{ order.discount || 0 }}</p>
            </div>
          </el-col>
        </el-row>
        <el-divider />
        <div class="stat-item" style="text-align: right">
          <p class="stat-label">实付金额</p>
          <p class="stat-value" style="color: #f56c6c; font-size: 20px">
            ¥{{ (order.amount || 0) - (order.discount || 0) }}
          </p>
        </div>
      </el-card>

      <!-- 支付信息 -->
      <el-card class="detail-card">
        <template #header>
          <span>支付信息</span>
        </template>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="支付方式">
            {{ getPaymentMethodLabel(order.payment_method) }}
          </el-descriptions-item>
          <el-descriptions-item label="支付状态">
            <el-tag v-if="order.status === 'completed'" type="success">已支付</el-tag>
            <el-tag v-else type="warning">未支付</el-tag>
          </el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <el-button @click="handleClose">关闭</el-button>
        <el-button type="primary" @click="handlePay" v-if="order.status !== 'completed'">
          付款
        </el-button>
        <el-button type="success" @click="handleComplete" v-if="order.status === 'pending'">
          完成订单
        </el-button>
        <el-button type="danger" @click="handleCancel" v-if="order.status !== 'completed'">
          取消订单
        </el-button>
      </div>
    </div>
  </el-drawer>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import * as ordersApi from '@/api/orders'
import { formatDate } from '@/utils/date'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  orderId: {
    type: [String, Number],
    default: null,
  },
})

const emit = defineEmits(['update:modelValue'])

const loading = ref(false)
const order = ref(null)

const getStatusType = (status) => {
  const map = {
    completed: 'success',
    pending: 'warning',
    cancelled: 'danger',
  }
  return map[status] || 'info'
}

const getStatusLabel = (status) => {
  const map = {
    completed: '已完成',
    pending: '待结算',
    cancelled: '已取消',
  }
  return map[status] || status
}

const getPaymentMethodLabel = (method) => {
  const map = {
    wechat: '微信支付',
    alipay: '支付宝',
    cash: '现金',
    card: '刷卡',
  }
  return map[method] || method
}

const loadOrderDetail = async () => {
  if (!props.orderId) return

  loading.value = true
  try {
    const response = await ordersApi.getOrderDetail(props.orderId)
    order.value = response
  } catch (error) {
    ElMessage.error('加载订单详情失败')
  } finally {
    loading.value = false
  }
}

const handlePay = () => {
  // 触发支付对话框
  emit('pay', props.orderId)
}

const handleComplete = async () => {
  try {
    await ordersApi.completeOrder(props.orderId)
    ElMessage.success('订单已完成')
    await loadOrderDetail()
  } catch (error) {
    ElMessage.error('完成订单失败')
  }
}

const handleCancel = async () => {
  try {
    await ordersApi.cancelOrder(props.orderId, '用户取消')
    ElMessage.success('订单已取消')
    await loadOrderDetail()
  } catch (error) {
    ElMessage.error('取消订单失败')
  }
}

const handleClose = () => {
  emit('update:modelValue', false)
}

watch(
  () => props.modelValue,
  (newVal) => {
    if (newVal) {
      loadOrderDetail()
    }
  }
)
</script>

<style scoped lang="scss">
.order-detail {
  .detail-card {
    margin-bottom: 20px;

    :deep(.el-card__header) {
      border-bottom: 1px solid #ebeef5;
      padding: 15px;
      background-color: #f5f7fa;
    }
  }

  .stat-item {
    padding: 10px;

    .stat-label {
      font-size: 12px;
      color: #909399;
      margin: 0;
    }

    .stat-value {
      font-size: 18px;
      color: #f56c6c;
      font-weight: 600;
      margin: 8px 0 0 0;
    }
  }

  .empty-state {
    text-align: center;
    padding: 20px;
    color: #909399;
  }

  .action-buttons {
    display: flex;
    gap: 10px;
    margin-top: 20px;
  }
}
</style>
