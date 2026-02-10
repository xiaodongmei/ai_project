<template>
  <div class="customers-page">
    <!-- 操作栏 -->
    <div class="action-bar">
      <div class="search-area">
        <el-input
          v-model="searchText"
          placeholder="搜索顾客名称或手机号..."
          prefix-icon="Search"
          clearable
          @input="handleSearch"
        />
        <el-select v-model="filterType" placeholder="客户类型" clearable class="filter-select">
          <el-option label="全部" value="" />
          <el-option label="会员" value="member" />
          <el-option label="非会员" value="non-member" />
        </el-select>
      </div>
      <div class="button-group">
        <el-button type="primary" @click="handleAdd">新增顾客</el-button>
        <el-button @click="handleImport">批量导入</el-button>
        <el-button @click="handleExport">导出数据</el-button>
      </div>
    </div>

    <!-- 顾客列表 -->
    <el-card class="table-card">
      <el-table
        :data="customers"
        stripe
        :loading="loading"
        @selection-change="handleSelectionChange"
        height="auto"
      >
        <el-table-column type="selection" width="50" />
        <el-table-column prop="name" label="顾客名称" min-width="120" />
        <el-table-column prop="phone" label="手机号" min-width="130" />
        <el-table-column prop="wechat_id" label="微信ID" min-width="140" />
        <el-table-column prop="customer_type" label="客户类型" width="100">
          <template #default="{ row }">
            <el-tag :type="row.customer_type === 'member' ? 'success' : 'info'">
              {{ row.customer_type === 'member' ? '会员' : '非会员' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="total_consumption" label="累计消费" width="120">
          <template #default="{ row }">
            <span class="amount">¥{{ row.total_consumption || 0 }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="last_consume_time" label="最后消费时间" min-width="160">
          <template #default="{ row }">
            {{ formatDate(row.last_consume_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-switch
              v-model="row.status"
              active-value="active"
              inactive-value="inactive"
              @change="handleStatusChange(row)"
            />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-link type="primary" @click="handleView(row)">查看</el-link>
            <el-divider direction="vertical" />
            <el-link type="primary" @click="handleEdit(row)">编辑</el-link>
            <el-divider direction="vertical" />
            <el-popconfirm
              title="确定删除此顾客吗？"
              confirm-button-text="确定"
              cancel-button-text="取消"
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
          @current-page-change="handlePageChange"
          @page-size-change="handlePageSizeChange"
        />
      </div>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <customer-dialog v-model="dialogVisible" :customer="editingCustomer" @save="handleSave" />

    <!-- 顾客详情抽屉 -->
    <customer-drawer v-model="drawerVisible" :customer-id="viewingCustomerId" />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import CustomerDialog from '@/components/dialogs/CustomerDialog.vue'
import CustomerDrawer from '@/components/drawers/CustomerDrawer.vue'
import * as customersApi from '@/api/customers'
import { formatDate } from '@/utils/date'

const route = useRoute()

const loading = ref(false)
const searchText = ref('')
const filterType = ref('')
const customers = ref([])
const selectedCustomers = ref([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const dialogVisible = ref(false)
const drawerVisible = ref(false)
const editingCustomer = ref(null)
const viewingCustomerId = ref(null)

const handleSearch = async () => {
  currentPage.value = 1
  await loadCustomers()
}

const loadCustomers = async () => {
  loading.value = true
  try {
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
      search: searchText.value || undefined,
      customer_type: filterType.value || undefined,
    }
    const response = await customersApi.getCustomers(params)
    customers.value = response.items || []
    total.value = response.total || 0
  } catch (error) {
    ElMessage.error('加载顾客列表失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  editingCustomer.value = null
  dialogVisible.value = true
}

const handleEdit = (row) => {
  editingCustomer.value = { ...row }
  dialogVisible.value = true
}

const handleView = (row) => {
  viewingCustomerId.value = row.id
  drawerVisible.value = true
}

const handleDelete = async (customerId) => {
  try {
    await customersApi.deleteCustomer(customerId)
    ElMessage.success('删除成功')
    await loadCustomers()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

const handleStatusChange = async (row) => {
  try {
    await customersApi.updateCustomer(row.id, { status: row.status })
    // 移除成功提示，避免页面加载时重复显示
  } catch (error) {
    ElMessage.error('状态更新失败')
    // 失败时恢复原状态
    row.status = row.status === 'active' ? 'inactive' : 'active'
  }
}

const handleSave = async () => {
  dialogVisible.value = false
  await loadCustomers()
}

const handleImport = () => {
  // 处理批量导入
  ElMessage.info('导入功能开发中...')
}

const handleExport = async () => {
  try {
    const blob = await customersApi.exportCustomers()
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `customers-${Date.now()}.xlsx`
    link.click()
    URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

const handleSelectionChange = (selection) => {
  selectedCustomers.value = selection
}

const handlePageChange = () => {
  loadCustomers()
}

const handlePageSizeChange = () => {
  currentPage.value = 1
  loadCustomers()
}

onMounted(() => {
  loadCustomers()
})

watch(
  () => route.path,
  () => {
    if (route.path === '/customers') {
      loadCustomers()
    }
  }
)
</script>

<style scoped lang="scss">
.customers-page {
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

@media (max-width: 768px) {
  .customers-page .action-bar {
    flex-direction: column;
    align-items: stretch;

    .search-area {
      width: 100%;
      flex-direction: column;
    }

    .button-group {
      flex-direction: column;

      :deep(.el-button) {
        width: 100%;
      }
    }
  }
}
</style>
