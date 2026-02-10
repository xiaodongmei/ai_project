<template>
  <el-dialog
    :model-value="modelValue"
    title="订单支付"
    width="450px"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="100px"
      @submit.prevent="handleSubmit"
    >
      <el-form-item label="支付方式" prop="payment_method">
        <el-select v-model="form.payment_method" placeholder="请选择支付方式">
          <el-option label="微信支付" value="wechat" />
          <el-option label="支付宝" value="alipay" />
          <el-option label="现金" value="cash" />
          <el-option label="刷卡" value="card" />
        </el-select>
      </el-form-item>

      <el-form-item label="支付金额" prop="amount">
        <el-input-number
          v-model="form.amount"
          :precision="2"
          :min="0"
          placeholder="请输入支付金额"
        />
      </el-form-item>

      <el-form-item label="交易号" prop="transaction_id">
        <el-input
          v-model="form.transaction_id"
          placeholder="请输入交易号（可选）"
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

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="loading">确认支付</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import * as ordersApi from '@/api/orders'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  orderId: {
    type: [String, Number],
    default: null,
  },
})

const emit = defineEmits(['update:modelValue', 'save'])

const formRef = ref(null)
const loading = ref(false)

const form = ref({
  payment_method: 'cash',
  amount: 0,
  transaction_id: '',
  remark: '',
})

const rules = {
  payment_method: [{ required: true, message: '请选择支付方式', trigger: 'change' }],
  amount: [{ required: true, message: '请输入支付金额', trigger: 'change' }],
}

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    loading.value = true

    await ordersApi.addOrderPayment(props.orderId, form.value)
    ElMessage.success('支付成功')

    emit('save')
    handleClose()
  } catch (error) {
    ElMessage.error(error.message || '支付失败')
  } finally {
    loading.value = false
  }
}

const handleClose = () => {
  emit('update:modelValue', false)
}

watch(
  () => props.modelValue,
  (newVal) => {
    if (!newVal) {
      form.value = {
        payment_method: 'cash',
        amount: 0,
        transaction_id: '',
        remark: '',
      }
    }
  }
)
</script>

<style scoped lang="scss">
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
