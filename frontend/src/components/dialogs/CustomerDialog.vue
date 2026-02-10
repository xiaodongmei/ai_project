<template>
  <el-dialog
    :model-value="modelValue"
    :title="isEdit ? '编辑顾客' : '新增顾客'"
    width="500px"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="100px"
      @submit.prevent="handleSubmit"
    >
      <el-form-item label="姓名" prop="name">
        <el-input v-model="form.name" placeholder="请输入顾客姓名" />
      </el-form-item>

      <el-form-item label="手机号" prop="phone">
        <el-input v-model="form.phone" placeholder="请输入手机号" />
      </el-form-item>

      <el-form-item label="微信ID" prop="wechat_id">
        <el-input v-model="form.wechat_id" placeholder="请输入微信ID" />
      </el-form-item>

      <el-form-item label="客户类型" prop="customer_type">
        <el-select v-model="form.customer_type" placeholder="请选择客户类型">
          <el-option label="会员" value="member" />
          <el-option label="非会员" value="non-member" />
        </el-select>
      </el-form-item>

      <el-form-item label="状态" prop="status">
        <el-switch
          v-model="form.status"
          active-value="active"
          inactive-value="inactive"
          active-text="启用"
          inactive-text="禁用"
        />
      </el-form-item>

      <el-form-item label="备注" prop="remark">
        <el-input
          v-model="form.remark"
          type="textarea"
          placeholder="请输入备注信息"
          :rows="3"
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
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import * as customersApi from '@/api/customers'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  customer: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['update:modelValue', 'save'])

const formRef = ref(null)
const loading = ref(false)

const form = ref({
  name: '',
  phone: '',
  wechat_id: '',
  customer_type: 'non-member',
  status: 'active',
  remark: '',
})

const rules = {
  name: [{ required: true, message: '请输入顾客姓名', trigger: 'blur' }],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    {
      pattern: /^1[3-9]\d{9}$/,
      message: '手机号格式不正确',
      trigger: 'blur',
    },
  ],
}

const isEdit = computed(() => !!props.customer)

watch(
  () => props.customer,
  (newVal) => {
    if (newVal) {
      form.value = { ...newVal }
    } else {
      form.value = {
        name: '',
        phone: '',
        wechat_id: '',
        customer_type: 'non-member',
        status: 'active',
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

    if (isEdit.value) {
      await customersApi.updateCustomer(props.customer.id, form.value)
      ElMessage.success('编辑成功')
    } else {
      await customersApi.createCustomer(form.value)
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
</script>

<style scoped lang="scss">
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
