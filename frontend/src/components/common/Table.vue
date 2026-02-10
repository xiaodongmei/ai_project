<template>
  <el-card class="table-card">
    <el-table
      :data="data"
      :stripe="stripe"
      :loading="loading"
      :height="height"
      v-bind="$attrs"
      @selection-change="handleSelectionChange"
    >
      <!-- 复选框列 -->
      <el-table-column
        v-if="showSelection"
        type="selection"
        :width="selectionWidth"
        :selectable="selectable"
      />

      <!-- 序号列 -->
      <el-table-column v-if="showIndex" label="序号" type="index" :width="indexWidth" />

      <!-- 动态列 -->
      <el-table-column
        v-for="col in columns"
        :key="col.prop"
        :prop="col.prop"
        :label="col.label"
        :width="col.width"
        :min-width="col.minWidth"
        :align="col.align || 'left'"
        :formatter="col.formatter"
      >
        <template v-if="col.render" #default="{ row }">
          <component :is="col.render" :row="row" />
        </template>
      </el-table-column>

      <!-- 操作列 -->
      <el-table-column
        v-if="actions && actions.length > 0"
        label="操作"
        :width="actionWidth"
        :fixed="actionFixed"
        align="center"
      >
        <template #default="{ row }">
          <div class="action-buttons">
            <el-link
              v-for="action in actions"
              :key="action.name"
              :type="action.type || 'primary'"
              @click="handleAction(action, row)"
            >
              {{ action.label }}
            </el-link>
          </div>
        </template>
      </el-table-column>

      <!-- 空状态 -->
      <template #empty>
        <el-empty description="暂无数据" />
      </template>
    </el-table>

    <!-- 分页 -->
    <div v-if="pagination" class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="pageSizes"
        :layout="paginationLayout"
        :total="total"
        @current-page-change="$emit('page-change', currentPage)"
        @page-size-change="$emit('page-size-change', pageSize)"
      />
    </div>
  </el-card>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    required: true,
  },
  columns: {
    type: Array,
    required: true,
  },
  actions: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
  height: {
    type: [String, Number],
    default: 'auto',
  },
  stripe: {
    type: Boolean,
    default: true,
  },
  showSelection: {
    type: Boolean,
    default: false,
  },
  selectionWidth: {
    type: Number,
    default: 50,
  },
  showIndex: {
    type: Boolean,
    default: false,
  },
  indexWidth: {
    type: Number,
    default: 50,
  },
  actionWidth: {
    type: Number,
    default: 200,
  },
  actionFixed: {
    type: String,
    default: 'right',
  },
  pagination: {
    type: Boolean,
    default: true,
  },
  pageSizes: {
    type: Array,
    default: () => [10, 20, 50, 100],
  },
  paginationLayout: {
    type: String,
    default: 'total, sizes, prev, pager, next, jumper',
  },
  total: {
    type: Number,
    default: 0,
  },
  selectable: {
    type: Function,
    default: null,
  },
})

const emit = defineEmits(['selection-change', 'action', 'page-change', 'page-size-change'])

const currentPage = ref(1)
const pageSize = ref(10)

const handleSelectionChange = (selection) => {
  emit('selection-change', selection)
}

const handleAction = (action, row) => {
  emit('action', { action: action.name, row })
}
</script>

<style scoped lang="scss">
.table-card {
  .action-buttons {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;

    :deep(.el-link) {
      font-size: 12px;

      &:not(:last-child)::after {
        content: '|';
        margin: 0 8px;
        color: #dcdfe6;
      }
    }
  }

  .pagination {
    display: flex;
    justify-content: flex-end;
    margin-top: 20px;
  }
}
</style>
