<template>
  <div class="checkout-page">
    <!-- 结算清单面板 -->
    <div class="checkout-panel">
      <div class="panel-header">
        <h3>结算清单</h3>
        <el-input
          v-model="searchText"
          placeholder="搜索顾客..."
          prefix-icon="Search"
          clearable
          size="small"
          @input="handleSearch"
          style="width: 150px"
        />
        <el-button type="text" icon="Plus" size="small" @click="handleNewCustomer">新增顾客</el-button>
      </div>

      <!-- 订单列表 - 紧凑显示 -->
      <div class="orders-list">
        <div
          v-for="order in pendingOrders"
          :key="order.id"
          class="order-item"
          :class="{ selected: isOrderSelected(order.id) }"
          @click="toggleOrderSelection(order)"
        >
          <el-checkbox
            :model-value="isOrderSelected(order.id)"
            @update:model-value="toggleOrderSelection(order)"
            @click.stop
          />
          <div class="order-info">
            <div class="order-name">{{ order.customer_name }}</div>
            <div class="order-detail">{{ order.service_items?.join('、') || '服务' }}</div>
          </div>
          <div class="order-amount">¥{{ order.amount }}</div>
        </div>
        <div v-if="pendingOrders.length === 0" class="empty-list">
          暂无待结算订单
        </div>
      </div>

      <!-- 统计信息 -->
      <div class="summary-info">
        <div class="summary-row">
          <span>本单数量:</span>
          <span class="count">{{ selectedOrders.length }}</span>
        </div>
        <div class="summary-row total">
          <span>合计金额:</span>
          <span class="amount">¥{{ totalAmount.toFixed(2) }}</span>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <el-button @click="handleClear">取单</el-button>
        <el-button>挂单</el-button>
        <el-button
          type="primary"
          @click="handleBatchCheckout"
          :disabled="selectedOrders.length === 0"
          class="btn-checkout"
        >
          收银结账
        </el-button>
      </div>
    </div>

    <!-- 结账确认对话框 -->
    <el-dialog
      v-model="checkoutDialogVisible"
      title="确认结账"
      width="400px"
      @close="resetCheckoutForm"
    >
      <div class="checkout-form">
        <el-form :model="checkoutForm" label-width="100px">
          <el-form-item label="订单号">
            <span>{{ checkoutForm.order_no }}</span>
          </el-form-item>
          <el-form-item label="顾客名称">
            <span>{{ checkoutForm.customer_name }}</span>
          </el-form-item>
          <el-form-item label="金额">
            <span class="amount">¥{{ checkoutForm.amount }}</span>
          </el-form-item>
          <el-form-item label="支付方式">
            <el-select v-model="checkoutForm.payment_method" placeholder="请选择支付方式">
              <el-option label="现金" value="cash" />
              <el-option label="微信" value="wechat" />
              <el-option label="支付宝" value="alipay" />
              <el-option label="银行卡" value="card" />
            </el-select>
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <el-button @click="checkoutDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmCheckout" :loading="submitting">
          确认结账
        </el-button>
      </template>
    </el-dialog>

    <!-- 新增顾客对话框 -->
    <el-dialog
      v-model="newCustomerDialogVisible"
      title="新增顾客"
      width="500px"
      @close="resetCustomerForm"
    >
      <el-form :model="customerForm" label-width="100px">
        <el-form-item label="顾客名称">
          <el-input v-model="customerForm.name" placeholder="请输入顾客名称" />
        </el-form-item>
        <el-form-item label="联系电话">
          <el-input v-model="customerForm.phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="服务项目">
          <el-select v-model="customerForm.service_items" multiple placeholder="请选择服务项目">
            <el-option label="除湿排毒" value="除湿排毒" />
            <el-option label="艾灸精油" value="艾灸精油" />
            <el-option label="推拿按摩" value="推拿按摩" />
          </el-select>
        </el-form-item>
        <el-form-item label="金额">
          <el-input v-model="customerForm.amount" type="number" placeholder="请输入金额" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="newCustomerDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitNewCustomer" :loading="submitting">
          创建订单
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import * as ordersApi from '@/api/orders'
import * as customersApi from '@/api/customers'
import { formatDate } from '@/utils/date'

const route = useRoute()

