<template>
  <div class="search-form-wrapper">
    <div class="search-form">
      <el-form :model="form" :inline="true" label-width="auto">
        <!-- 动态搜索字段 -->
        <el-form-item v-for="field in fields" :key="field.prop" :label="field.label">
          <!-- 输入框 -->
          <el-input
            v-if="field.type === 'input'"
            v-model="form[field.prop]"
            :placeholder="field.placeholder"
            clearable
          />

          <!-- 选择框 -->
          <el-select
            v-else-if="field.type === 'select'"
            v-model="form[field.prop]"
            :placeholder="field.placeholder"
            clearable
          >
            <el-option
              v-for="opt in field.options"
              :key="opt.value"
              :label="opt.label"
              :value="opt.value"
            />
          </el-select>

          <!-- 日期范围 -->
          <el-date-picker
            v-else-if="field.type === 'daterange'"
            v-model="form[field.prop]"
            type="daterange"
            :range-separator="field.rangeSeparator || '至'"
            :start-placeholder="field.startPlaceholder || '开始日期'"
            :end-placeholder="field.endPlaceholder || '结束日期'"
          />

          <!-- 日期 -->
          <el-date-picker
            v-else-if="field.type === 'date'"
            v-model="form[field.prop]"
            type="date"
            :placeholder="field.placeholder"
          />
        </el-form-item>
      </el-form>

      <!-- 按钮 -->
      <div class="form-actions">
        <el-button type="primary" @click="handleSearch">查询</el-button>
        <el-button @click="handleReset">重置</el-button>
        <el-button v-if="showAdvanced" link @click="showAdvancedOptions = !showAdvancedOptions">
          {{ showAdvancedOptions ? '隐藏' : '显示' }}高级选项
        </el-button>
      </div>
    </div>

    <!-- 快速筛选 -->
    <div v-if="quickFilters && quickFilters.length > 0" class="quick-filters">
      <el-button
        v-for="filter in quickFilters"
        :key="filter.name"
        :type="isFilterActive(filter) ? 'primary' : 'default'"
        @click="applyQuickFilter(filter)"
      >
        {{ filter.label }}
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, reactive } from 'vue'

const props = defineProps({
  fields: {
    type: Array,
    required: true,
  },
  quickFilters: {
    type: Array,
    default: () => [],
  },
  showAdvanced: {
    type: Boolean,
    default: false,
  },
  initialForm: {
    type: Object,
    default: () => ({}),
  },
})

const emit = defineEmits(['search', 'reset'])

const showAdvancedOptions = ref(false)
const form = reactive(props.initialForm)

const handleSearch = () => {
  emit('search', { ...form })
}

const handleReset = () => {
  Object.keys(form).forEach((key) => {
    form[key] = props.initialForm[key] || ''
  })
  emit('reset')
}

const isFilterActive = (filter) => {
  if (!filter.conditions) return false
  return Object.keys(filter.conditions).every((key) => {
    return form[key] === filter.conditions[key]
  })
}

const applyQuickFilter = (filter) => {
  if (filter.conditions) {
    Object.assign(form, filter.conditions)
    handleSearch()
  }
}

watch(
  () => props.initialForm,
  (newVal) => {
    Object.assign(form, newVal)
  }
)
</script>

<style scoped lang="scss">
.search-form-wrapper {
  margin-bottom: 20px;
}

.search-form {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
  margin-bottom: 15px;

  :deep(.el-form) {
    flex: 1;

    .el-form-item {
      margin-bottom: 12px;
    }
  }

  .form-actions {
    display: flex;
    gap: 10px;
    white-space: nowrap;
  }
}

.quick-filters {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 15px;

  :deep(.el-button) {
    font-size: 12px;
  }
}
</style>
