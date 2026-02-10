<template>
  <div class="main-layout">
    <!-- 固定侧边栏 -->
    <Sidebar />

    <!-- 主内容区域 -->
    <div class="main-wrapper">
      <!-- 顶部导航栏 -->
      <header class="header-wrapper">
        <HeaderBar />
      </header>

      <!-- 主要内容 -->
      <main class="main-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import Sidebar from '@/components/Sidebar.vue'
import HeaderBar from '@/components/HeaderBar.vue'
</script>

<style scoped lang="scss">
.main-layout {
  min-height: 100vh;
  background: #f5f7fa;
  padding-left: 106px;
}

.main-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header-wrapper {
  position: sticky;
  top: 0;
  z-index: 30;
  height: 56px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid #e5e7eb;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: transparent;
  }

  &::-webkit-scrollbar-thumb {
    background: #d1d5db;
    border-radius: 3px;

    &:hover {
      background: #9ca3af;
    }
  }
}

@media (max-width: 768px) {
  .main-layout {
    padding-left: 0;
  }
}
</style>