const loading = ref(false)
const submitting = ref(false)
const searchText = ref('')
const orders = ref([])
const selectedOrders = ref([])
const checkoutDialogVisible = ref(false)
const newCustomerDialogVisible = ref(false)

const checkoutForm = ref({
  order_no: '',
  customer_name: '',
  amount: 0,
  payment_method: 'cash',
})

const customerForm = ref({
  name: '',
  phone: '',
  service_items: [],
  amount: 0,
})

const currentCheckoutOrder = ref(null)

// 计算待结算订单（状态为 pending）
const pendingOrders = computed(() => {
  return orders.value.filter(order => order.status === 'pending')
})

// 计算选中订单的总金额
const totalAmount = computed(() => {
  return selectedOrders.value.reduce((sum, order) => sum + (order.amount || 0), 0)
})

const handleSearch = () => {
  loadOrders()
}

const handleRefresh = () => {
  loadOrders()
}

const loadOrders = async () => {
  loading.value = true
  try {
    const params = {
      skip: 0,
      limit: 100,
      search: searchText.value || undefined,
      status: 'pending',
    }
    const response = await ordersApi.getOrders(params)
    orders.value = response.items || []
  } catch (error) {
    ElMessage.error('加载订单列表失败')
  } finally {
    loading.value = false
  }
}

const handleSelectionChange = (selection) => {
  selectedOrders.value = selection
}

const isOrderSelected = (orderId) => {
  return selectedOrders.value.some(order => order.id === orderId)
}

const toggleOrderSelection = (order) => {
  const index = selectedOrders.value.findIndex(o => o.id === order.id)
  if (index > -1) {
    selectedOrders.value.splice(index, 1)
  } else {
    selectedOrders.value.push(order)
  }
}

const handleClear = () => {
  selectedOrders.value = []
}

const handleCheckout = (order) => {
  currentCheckoutOrder.value = order
  checkoutForm.value = {
    order_no: order.order_no,
    customer_name: order.customer_name,
    amount: order.amount,
    payment_method: 'cash',
  }
  checkoutDialogVisible.value = true
}

const handleBatchCheckout = () => {
  if (selectedOrders.value.length === 0) {
    ElMessage.warning('请先选择要结账的订单')
    return
  }
  ElMessageBox.confirm(
    `确定要结账选中的 ${selectedOrders.value.length} 个订单，合计 ¥${totalAmount.value.toFixed(2)} 吗？`,
    '批量结账',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(async () => {
      submitting.value = true
      try {
        for (const order of selectedOrders.value) {
          await ordersApi.updateOrder(order.id, { status: 'completed' })
        }
        ElMessage.success('结账成功')
        selectedOrders.value = []
        await loadOrders()
      } catch (error) {
        ElMessage.error('结账失败')
      } finally {
        submitting.value = false
      }
    })
    .catch(() => {})
}

const handleCancel = async (order) => {
  ElMessageBox.confirm('确定要取消此订单吗？', '取消订单', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  })
    .then(async () => {
      try {
        await ordersApi.updateOrder(order.id, { status: 'cancelled' })
        ElMessage.success('取消成功')
        await loadOrders()
      } catch (error) {
        ElMessage.error('取消失败')
      }
    })
    .catch(() => {})
}

const resetCheckoutForm = () => {
  currentCheckoutOrder.value = null
  checkoutForm.value = {
    order_no: '',
    customer_name: '',
    amount: 0,
    payment_method: 'cash',
  }
}

const confirmCheckout = async () => {
  if (!checkoutForm.value.payment_method) {
    ElMessage.warning('请选择支付方式')
    return
  }
  submitting.value = true
  try {
    await ordersApi.updateOrder(currentCheckoutOrder.value.id, {
      status: 'completed',
      payment_method: checkoutForm.value.payment_method,
    })
    ElMessage.success('结账成功')
    checkoutDialogVisible.value = false
    resetCheckoutForm()
    await loadOrders()
  } catch (error) {
    ElMessage.error('结账失败')
  } finally {
    submitting.value = false
  }
}

const handleNewCustomer = () => {
  resetCustomerForm()
  newCustomerDialogVisible.value = true
}

const resetCustomerForm = () => {
  customerForm.value = {
    name: '',
    phone: '',
    service_items: [],
    amount: 0,
  }
}

