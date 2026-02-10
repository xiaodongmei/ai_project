<template>
  <el-dialog
    :model-value="modelValue"
    :title="title"
    width="400px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <!-- 图标 -->
    <div class="confirm-icon">
      <el-icon :class="iconClass">
        <component :is="icon" />
      </el-icon>
    </div>

    <!-- 内容 -->
    <p class="confirm-content">{{ content }}</p>

    <!-- 详细信息 -->
    <div v-if="details" class="confirm-details">
      <p v-for="(value, key) in details" :key="key">
        <strong>{{ key }}:</strong> {{ value }}
      </p>
    </div>

    <!-- 页脚 -->
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">{{ cancelText }}</el-button>
        <el-button :type="confirmType" @click="handleConfirm" :loading="loading">
          {{ confirmText }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed } from 'vue'
import { ref } from 'vue'
import {
  WarningFilled,
  SuccessFilled,
  InfoFilled,
  CircleCloseFilled,
} from '@element-plus/icons-vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  title: {
    type: String,
    default: '确认操作',
  },
  content: {
    type: String,
    default: '您确定要执行此操作吗？',
  },
  type: {
    type: String,
    enum: ['warning', 'success', 'info', 'error'],
    default: 'warning',
  },
  details: {
    type: Object,
    default: null,
  },
  confirmText: {
    type: String,
    default: '确定',
  },
  cancelText: {
    type: String,
    default: '取消',
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:modelValue', 'confirm'])

const icon = computed(() => {
  const iconMap = {
    warning: WarningFilled,
    success: SuccessFilled,
    info: InfoFilled,
    error: CircleCloseFilled,
  }
  return iconMap[props.type] || InfoFilled
})

const iconClass = computed(() => {
  const classMap = {
    warning: 'warning-icon',
    success: 'success-icon',
    info: 'info-icon',
    error: 'error-icon',
  }
  return classMap[props.type] || 'info-icon'
})

const confirmType = computed(() => {
  const typeMap = {
    warning: 'warning',
    success: 'success',
    info: 'primary',
    error: 'danger',
  }
  return typeMap[props.type] || 'primary'
})

const handleClose = () => {
  emit('update:modelValue', false)
}

const handleConfirm = () => {
  emit('confirm')
}
</script>

<style scoped lang="scss">
.confirm-icon {
  text-align: center;
  margin-bottom: 20px;

  :deep(.el-icon) {
    font-size: 48px;

    &.warning-icon {
      color: #e6a23c;
    }

    &.success-icon {
      color: #67c23a;
    }

    &.info-icon {
      color: #909399;
    }

    &.error-icon {
      color: #f56c6c;
    }
  }
}

.confirm-content {
  font-size: 16px;
  color: #333;
  text-align: center;
  margin: 0 0 20px 0;
}

.confirm-details {
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 20px;
  max-height: 200px;
  overflow-y: auto;

  p {
    margin: 8px 0;
    font-size: 12px;
    color: #606266;

    strong {
      color: #333;
      margin-right: 8px;
    }
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
