<template>
  <el-dialog
    :model-value="modelValue"
    :title="isEdit ? '编辑产品' : '新增产品'"
    width="600px"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="100px"
      @submit.prevent="handleSubmit"
    >
      <el-form-item label="产品名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入产品名称" />
      </el-form-item>

      <el-form-item label="产品分类" prop="category_id">
        <el-select v-model="form.category_id" placeholder="请选择分类">
          <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
        </el-select>
      </el-form-item>

      <el-form-item label="产品描述" prop="description">
        <el-input
          v-model="form.description"
          type="textarea"
          placeholder="请输入产品描述"
          :rows="3"
        />
      </el-form-item>

      <el-form-item label="会员价" prop="member_price">
        <el-input-number v-model="form.member_price" :precision="2" :min="0" />
      </el-form-item>

      <el-form-item label="非会员价" prop="non_member_price">
        <el-input-number v-model="form.non_member_price" :precision="2" :min="0" />
      </el-form-item>

      <el-form-item label="成本价" prop="cost_price">
        <el-input-number v-model="form.cost_price" :precision="2" :min="0" />
      </el-form-item>

      <el-form-item label="库存" prop="stock">
        <el-input-number v-model="form.stock" :min="0" />
      </el-form-item>

      <el-form-item label="规格" prop="spec">
        <el-input v-model="form.spec" placeholder="如：50ml、100克等" />
      </el-form-item>

      <el-form-item label="单位" prop="unit">
        <el-input v-model="form.unit" placeholder="如：瓶、盒、个等" />
      </el-form-item>

      <el-form-item label="产品状态" prop="is_active">
        <el-switch
          v-model="form.is_active"
          active-text="启用"
          inactive-text="禁用"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="loading">保存</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import * as productsApi from '@/api/products'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  product: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['update:modelValue', 'save'])

const formRef = ref(null)
const loading = ref(false)
const categories = ref([])

const form = ref({
  name: '',
  category_id: '',
  description: '',
  member_price: 0,
  non_member_price: 0,
  cost_price: 0,
  stock: 0,
  spec: '',
  unit: '',
  is_active: true,
})

const rules = {
  name: [{ required: true, message: '请输入产品名称', trigger: 'blur' }],
  category_id: [{ required: true, message: '请选择分类', trigger: 'change' }],
  member_price: [{ required: true, message: '请输入会员价', trigger: 'change' }],
}

const isEdit = computed(() => !!props.product)

const loadCategories = async () => {
  try {
    const response = await productsApi.getCategories()
    categories.value = response || []
  } catch (error) {
    ElMessage.error('加载分类失败')
  }
}

watch(
  () => props.product,
  (newVal) => {
    if (newVal) {
      form.value = { ...newVal }
    } else {
      form.value = {
        name: '',
        category_id: '',
        description: '',
        member_price: 0,
        non_member_price: 0,
        cost_price: 0,
        stock: 0,
        spec: '',
        unit: '',
        is_active: true,
      }
    }
  }
)

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    loading.value = true

    if (isEdit.value) {
      await productsApi.updateProduct(props.product.id, form.value)
      ElMessage.success('编辑成功')
    } else {
      await productsApi.createProduct(form.value)
      ElMessage.success('新增成功')
    }

    emit('save')
    handleClose()
  } catch (error) {
    ElMessage.error(error.message || '操作失败')
  } finally {
    loading.value = false
  }
}

const handleClose = () => {
  emit('update:modelValue', false)
}

onMounted(() => {
  loadCategories()
})
</script>

<style scoped lang="scss">
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