const submitNewCustomer = async () => {
  if (!customerForm.value.name) {
    ElMessage.warning('请输入顾客名称')
    return
  }
  if (!customerForm.value.amount) {
    ElMessage.warning('请输入金额')
    return
  }

  submitting.value = true
  try {
    // 创建顾客
    const customerRes = await customersApi.createCustomer({
      name: customerForm.value.name,
      phone: customerForm.value.phone,
    })

    // 创建订单
    await ordersApi.createOrder({
      customer_id: customerRes.id,
      customer_name: customerForm.value.name,
      service_items: customerForm.value.service_items,
      amount: customerForm.value.amount,
      status: 'pending',
    })

    ElMessage.success('订单创建成功')
    newCustomerDialogVisible.value = false
    resetCustomerForm()
    await loadOrders()
  } catch (error) {
    ElMessage.error('创建订单失败')
  } finally {
    submitting.value = false
  }
}

const initPage = () => {
  loadOrders()
}

onMounted(() => {
  initPage()
})

watch(
  () => route.path,
  () => {
    if (route.path === '/checkout') {
      initPage()
    }
  }
)
</script>

<style scoped lang="scss">
.checkout-page {
  display: flex;
  height: 100%;
}

.checkout-panel {
  width: 380px;
  background: #f5f5f5;
  border-right: 1px solid #ddd;
  display: flex;
  flex-direction: column;
  padding: 0;

  .panel-header {
    background: #fff;
    padding: 15px;
    border-bottom: 1px solid #ddd;
    display: flex;
    align-items: center;
    gap: 8px;

    h3 {
      margin: 0;
      font-size: 16px;
      font-weight: 600;
      min-width: 60px;
    }

    :deep(.el-input) {
      flex: 1;
    }
  }

  .orders-list {
    flex: 1;
    overflow-y: auto;
    padding: 8px 0;
    background: #fff;

    .order-item {
      display: flex;
      align-items: center;
      padding: 12px 15px;
      border-bottom: 1px solid #f0f0f0;
      cursor: pointer;
      transition: background-color 0.2s;

      &:hover {
        background-color: #f9f9f9;
      }

      &.selected {
        background-color: #e8f4fd;
      }

      :deep(.el-checkbox) {
        margin-right: 8px;
      }

      .order-info {
        flex: 1;
        min-width: 0;

        .order-name {
          font-size: 14px;
          font-weight: 500;
          color: #333;
          margin-bottom: 4px;
        }

        .order-detail {
          font-size: 12px;
          color: #999;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
      }

      .order-amount {
        font-size: 14px;
        font-weight: 600;
        color: #ff5a3a;
        min-width: 60px;
        text-align: right;
      }
    }

    .empty-list {
      padding: 40px 15px;
      text-align: center;
      color: #999;
      font-size: 14px;
    }
  }

  .summary-info {
    background: #fff;
    padding: 15px;
    border-top: 1px solid #ddd;
    border-bottom: 1px solid #ddd;

    .summary-row {
      display: flex;
      justify-content: space-between;
      font-size: 14px;
      margin-bottom: 8px;

      &:last-child {
        margin-bottom: 0;
      }

      span {
        color: #666;

        &.count {
          font-weight: 600;
          color: #333;
        }

        &.amount {
          font-size: 18px;
          font-weight: 700;
          color: #ff5a3a;
        }
      }

      &.total {
        padding-top: 8px;
        border-top: 1px dashed #ddd;
      }
    }
  }

  .action-buttons {
    display: flex;
    gap: 8px;
    padding: 12px 15px;
    background: #fff;

    :deep(.el-button) {
      flex: 1;
      height: 40px;
      font-size: 14px;
    }

    .btn-checkout {
      background: #1e5aa8;
      border-color: #1e5aa8;

      &:hover {
        background: #154784;
        border-color: #154784;
      }
    }
  }
}

.checkout-form {
  padding: 10px 0;

  .amount {
    color: #ff5a3a;
    font-weight: 600;
  }

  :deep(.el-form-item__content) {
    color: #606266;
  }
}

@media (max-width: 768px) {
  .checkout-panel {
    width: 100%;
  }
}
</style>
