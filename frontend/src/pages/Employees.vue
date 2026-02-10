<template>

    <div class="employees-page">
      <!-- 操作栏 -->
      <div class="action-bar">
        <div class="search-area">
          <el-input
            v-model="searchText"
            placeholder="搜索员工名称或ID..."
            prefix-icon="Search"
            clearable
            @input="handleSearch"
          />
          <el-select v-model="filterPosition" placeholder="岗位筛选" clearable class="filter-select">
            <el-option label="全部" value="" />
            <el-option label="店长" value="店长" />
            <el-option label="调理师" value="调理师" />
            <el-option label="收银员" value="收银员" />
            <el-option label="前台" value="前台" />
          </el-select>
        </div>
        <div class="button-group">
          <el-button type="primary" @click="handleAdd">新增员工</el-button>
          <el-button @click="handleExport">导出数据</el-button>
        </div>
      </div>

      <!-- 员工列表 -->
      <el-card class="table-card">
        <el-table
          :data="employees"
          stripe
          :loading="loading"
          height="auto"
        >
          <el-table-column prop="name" label="员工名称" min-width="120" />
          <el-table-column prop="employee_id" label="员工ID" width="120" />
          <el-table-column prop="position" label="岗位" width="100" />
          <el-table-column prop="phone" label="电话" min-width="130" />
          <el-table-column prop="hire_date" label="入职日期" width="120">
            <template #default="{ row }">
              {{ formatDate(row.hire_date, 'yyyy-MM-dd') }}
            </template>
          </el-table-column>
          <el-table-column label="实名认证" width="100">
            <template #default="{ row }">
              <el-tag :type="row.real_name_verified ? 'success' : 'danger'">
                {{ row.real_name_verified ? '已认证' : '未认证' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="状态" width="80">
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
                title="确定删除此员工吗？"
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
            @current-page-change="loadEmployees"
            @page-size-change="loadEmployees"
          />
        </div>
      </el-card>

      <!-- 新增/编辑对话框 -->
      <employee-dialog v-model="dialogVisible" :employee="editingEmployee" @save="handleSave" />

      <!-- 员工详情抽屉 -->
      <employee-drawer v-model="drawerVisible" :employee-id="viewingEmployeeId" />
    </div>

</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import EmployeeDialog from '@/components/dialogs/EmployeeDialog.vue'
import EmployeeDrawer from '@/components/drawers/EmployeeDrawer.vue'
import * as employeesApi from '@/api/employees'
import { formatDate } from '@/utils/date'

const route = useRoute()

const loading = ref(false)
const searchText = ref('')
const filterPosition = ref('')
const employees = ref([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const dialogVisible = ref(false)
const drawerVisible = ref(false)
const editingEmployee = ref(null)
const viewingEmployeeId = ref(null)

const handleSearch = () => {
  currentPage.value = 1
  loadEmployees()
}

const loadEmployees = async () => {
  loading.value = true
  try {
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
      search: searchText.value || undefined,
      position: filterPosition.value || undefined,
    }
    const response = await employeesApi.getEmployees(params)
    employees.value = response.items || []
    total.value = response.total || 0
  } catch (error) {
    ElMessage.error('加载员工列表失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  editingEmployee.value = null
  dialogVisible.value = true
}

const handleEdit = (row) => {
  editingEmployee.value = { ...row }
  dialogVisible.value = true
}

const handleView = (row) => {
  viewingEmployeeId.value = row.id
  drawerVisible.value = true
}

const handleDelete = async (employeeId) => {
  try {
    await employeesApi.deleteEmployee(employeeId)
    ElMessage.success('删除成功')
    await loadEmployees()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

const handleStatusChange = async (row) => {
  try {
    await employeesApi.updateEmployee(row.id, { status: row.status })
    ElMessage.success('状态更新成功')
  } catch (error) {
    ElMessage.error('状态更新失败')
  }
}

const handleSave = async () => {
  dialogVisible.value = false
  await loadEmployees()
}

const handleExport = async () => {
  try {
    const blob = await employeesApi.exportEmployees()
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `employees-${Date.now()}.xlsx`
    link.click()
    URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

const initPage = () => {
  loadEmployees()
}

onMounted(() => {
  initPage()
})

watch(
  () => route.path,
  () => {
    if (route.path === '/employees') {
      initPage()
    }
  }
)
</script>

<style scoped lang="scss">
.employees-page {
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
    .pagination {
      display: flex;
      justify-content: flex-end;
      margin-top: 20px;
    }
  }
}
</style>
