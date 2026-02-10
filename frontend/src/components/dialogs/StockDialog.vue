<template>
  <el-dialog
    :model-value="modelValue"
    title="库存调整"
    width="450px"
    @close="handleClose"
  >
    <div v-if="product" class="stock-dialog">
      <!-- 产品信息 -->
      <div class="product-info">
        <p><strong>产品名称:</strong> {{ product.name }}</p>
        <p><strong>当前库存:</strong> <span class="stock-value">{{ product.stock }}</span></p>
      </div>

      <!-- 调整表单 -->
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
        @submit.prevent="handleSubmit"
      >
        <el-form-item label="调整类型" prop="adjust_type">
          <el-select v-model="form.adjust_type" placeholder="请选择调整类型">
            <el-option label="入库" value="in" />
            <el-option label="出库" value="out" />
            <el-option label="盘点" value="inventory" />
          </el-select>
        </el-form-item>

        <el-form-item label="调整数量" prop="quantity">
          <el-input-number v-model="form.quantity" :min="0" />
        </el-form-item>

        <el-form-item label="调整原因" prop="reason">
          <el-input
            v-model="form.reason"
            type="textarea"
            placeholder="请输入调整原因"
            :rows="3"
          />
        </el-form-item>

        <el-form-item label="备注" prop="remark">
          <el-input
            v-model="form.remark"
            type="textarea"
            placeholder="请输入备注信息"
            :rows="2"
          />
        </el-form-item>
      </el-form>

      <!-- 预览 -->
      <div class="preview">
        <p>调整后库存: <strong>{{ calculateNewStock() }}</strong></p>
      </div>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="loading">确认调整</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
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

const form = ref({
  adjust_type: 'in',
  quantity: 0,
  reason: '',
  remark: '',
})

const rules = {
  adjust_type: [{ required: true, message: '请选择调整类型', trigger: 'change' }],
  quantity: [{ required: true, message: '请输入调整数量', trigger: 'change' }],
  reason: [{ required: true, message: '请输入调整原因', trigger: 'blur' }],
}

const calculateNewStock = () => {
  if (!props.product) return 0
  const current = props.product.stock || 0
  if (form.value.adjust_type === 'in') {
    return current + form.value.quantity
  } else if (form.value.adjust_type === 'out') {
    return Math.max(0, current - form.value.quantity)
  }
  return form.value.quantity
}

watch(
  () => props.modelValue,
  (newVal) => {
    if (!newVal) {
      form.value = {
        adjust_type: 'in',
        quantity: 0,
        reason: '',
        remark: '',
      }
    }
  }
)

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    loading.value = true

    const newStock = calculateNewStock()
    await productsApi.updateStock(props.product.id, newStock)

    ElMessage.success('库存调整成功')
    emit('save')
    handleClose()
  } catch (error) {
    ElMessage.error(error.message || '调整失败')
  } finally {
    loading.value = false
  }
}

const handleClose = () => {
  emit('update:modelValue', false)
}
</script>

<style scoped lang="scss">
.stock-dialog {
  .product-info {
    padding: 15px;
    background-color: #f5f7fa;
    border-radius: 4px;
    margin-bottom: 20px;

    p {
      margin: 8px 0;
      font-size: 14px;

      .stock-value {
        color: #f56c6c;
        font-weight: 600;
        font-size: 16px;
      }
    }
  }

  .preview {
    padding: 15px;
    background-color: #f0f9ff;
    border-left: 3px solid #409eff;
    margin-top: 20px;

    p {
      margin: 0;
      color: #333;
    }
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
