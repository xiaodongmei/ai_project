<template>
  <el-dialog
    :model-value="modelValue"
    :title="isEdit ? '编辑订单' : '新增订单'"
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
      <el-form-item label="顾客名称" prop="customer_name">
        <el-input v-model="form.customer_name" placeholder="请输入或选择顾客" />
      </el-form-item>

      <el-form-item :label="shopConfig.providerLabel" prop="employee_name">
        <el-select v-model="form.employee_name" :placeholder="`请选择${shopConfig.providerLabel}`" filterable>
          <el-option
            v-for="emp in employeeList"
            :key="emp.id"
            :label="`${emp.name} (${emp.position})`"
            :value="emp.name"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="服务项目" prop="service_items">
        <el-select v-model="form.service_items" multiple placeholder="请选择服务项目" filterable>
          <el-option
            v-for="svc in serviceItemList"
            :key="svc.id || svc.name"
            :label="svc.price ? `${svc.name} (¥${svc.price} / ${svc.duration}分钟)` : svc.name"
            :value="svc.name"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="金额" prop="amount">
        <el-input-number v-model="form.amount" :precision="2" :min="0" />
      </el-form-item>

      <el-form-item label="折扣" prop="discount">
        <el-input-number v-model="form.discount" :precision="2" :min="0" />
      </el-form-item>

      <el-form-item label="订单状态" prop="status">
        <el-select v-model="form.status" placeholder="请选择订单状态">
          <el-option label="待结算" value="pending" />
          <el-option label="已完成" value="completed" />
          <el-option label="已取消" value="cancelled" />
        </el-select>
      </el-form-item>

      <el-form-item label="支付方式" prop="payment_method">
        <el-select v-model="form.payment_method" placeholder="请选择支付方式">
          <el-option label="微信支付" value="wechat" />
          <el-option label="支付宝" value="alipay" />
          <el-option label="现金" value="cash" />
          <el-option label="刷卡" value="card" />
        </el-select>
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
import { ref, computed, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import * as ordersApi from '@/api/orders'
import * as employeesApi from '@/api/employees'
import * as serviceItemsApi from '@/api/serviceItems'
import { useShopConfigStore } from '@/store/shopConfig'

const shopConfig = useShopConfigStore()

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  order: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['update:modelValue', 'save'])

const formRef = ref(null)
const loading = ref(false)
const employeeList = ref([])
const serviceItemList = ref([])

const form = ref({
  customer_name: '',
  employee_name: '',
  service_items: [],
  amount: 0,
  discount: 0,
  status: 'pending',
  payment_method: 'cash',
  remark: '',
})

const rules = {
  customer_name: [{ required: true, message: '请输入顾客名称', trigger: 'blur' }],
  employee_name: [{ required: true, message: `请选择服务人员`, trigger: 'change' }],
  service_items: [{ required: true, message: '请选择服务项目', trigger: 'change' }],
  amount: [{ required: true, message: '请输入金额', trigger: 'change' }],
}

const isEdit = computed(() => !!props.order)

// 加载员工列表
const loadEmployees = async () => {
  try {
    const res = await employeesApi.getEmployees({ limit: 50 })
    employeeList.value = res?.items || []
  } catch {
    // fallback: 使用空列表
    employeeList.value = []
  }
}

// 加载服务项目列表
const loadServiceItems = async () => {
  try {
    const res = await serviceItemsApi.getServiceItems()
    serviceItemList.value = res?.items || []
  } catch {
    // fallback: 使用shopConfig中的服务分类
    serviceItemList.value = shopConfig.serviceCategories.map((name, i) => ({
      id: i + 1,
      name,
      price: 0,
      duration: 60,
    }))
  }
}

// 选择服务项目后自动计算金额
watch(() => form.value.service_items, (newItems) => {
  if (!isEdit.value && newItems && newItems.length > 0) {
    let total = 0
    for (const itemName of newItems) {
      const svc = serviceItemList.value.find(s => s.name === itemName)
      if (svc && svc.price) {
        total += svc.price
      }
    }
    if (total > 0) {
      form.value.amount = total
    }
  }
})

watch(
  () => props.modelValue,
  (visible) => {
    if (visible) {
      loadEmployees()
      loadServiceItems()
    }
  }
)

watch(
  () => props.order,
  (newVal) => {
    if (newVal) {
      form.value = { ...newVal }
    } else {
      form.value = {
        customer_name: '',
        employee_name: '',
        service_items: [],
        amount: 0,
        discount: 0,
        status: 'pending',
        payment_method: 'cash',
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
      await ordersApi.updateOrder(props.order.id, form.value)
      ElMessage.success('编辑成功')
    } else {
      await ordersApi.createOrder(form.value)
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
