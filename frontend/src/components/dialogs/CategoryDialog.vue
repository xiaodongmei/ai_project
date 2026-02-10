<template>
  <el-dialog
    :model-value="modelValue"
    title="分类管理"
    width="600px"
    @close="handleClose"
  >
    <!-- 分类列表 -->
    <div class="category-list">
      <el-table
        :data="categories"
        stripe
        style="margin-bottom: 20px"
      >
        <el-table-column prop="name" label="分类名称" min-width="150" />
        <el-table-column prop="description" label="描述" min-width="200" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-link type="primary" @click="handleEditCategory(row)">编辑</el-link>
            <el-divider direction="vertical" />
            <el-popconfirm
              title="确定删除此分类吗？"
              @confirm="handleDeleteCategory(row.id)"
            >
              <template #reference>
                <el-link type="danger">删除</el-link>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 新增/编辑表单 -->
    <el-card class="form-card">
      <template #header>
        <span>{{ editingCategory ? '编辑分类' : '新增分类' }}</span>
      </template>
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="分类名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入分类名称" />
        </el-form-item>

        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            placeholder="请输入分类描述"
            :rows="3"
          />
        </el-form-item>

        <el-form-item label="显示顺序" prop="order">
          <el-input-number v-model="form.order" :min="0" />
        </el-form-item>

        <div class="form-actions">
          <el-button @click="handleReset">重置</el-button>
          <el-button type="primary" @click="handleSaveCategory" :loading="loading">
            {{ editingCategory ? '更新' : '新增' }}
          </el-button>
        </div>
      </el-form>
    </el-card>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">关闭</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import * as productsApi from '@/api/products'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
})

const emit = defineEmits(['update:modelValue', 'save'])

const formRef = ref(null)
const loading = ref(false)
const categories = ref([])
const editingCategory = ref(null)

const form = ref({
  name: '',
  description: '',
  order: 0,
})

const rules = {
  name: [{ required: true, message: '请输入分类名称', trigger: 'blur' }],
}

const loadCategories = async () => {
  try {
    const response = await productsApi.getCategories()
    categories.value = response || []
  } catch (error) {
    ElMessage.error('加载分类失败')
  }
}

const handleEditCategory = (row) => {
  editingCategory.value = row
  form.value = { ...row }
}

const handleDeleteCategory = async (categoryId) => {
  try {
    await productsApi.deleteCategory(categoryId)
    ElMessage.success('删除成功')
    await loadCategories()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

const handleSaveCategory = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    loading.value = true

    if (editingCategory.value) {
      await productsApi.updateCategory(editingCategory.value.id, form.value)
      ElMessage.success('更新成功')
    } else {
      await productsApi.createCategory(form.value)
      ElMessage.success('新增成功')
    }

    await loadCategories()
    handleReset()
  } catch (error) {
    ElMessage.error(error.message || '操作失败')
  } finally {
    loading.value = false
  }
}

const handleReset = () => {
  editingCategory.value = null
  form.value = {
    name: '',
    description: '',
    order: 0,
  }
  formRef.value?.clearValidate()
}

const handleClose = () => {
  handleReset()
  emit('update:modelValue', false)
}

watch(
  () => props.modelValue,
  (newVal) => {
    if (newVal) {
      loadCategories()
    }
  }
)

onMounted(() => {
  loadCategories()
})
</script>

<style scoped lang="scss">
.category-list {
  margin-bottom: 20px;
}

.form-card {
  :deep(.el-card__header) {
    background-color: #f5f7fa;
    border-bottom: 1px solid #ebeef5;
  }

  .form-actions {
    display: flex;
    gap: 10px;
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
