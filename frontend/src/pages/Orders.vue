<template>

    <div class="orders-page">
      <!-- 操作栏 -->
      <div class="action-bar">
        <div class="search-area">
          <el-input
            v-model="searchText"
            placeholder="搜索订单号或顾客名称..."
            prefix-icon="Search"
            clearable
            @input="handleSearch"
          />
          <el-select v-model="filterStatus" placeholder="订单状态" clearable class="filter-select">
            <el-option label="全部" value="" />
            <el-option label="待结算" value="pending" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
            <el-option label="已退单" value="refunded" />
          </el-select>
        </div>
        <div class="button-group">
          <el-button type="primary" @click="handleAdd">新增订单</el-button>
          <el-button @click="handleExport">导出数据</el-button>
        </div>
      </div>

      <!-- 订单列表 -->
      <el-card class="table-card">
        <el-table
          :data="orders"
          stripe
          :loading="loading"
          height="auto"
        >
          <el-table-column prop="order_no" label="订单号" min-width="150" />
          <el-table-column prop="customer_name" label="顾客名称" min-width="120" />
          <el-table-column prop="service_items" label="服务项目" min-width="200">
            <template #default="{ row }">
              <el-tag v-for="item in row.service_items" :key="item" style="margin-right: 5px">
                {{ item }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="amount" label="金额" width="100">
            <template #default="{ row }">
              <span class="amount">¥{{ row.amount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)">
                {{ getStatusLabel(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" min-width="160">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-link type="primary" @click="handleView(row)">查看</el-link>
              <el-divider direction="vertical" />
              <el-link type="primary" @click="handleEdit(row)">编辑</el-link>
              <el-divider direction="vertical" />
              <el-popconfirm
                title="确定删除此订单吗？"
                @confirm="handleDelete(row.id)"
              >
                <template #reference>
                  <el-link type="danger">删除</el-link>
                </template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="pagination">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total"
            @current-page-change="loadOrders"
            @page-size-change="loadOrders"
          />
        </div>
      </el-card>

      <!-- 新增/编辑对话框 -->
      <order-dialog v-model="dialogVisible" :order="editingOrder" @save="handleSave" />

      <!-- 订单详情抽屉 -->
      <order-drawer v-model="drawerVisible" :order-id="viewingOrderId" />

      <!-- 支付对话框 -->
      <order-payment-dialog v-model="paymentDialogVisible" :order-id="payingOrderId" @save="handleSave" />
    </div>

</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import OrderDialog from '@/components/dialogs/OrderDialog.vue'
import OrderDrawer from '@/components/drawers/OrderDrawer.vue'
import OrderPaymentDialog from '@/components/dialogs/OrderPaymentDialog.vue'
import * as ordersApi from '@/api/orders'
import { formatDate } from '@/utils/date'

const route = useRoute()

const loading = ref(false)
const searchText = ref('')
const filterStatus = ref('')
const orders = ref([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const dialogVisible = ref(false)
const drawerVisible = ref(false)
const paymentDialogVisible = ref(false)
const editingOrder = ref(null)
const viewingOrderId = ref(null)
const payingOrderId = ref(null)

const handleSearch = () => {
  currentPage.value = 1
  loadOrders()
}

const loadOrders = async () => {
  loading.value = true
  try {
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
      search: searchText.value || undefined,
      status: filterStatus.value || undefined,
    }
    const response = await ordersApi.getOrders(params)
    orders.value = response.items || []
    total.value = response.total || 0
  } catch (error) {
    ElMessage.error('加载订单列表失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  editingOrder.value = null
  dialogVisible.value = true
}

const handleEdit = (row) => {
  editingOrder.value = { ...row }
  dialogVisible.value = true
}

const handleView = (row) => {
  viewingOrderId.value = row.id
  drawerVisible.value = true
}

const handleDelete = async (orderId) => {
  try {
    await ordersApi.deleteOrder(orderId)
    ElMessage.success('删除成功')
    await loadOrders()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

const handleSave = async () => {
  dialogVisible.value = false
  paymentDialogVisible.value = false
  await loadOrders()
}

const handleExport = async () => {
  try {
    const blob = await ordersApi.exportOrders()
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `orders-${Date.now()}.xlsx`
    link.click()
    URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

const getStatusType = (status) => {
  const statusMap = {
    completed: 'success',
    pending: 'warning',
    cancelled: 'danger',
    refunded: 'info',
  }
  return statusMap[status] || 'info'
}

const getStatusLabel = (status) => {
  const statusMap = {
    completed: '已完成',
    pending: '待结算',
    cancelled: '已取消',
    refunded: '已退单',
  }
  return statusMap[status] || status
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
    if (route.path === '/orders') {
      initPage()
    }
  }
)
</script>

<style scoped lang="scss">
.orders-page {
  .action-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
    margin-bottom: 20px;
    flex-wrap: wrap;

    .search-area {
      display: flex;
      gap: 10px;
      flex: 1;
      min-width: 300px;

      :deep(.el-input) {
        flex: 1;
      }

      .filter-select {
        width: 150px;
      }
    }

    .button-group {
      display: flex;
      gap: 10px;
    }
  }

  .table-card {
    .amount {
      color: #f56c6c;
      font-weight: 600;
    }

    .pagination {
      display: flex;
      justify-content: flex-end;
      margin-top: 20px;
    }
  }
}
</style>
