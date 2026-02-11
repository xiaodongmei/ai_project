<template>
  <div class="header-bar">
    <!-- 左侧面包屑 -->
    <div class="header-left">
      <nav class="breadcrumb">
        <span class="breadcrumb-item breadcrumb-item--muted">首页</span>
        <template v-for="(item, index) in breadcrumbs" :key="item.path">
          <svg class="breadcrumb-sep" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6" />
          </svg>
          <span :class="['breadcrumb-item', { 'breadcrumb-item--active': index === breadcrumbs.length - 1 }]">
            {{ item.name }}
          </span>
        </template>
      </nav>
    </div>

    <!-- 右侧操作 -->
    <div class="header-right">
      <!-- 搜索框 -->
      <div class="search-box">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
        <input
          v-model="searchText"
          type="text"
          placeholder="搜索..."
          class="search-input"
          @keyup.enter="handleSearch"
        />
      </div>

      <!-- 用户头像下拉菜单 -->
      <el-dropdown @command="handleCommand">
        <div class="user-avatar">
          <el-avatar :size="32" :src="userStore.user?.avatar">
            {{ userStore.user?.username?.[0]?.toUpperCase() || 'U' }}
          </el-avatar>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item disabled>
              <div style="padding: 4px 0">
                <div style="font-weight: 600; color: #111827">{{ userStore.user?.username || '未登录' }}</div>
                <div style="font-size: 12px; color: #9ca3af; margin-top: 2px">{{ userStore.user?.role || '管理员' }}</div>
              </div>
            </el-dropdown-item>
            <el-dropdown-item divided command="profile">
              <el-icon><User /></el-icon>
              个人中心
            </el-dropdown-item>
            <el-dropdown-item command="settings">
              <el-icon><Setting /></el-icon>
              系统设置
            </el-dropdown-item>
            <el-dropdown-item divided command="logout">
              <el-icon><SwitchButton /></el-icon>
              退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { useShopConfigStore } from '@/store/shopConfig'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, Setting, SwitchButton } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const shopConfig = useShopConfigStore()

const route = useRoute()
const searchText = ref('')

const breadcrumbs = computed(() => {
  const currentName = shopConfig.breadcrumbLabels[route.path] || route.meta?.title || '页面'
  return [{ name: currentName, path: route.path }]
})

const handleSearch = () => {
  if (searchText.value) {
    console.log('搜索:', searchText.value)
  }
}

const handleCommand = async (command) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'settings':
      router.push('/settings')
      break
    case 'logout':
      try {
        await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        })
        userStore.logout()
        ElMessage.success('已退出登录')
        router.push('/login')
      } catch {
        // 用户取消操作
      }
      break
  }
}
</script>

<style scoped lang="scss">
.header-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 100%;
}

.header-left {
  flex: 1;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 4px;
}

.breadcrumb-item {
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.2s;

  &--muted {
    color: #9ca3af;

    &:hover {
      color: #6b7280;
    }
  }

  &--active {
    color: #111827;
    cursor: default;
  }
}

.breadcrumb-sep {
  width: 16px;
  height: 16px;
  color: #d1d5db;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;

  .search-icon {
    position: absolute;
    left: 10px;
    width: 16px;
    height: 16px;
    color: #9ca3af;
    pointer-events: none;
  }

  .search-input {
    width: 220px;
    height: 36px;
    padding: 0 12px 0 34px;
    border: none;
    border-radius: 8px;
    background: #f3f4f6;
    font-size: 14px;
    color: #374151;
    outline: none;
    transition: all 0.2s;

    &::placeholder {
      color: #9ca3af;
    }

    &:focus {
      background: white;
      box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15);
    }
  }
}

.user-avatar {
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 2px;
  border-radius: 8px;
  transition: background 0.2s;

  &:hover {
    background: #f3f4f6;
  }
}

@media (max-width: 768px) {
  .search-box {
    display: none;
  }
}
</style>
