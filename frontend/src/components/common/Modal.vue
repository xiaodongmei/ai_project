<template>
  <el-dialog
    :model-value="modelValue"
    :title="title"
    :width="width"
    :close-on-click-modal="closeOnClickModal"
    :show-close="showClose"
    @close="handleClose"
  >
    <!-- 标签页 -->
    <el-tabs v-if="tabs && tabs.length > 0" v-model="activeTab">
      <el-tab-pane
        v-for="tab in tabs"
        :key="tab.name"
        :label="tab.label"
        :name="tab.name"
      >
        <slot :name="`tab-${tab.name}`" />
      </el-tab-pane>
    </el-tabs>

    <!-- 默认插槽 -->
    <slot v-else />

    <!-- 页脚 -->
    <template #footer>
      <div class="dialog-footer">
        <el-button
          v-for="btn in footerButtons"
          :key="btn.name"
          :type="btn.type || 'default'"
          :loading="btn.loading"
          @click="handleButtonClick(btn)"
        >
          {{ btn.label }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  title: {
    type: String,
    default: '对话框',
  },
  width: {
    type: String,
    default: '500px',
  },
  tabs: {
    type: Array,
    default: () => [],
  },
  footerButtons: {
    type: Array,
    default: () => [
      { name: 'cancel', label: '取消', type: 'default' },
      { name: 'confirm', label: '确定', type: 'primary' },
    ],
  },
  closeOnClickModal: {
    type: Boolean,
    default: false,
  },
  showClose: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits(['update:modelValue', 'button-click'])

const activeTab = ref(props.tabs.length > 0 ? props.tabs[0].name : '')

const handleClose = () => {
  emit('update:modelValue', false)
}

const handleButtonClick = (btn) => {
  if (btn.name === 'cancel') {
    handleClose()
  } else {
    emit('button-click', btn.name)
  }
}
</script>

<style scoped lang="scss">
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
