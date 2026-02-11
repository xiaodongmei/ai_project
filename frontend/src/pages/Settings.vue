<template>

    <div class="settings-page">
      <el-row :gutter="20">
        <!-- 左侧菜单 -->
        <el-col :xs="24" :sm="24" :md="6">
          <div class="settings-menu">
            <div
              v-for="item in menuItems"
              :key="item.name"
              :class="['menu-item', { active: activeTab === item.name }]"
              @click="activeTab = item.name"
            >
              <el-icon>
                <component :is="item.icon" />
              </el-icon>
              <span>{{ item.label }}</span>
            </div>
          </div>
        </el-col>

        <!-- 右侧内容 -->
        <el-col :xs="24" :sm="24" :md="18">
          <!-- 店铺设置 -->
          <el-card v-show="activeTab === 'shop'" class="settings-card">
            <template #header>
              <span>店铺基本信息</span>
            </template>
            <el-form :model="shopSettings" label-width="120px">
              <el-form-item label="行业类型">
                <el-select v-model="currentIndustry" placeholder="请选择行业类型" @change="handleIndustryChange">
                  <el-option
                    v-for="(tmpl, key) in industryTemplates"
                    :key="key"
                    :label="tmpl.name"
                    :value="key"
                  >
                    <span>{{ tmpl.name }}</span>
                    <span style="color: #999; font-size: 12px; margin-left: 8px;">{{ tmpl.description }}</span>
                  </el-option>
                </el-select>
              </el-form-item>

              <el-form-item label="店铺名称">
                <el-input v-model="shopSettings.name" />
              </el-form-item>

              <el-form-item label="店铺地址">
                <el-input v-model="shopSettings.address" />
              </el-form-item>

              <el-form-item label="联系电话">
                <el-input v-model="shopSettings.phone" />
              </el-form-item>

              <el-form-item label="营业时间">
                <el-input v-model="shopSettings.business_hours" />
              </el-form-item>

              <el-form-item label="店铺描述">
                <el-input
                  v-model="shopSettings.description"
                  type="textarea"
                  :rows="4"
                />
              </el-form-item>

              <el-button type="primary" @click="handleSaveShopSettings">保存设置</el-button>
            </el-form>
          </el-card>

          <!-- 营业设置 -->
          <el-card v-show="activeTab === 'business'" class="settings-card">
            <template #header>
              <span>营业设置</span>
            </template>
            <el-form :model="businessSettings" label-width="120px">
              <el-form-item label="默认折扣">
                <el-input-number v-model="businessSettings.defaultDiscount" :precision="2" />
              </el-form-item>

              <el-form-item label="会员折扣">
                <el-input-number v-model="businessSettings.memberDiscount" :precision="2" />
              </el-form-item>

              <el-form-item label="最低消费">
                <el-input-number v-model="businessSettings.minConsumption" :precision="2" />
              </el-form-item>

              <el-form-item label="积分兑换比例">
                <el-input-number v-model="businessSettings.pointsRate" />
              </el-form-item>

              <el-button type="primary" @click="handleSaveSettings">保存设置</el-button>
            </el-form>
          </el-card>

          <!-- 通知设置 -->
          <el-card v-show="activeTab === 'notification'" class="settings-card">
            <template #header>
              <span>通知设置</span>
            </template>
            <el-form :model="notificationSettings" label-width="120px">
              <el-form-item label="订单提醒">
                <el-switch v-model="notificationSettings.orderNotify" />
              </el-form-item>

              <el-form-item label="库存预警">
                <el-switch v-model="notificationSettings.stockNotify" />
              </el-form-item>

              <el-form-item label="低库存数量">
                <el-input-number v-model="notificationSettings.lowStockLevel" :min="0" />
              </el-form-item>

              <el-form-item label="员工打卡提醒">
                <el-switch v-model="notificationSettings.checkinNotify" />
              </el-form-item>

              <el-form-item label="营业报告">
                <el-switch v-model="notificationSettings.dailyReport" />
              </el-form-item>

              <el-button type="primary" @click="handleSaveSettings">保存设置</el-button>
            </el-form>
          </el-card>

          <!-- 权限管理 -->
          <el-card v-show="activeTab === 'permission'" class="settings-card">
            <template #header>
              <span>权限管理</span>
            </template>
            <el-table :data="permissions" stripe style="margin-bottom: 20px">
              <el-table-column prop="name" label="权限名称" width="150" />
              <el-table-column prop="description" label="权限描述" />
              <el-table-column label="状态" width="100">
                <template #default="{ row }">
                  <el-switch v-model="row.enabled" />
                </template>
              </el-table-column>
            </el-table>
            <el-button type="primary" @click="handleSaveSettings">保存权限</el-button>
          </el-card>

          <!-- 服务项目管理 -->
          <el-card v-show="activeTab === 'services'" class="settings-card">
            <template #header>
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span>服务项目管理</span>
                <div>
                  <el-button size="small" @click="handleResetServices">重置为模板默认</el-button>
                  <el-button type="primary" size="small" @click="handleAddService">添加服务</el-button>
                </div>
              </div>
            </template>
            <el-table :data="serviceItems" stripe>
              <el-table-column prop="name" label="服务名称" min-width="120" />
              <el-table-column prop="category" label="所属分类" width="120" />
              <el-table-column prop="duration" label="时长(分钟)" width="100" />
              <el-table-column prop="price" label="价格(¥)" width="100">
                <template #default="{ row }">
                  ¥{{ row.price }}
                </template>
              </el-table-column>
              <el-table-column prop="is_active" label="状态" width="80">
                <template #default="{ row }">
                  <el-tag :type="row.is_active ? 'success' : 'info'" size="small">
                    {{ row.is_active ? '启用' : '停用' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="150" fixed="right">
                <template #default="{ row }">
                  <el-link type="primary" @click="handleEditService(row)">编辑</el-link>
                  <el-divider direction="vertical" />
                  <el-popconfirm title="确定删除此服务项目？" @confirm="handleDeleteService(row.id)">
                    <template #reference>
                      <el-link type="danger">删除</el-link>
                    </template>
                  </el-popconfirm>
                </template>
              </el-table-column>
            </el-table>
          </el-card>

          <!-- 服务项目编辑对话框 -->
          <el-dialog v-model="serviceDialogVisible" :title="editingService ? '编辑服务项目' : '添加服务项目'" width="480px">
            <el-form :model="serviceForm" label-width="100px">
              <el-form-item label="服务名称" required>
                <el-input v-model="serviceForm.name" placeholder="请输入服务名称" />
              </el-form-item>
              <el-form-item label="所属分类">
                <el-select v-model="serviceForm.category" placeholder="请选择分类" filterable allow-create>
                  <el-option
                    v-for="cat in shopConfig.serviceCategories"
                    :key="cat"
                    :label="cat"
                    :value="cat"
                  />
                </el-select>
              </el-form-item>
              <el-form-item label="时长(分钟)">
                <el-input-number v-model="serviceForm.duration" :min="10" :step="10" />
              </el-form-item>
              <el-form-item label="价格(¥)">
                <el-input-number v-model="serviceForm.price" :min="0" :precision="2" />
              </el-form-item>
              <el-form-item label="状态">
                <el-switch v-model="serviceForm.is_active" active-text="启用" inactive-text="停用" />
              </el-form-item>
              <el-form-item label="描述">
                <el-input v-model="serviceForm.description" type="textarea" :rows="2" placeholder="可选描述" />
              </el-form-item>
            </el-form>
            <template #footer>
              <el-button @click="serviceDialogVisible = false">取消</el-button>
              <el-button type="primary" @click="handleSaveService">保存</el-button>
            </template>
          </el-dialog>

          <!-- 备份和恢复 -->
          <el-card v-show="activeTab === 'backup'" class="settings-card">
            <template #header>
              <span>备份和恢复</span>
            </template>
            <div class="backup-section">
              <p>最后备份时间: {{ lastBackupTime }}</p>
              <div style="margin: 20px 0">
                <el-button type="primary" @click="handleBackup">立即备份</el-button>
                <el-button @click="handleRestore">恢复备份</el-button>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Shop,
  Setting,
  Bell,
  User,
  Download,
  List,
} from '@element-plus/icons-vue'
import { useShopConfigStore } from '@/store/shopConfig'
import * as configApi from '@/api/config'
import * as serviceItemsApi from '@/api/serviceItems'

const shopConfig = useShopConfigStore()
const industryTemplates = ref({})
const currentIndustry = ref('')

onMounted(async () => {
  // 加载行业模板列表
  try {
    const res = await configApi.getIndustryTemplates()
    industryTemplates.value = res || {}
  } catch (e) {
    industryTemplates.value = {}
  }
  currentIndustry.value = shopConfig.industryType
  // 加载服务项目
  await loadServiceItems()
  // 同步店铺设置
  shopSettings.value.name = shopConfig.shopName
  shopSettings.value.address = shopConfig.config.address || ''
  shopSettings.value.phone = shopConfig.config.phone || ''
  shopSettings.value.business_hours = shopConfig.config.business_hours || ''
  shopSettings.value.description = shopConfig.config.description || ''
})

const handleIndustryChange = async (type) => {
  try {
    await shopConfig.switchIndustry(type)
    currentIndustry.value = type
    // 切换行业后重新加载服务项目（重置为新模板的默认服务）
    try {
      await serviceItemsApi.resetServiceItems()
      await loadServiceItems()
    } catch { /* ignore */ }
    ElMessage.success('行业模板已切换，页面术语和服务项目已更新')
  } catch (e) {
    ElMessage.error('切换失败')
  }
}

const activeTab = ref('shop')

const menuItems = [
  { name: 'shop', label: '店铺设置', icon: Shop },
  { name: 'services', label: '服务项目', icon: List },
  { name: 'business', label: '营业设置', icon: Setting },
  { name: 'notification', label: '通知设置', icon: Bell },
  { name: 'permission', label: '权限管理', icon: User },
  { name: 'backup', label: '备份恢复', icon: Download },
]

const shopSettings = ref({
  name: '',
  address: '',
  phone: '',
  business_hours: '',
  description: '',
})

const businessSettings = ref({
  defaultDiscount: 0,
  memberDiscount: 0.1,
  minConsumption: 100,
  pointsRate: 1,
})

const notificationSettings = ref({
  orderNotify: true,
  stockNotify: true,
  lowStockLevel: 10,
  checkinNotify: true,
  dailyReport: true,
})

const permissions = ref([
  { id: 1, name: '新增订单', description: '可以新增订单', enabled: true },
  { id: 2, name: '编辑订单', description: '可以编辑订单', enabled: true },
  { id: 3, name: '删除订单', description: '可以删除订单', enabled: false },
  { id: 4, name: '查看报表', description: '可以查看数据报表', enabled: true },
  { id: 5, name: '管理员工', description: '可以管理员工信息', enabled: false },
])

// ========== 服务项目管理 ==========
const serviceItems = ref([])
const serviceDialogVisible = ref(false)
const editingService = ref(null)
const serviceForm = ref({
  name: '',
  category: '',
  duration: 60,
  price: 0,
  is_active: true,
  description: '',
})

const loadServiceItems = async () => {
  try {
    const res = await serviceItemsApi.getServiceItems()
    serviceItems.value = res?.items || []
  } catch {
    serviceItems.value = []
  }
}

const handleAddService = () => {
  editingService.value = null
  serviceForm.value = {
    name: '',
    category: shopConfig.serviceCategories[0] || '',
    duration: 60,
    price: 0,
    is_active: true,
    description: '',
  }
  serviceDialogVisible.value = true
}

const handleEditService = (row) => {
  editingService.value = row
  serviceForm.value = { ...row }
  serviceDialogVisible.value = true
}

const handleSaveService = async () => {
  if (!serviceForm.value.name) {
    ElMessage.warning('请输入服务名称')
    return
  }
  try {
    if (editingService.value) {
      await serviceItemsApi.updateServiceItem(editingService.value.id, serviceForm.value)
      ElMessage.success('服务项目已更新')
    } else {
      await serviceItemsApi.createServiceItem(serviceForm.value)
      ElMessage.success('服务项目已添加')
    }
    serviceDialogVisible.value = false
    await loadServiceItems()
  } catch {
    ElMessage.error('操作失败')
  }
}

const handleDeleteService = async (id) => {
  try {
    await serviceItemsApi.deleteServiceItem(id)
    ElMessage.success('已删除')
    await loadServiceItems()
  } catch {
    ElMessage.error('删除失败')
  }
}

const handleResetServices = async () => {
  try {
    await serviceItemsApi.resetServiceItems()
    ElMessage.success('已重置为模板默认服务项目')
    await loadServiceItems()
  } catch {
    ElMessage.error('重置失败')
  }
}

const lastBackupTime = ref('2026-01-28 15:30:00')

const handleSaveSettings = () => {
  ElMessage.success('设置已保存')
}

const handleSaveShopSettings = async () => {
  try {
    await shopConfig.saveConfig({
      shop_name: shopSettings.value.name,
      address: shopSettings.value.address,
      phone: shopSettings.value.phone,
      business_hours: shopSettings.value.business_hours,
      description: shopSettings.value.description,
    })
    ElMessage.success('店铺设置已保存')
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

const handleBackup = () => {
  ElMessage.success('备份已启动')
}

const handleRestore = () => {
  ElMessage.info('恢复功能开发中...')
}
</script>

<style scoped lang="scss">
.settings-page {
  .settings-menu {
    background: white;
    border-radius: 4px;
    overflow: hidden;

    .menu-item {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 15px;
      cursor: pointer;
      border-left: 3px solid transparent;
      transition: all 0.3s;

      &:hover {
        background-color: #f5f7fa;
      }

      &.active {
        background-color: #e6f7ff;
        border-left-color: #409eff;
        color: #409eff;
      }

      :deep(.el-icon) {
        font-size: 18px;
      }
    }
  }

  .settings-card {
    margin-bottom: 20px;

    .backup-section {
      padding: 20px;
      background-color: #f5f7fa;
      border-radius: 4px;
    }
  }
}
</style>
