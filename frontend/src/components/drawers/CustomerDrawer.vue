<template>
  <el-drawer
    :model-value="modelValue"
    title="顾客详情"
    size="50%"
    @close="handleClose"
  >
    <div v-if="loading" class="loading">
      <el-skeleton :rows="5" />
    </div>

    <div v-else-if="customer" class="customer-detail">
      <!-- 基本信息 -->
      <el-card class="detail-card">
        <template #header>
          <span>基本信息</span>
        </template>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="顾客名称">{{ customer.name }}</el-descriptions-item>
          <el-descriptions-item label="手机号">{{ customer.phone }}</el-descriptions-item>
          <el-descriptions-item label="微信ID">{{ customer.wechat_id }}</el-descriptions-item>
          <el-descriptions-item label="客户类型">
            <el-tag :type="customer.customer_type === 'member' ? 'success' : 'info'">
              {{ customer.customer_type === 'member' ? '会员' : '非会员' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="customer.status === 'active' ? 'success' : 'danger'">
              {{ customer.status === 'active' ? '启用' : '禁用' }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 消费统计 -->
      <el-card class="detail-card">
        <template #header>
          <span>消费统计</span>
        </template>
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="stat-item">
              <p class="stat-label">累计消费</p>
              <p class="stat-value">¥{{ customer.total_consumption || 0 }}</p>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="stat-item">
              <p class="stat-label">消费次数</p>
              <p class="stat-value">{{ customer.order_count || 0 }}次</p>
            </div>
          </el-col>
        </el-row>
      </el-card>

      <!-- 会员信息 -->
      <el-card v-if="customer.customer_type === 'member'" class="detail-card">
        <template #header>
          <span>会员信息</span>
        </template>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="会员等级">
            {{ customer.member_level || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="会员余额">
            ¥{{ customer.member_balance || 0 }}
          </el-descriptions-item>
          <el-descriptions-item label="积分">
            {{ customer.points || 0 }}
          </el-descriptions-item>
          <el-descriptions-item label="有效卡数">
            {{ customer.valid_cards || 0 }}张
          </el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 消费记录 -->
      <el-card class="detail-card">
        <template #header>
          <span>最近消费记录</span>
        </template>
        <el-table :data="orders" max-height="300" stripe>
          <el-table-column prop="order_no" label="订单号" width="120" />
          <el-table-column prop="service_name" label="服务项目" width="150" />
          <el-table-column prop="amount" label="金额" width="100">
            <template #default="{ row }">
              ¥{{ row.amount }}
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)">
                {{ getStatusLabel(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="时间" width="150">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
  </el-drawer>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import * as customersApi from '@/api/customers'
import { formatDate } from '@/utils/date'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  customerId: {
    type: [String, Number],
    default: null,
  },
})

const emit = defineEmits(['update:modelValue'])

const loading = ref(false)
const customer = ref(null)
const orders = ref([])

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
    pending: '待处理',
    cancelled: '已取消',
  }
  return map[status] || status
}

const loadCustomerDetail = async () => {
  if (!props.customerId) return

  loading.value = true
  try {
    const response = await customersApi.getCustomerDetail(props.customerId)
    customer.value = response

    const ordersResponse = await customersApi.getCustomerOrders(props.customerId, {
      limit: 10,
    })
    orders.value = ordersResponse.items || []
  } catch (error) {
    ElMessage.error('加载顾客详情失败')
  } finally {
    loading.value = false
  }
}

const handleClose = () => {
  emit('update:modelValue', false)
}

watch(
  () => props.modelValue,
  (newVal) => {
    if (newVal) {
      loadCustomerDetail()
    }
  }
)
</script>

<style scoped lang="scss">
.customer-detail {
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
    text-align: center;

    .stat-label {
      font-size: 12px;
      color: #909399;
      margin: 0;
    }

    .stat-value {
      font-size: 20px;
      color: #f56c6c;
      font-weight: 600;
      margin: 8px 0 0 0;
    }
  }
}
</style>
