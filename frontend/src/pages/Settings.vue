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

              <el-button type="primary" @click="handleSaveSettings">保存设置</el-button>
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
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Shop,
  Setting,
  Bell,
  User,
  Download,
} from '@element-plus/icons-vue'

const activeTab = ref('shop')

const menuItems = [
  { name: 'shop', label: '店铺设置', icon: Shop },
  { name: 'business', label: '营业设置', icon: Setting },
  { name: 'notification', label: '通知设置', icon: Bell },
  { name: 'permission', label: '权限管理', icon: User },
  { name: 'backup', label: '备份恢复', icon: Download },
]

const shopSettings = ref({
  name: '养生店',
  address: '北京市朝阳区',
  phone: '010-12345678',
  business_hours: '09:00-21:00',
  description: '专业养生健身馆',
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

const lastBackupTime = ref('2026-01-28 15:30:00')

const handleSaveSettings = () => {
  ElMessage.success('设置已保存')
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
