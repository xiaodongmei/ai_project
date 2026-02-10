<template>
  <el-drawer
    :model-value="modelValue"
    title="员工详情"
    size="50%"
    @close="handleClose"
  >
    <div v-if="loading" class="loading">
      <el-skeleton :rows="5" />
    </div>

    <div v-else-if="employee" class="employee-detail">
      <!-- 基本信息 -->
      <el-card class="detail-card">
        <template #header>
          <span>基本信息</span>
        </template>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="员工名称">{{ employee.name }}</el-descriptions-item>
          <el-descriptions-item label="员工ID">{{ employee.employee_id }}</el-descriptions-item>
          <el-descriptions-item label="手机号">{{ employee.phone }}</el-descriptions-item>
          <el-descriptions-item label="岗位">{{ employee.position }}</el-descriptions-item>
          <el-descriptions-item label="员工等级">{{ employee.level }}</el-descriptions-item>
          <el-descriptions-item label="入职日期">{{ formatDate(employee.hire_date, 'yyyy-MM-dd') }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 认证和状态 -->
      <el-card class="detail-card">
        <template #header>
          <span>认证和状态</span>
        </template>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="实名认证">
            <el-tag :type="employee.real_name_verified ? 'success' : 'danger'">
              {{ employee.real_name_verified ? '已认证' : '未认证' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="员工状态">
            <el-tag :type="employee.status === 'active' ? 'success' : 'danger'">
              {{ employee.status === 'active' ? '在职' : '离职' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="身份证号">{{ employee.id_number }}</el-descriptions-item>
          <el-descriptions-item label="基础薪资">¥{{ employee.salary || 0 }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 绩效统计 -->
      <el-card class="detail-card">
        <template #header>
          <span>绩效统计</span>
        </template>
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="stat-item">
              <p class="stat-label">总业绩</p>
              <p class="stat-value">¥{{ employee.total_performance || 0 }}</p>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="stat-item">
              <p class="stat-label">累计提成</p>
              <p class="stat-value">¥{{ employee.total_commission || 0 }}</p>
            </div>
          </el-col>
        </el-row>
        <el-divider />
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="stat-item">
              <p class="stat-label">接待客户数</p>
              <p class="stat-value">{{ employee.customer_count || 0 }}</p>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="stat-item">
              <p class="stat-label">成交订单数</p>
              <p class="stat-value">{{ employee.order_count || 0 }}</p>
            </div>
          </el-col>
        </el-row>
      </el-card>

      <!-- 最近订单 -->
      <el-card class="detail-card">
        <template #header>
          <span>最近接待订单</span>
        </template>
        <el-table :data="orders" max-height="300" stripe>
          <el-table-column prop="order_no" label="订单号" width="120" />
          <el-table-column prop="customer_name" label="顾客" width="100" />
          <el-table-column prop="amount" label="金额" width="80">
            <template #default="{ row }">
              ¥{{ row.amount }}
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
import * as employeesApi from '@/api/employees'
import { formatDate } from '@/utils/date'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  employeeId: {
    type: [String, Number],
    default: null,
  },
})

const emit = defineEmits(['update:modelValue'])

const loading = ref(false)
const employee = ref(null)
const orders = ref([])

const loadEmployeeDetail = async () => {
  if (!props.employeeId) return

  loading.value = true
  try {
    const response = await employeesApi.getEmployeeDetail(props.employeeId)
    employee.value = response

    const ordersResponse = await employeesApi.getEmployeeOrders(props.employeeId, { limit: 10 })
    orders.value = ordersResponse.items || []
  } catch (error) {
    ElMessage.error('加载员工详情失败')
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
      loadEmployeeDetail()
    }
  }
)
</script>

<style scoped lang="scss">
.employee-detail {
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
      font-size: 18px;
      color: #409eff;
      font-weight: 600;
      margin: 8px 0 0 0;
    }
  }
}
</style>
