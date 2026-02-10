<template>
  <el-dialog
    :model-value="modelValue"
    :title="isEdit ? '编辑员工' : '新增员工'"
    width="550px"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="100px"
      @submit.prevent="handleSubmit"
    >
      <el-form-item label="员工名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入员工名称" />
      </el-form-item>

      <el-form-item label="员工ID" prop="employee_id">
        <el-input v-model="form.employee_id" placeholder="请输入员工ID" />
      </el-form-item>

      <el-form-item label="手机号" prop="phone">
        <el-input v-model="form.phone" placeholder="请输入手机号" />
      </el-form-item>

      <el-form-item label="岗位" prop="position">
        <el-select v-model="form.position" placeholder="请选择岗位">
          <el-option label="店长" value="店长" />
          <el-option label="调理师" value="调理师" />
          <el-option label="收银员" value="收银员" />
          <el-option label="前台" value="前台" />
          <el-option label="其他" value="其他" />
        </el-select>
      </el-form-item>

      <el-form-item label="身份证号" prop="id_number">
        <el-input v-model="form.id_number" placeholder="请输入身份证号" />
      </el-form-item>

      <el-form-item label="基础薪资" prop="salary">
        <el-input-number v-model="form.salary" :precision="2" :min="0" />
      </el-form-item>

      <el-form-item label="员工等级" prop="level">
        <el-select v-model="form.level" placeholder="请选择员工等级">
          <el-option label="初级" value="初级" />
          <el-option label="中级" value="中级" />
          <el-option label="高级" value="高级" />
          <el-option label="管理" value="管理" />
        </el-select>
      </el-form-item>

      <el-form-item label="入职日期" prop="hire_date">
        <el-date-picker v-model="form.hire_date" type="date" placeholder="请选择入职日期" />
      </el-form-item>

      <el-form-item label="实名认证" prop="real_name_verified">
        <el-switch
          v-model="form.real_name_verified"
          active-text="已认证"
          inactive-text="未认证"
        />
      </el-form-item>

      <el-form-item label="员工状态" prop="status">
        <el-switch
          v-model="form.status"
          active-value="active"
          inactive-value="inactive"
          active-text="在职"
          inactive-text="离职"
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
import * as employeesApi from '@/api/employees'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  employee: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['update:modelValue', 'save'])

const formRef = ref(null)
const loading = ref(false)

const form = ref({
  name: '',
  employee_id: '',
  phone: '',
  position: '',
  id_number: '',
  salary: 0,
  level: '初级',
  hire_date: new Date(),
  real_name_verified: false,
  status: 'active',
})

const rules = {
  name: [{ required: true, message: '请输入员工名称', trigger: 'blur' }],
  employee_id: [{ required: true, message: '请输入员工ID', trigger: 'blur' }],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    {
      pattern: /^1[3-9]\d{9}$/,
      message: '手机号格式不正确',
      trigger: 'blur',
    },
  ],
  position: [{ required: true, message: '请选择岗位', trigger: 'change' }],
}

const isEdit = computed(() => !!props.employee)

watch(
  () => props.employee,
  (newVal) => {
    if (newVal) {
      form.value = { ...newVal }
    } else {
      form.value = {
        name: '',
        employee_id: '',
        phone: '',
        position: '',
        id_number: '',
        salary: 0,
        level: '初级',
        hire_date: new Date(),
        real_name_verified: false,
        status: 'active',
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
      await employeesApi.updateEmployee(props.employee.id, form.value)
      ElMessage.success('编辑成功')
    } else {
      await employeesApi.createEmployee(form.value)
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
