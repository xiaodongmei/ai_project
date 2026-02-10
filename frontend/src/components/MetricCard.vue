<template>
  <div class="metric-card" :style="{ borderLeftColor: color }">
    <div class="metric-header">
      <h3 class="metric-title">{{ title }}</h3>
      <el-icon :style="{ color, fontSize: '24px' }">
        <component :is="icon" />
      </el-icon>
    </div>
    <div class="metric-body">
      <p class="metric-value" :style="{ color }">{{ value }}</p>
      <p class="metric-unit">{{ unit }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  value: {
    type: [String, Number],
    required: true,
  },
  unit: {
    type: String,
    default: '',
  },
  color: {
    type: String,
    default: '#409eff',
  },
  icon: {
    type: String,
    default: 'DataAnalysis',
  },
})
</script>

<style scoped lang="scss">
.metric-card {
  background: white;
  border-radius: 6px;
  padding: 20px;
  border-left: 4px solid;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;

  &:hover {
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.15);
    transform: translateY(-2px);
  }
}

.metric-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.metric-title {
  font-size: 14px;
  color: #606266;
  margin: 0;
  font-weight: 500;
}

.metric-body {
  text-align: left;
}

.metric-value {
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 4px 0;
  line-height: 1.2;
}

.metric-unit {
  font-size: 12px;
  color: #909399;
  margin: 0;
}
</style>
