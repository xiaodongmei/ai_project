<template>
  
    <div class="profile-page">
      <el-row :gutter="20">
        <!-- 左侧个人信息 -->
        <el-col :xs="24" :sm="24" :md="8">
          <el-card class="profile-card">
            <template #header>
              <span>个人信息</span>
            </template>
            <div class="profile-avatar">
              <el-avatar :src="userInfo.avatar" :size="100" />
              <el-button type="primary" size="small" @click="handleChangeAvatar">
                更换头像
              </el-button>
            </div>
            <el-descriptions :column="1" border>
              <el-descriptions-item label="账号">{{ userInfo.username }}</el-descriptions-item>
              <el-descriptions-item label="姓名">{{ userInfo.name }}</el-descriptions-item>
              <el-descriptions-item label="邮箱">{{ userInfo.email }}</el-descriptions-item>
              <el-descriptions-item label="电话">{{ userInfo.phone }}</el-descriptions-item>
              <el-descriptions-item label="角色">
                <el-tag>{{ userInfo.role }}</el-tag>
              </el-descriptions-item>
            </el-descriptions>
          </el-card>
        </el-col>

        <!-- 右侧编辑表单 -->
        <el-col :xs="24" :sm="24" :md="16">
          <el-card class="edit-card">
            <template #header>
              <span>编辑信息</span>
            </template>
            <el-form
              ref="formRef"
              :model="form"
              :rules="rules"
              label-width="100px"
            >
              <el-form-item label="姓名" prop="name">
                <el-input v-model="form.name" />
              </el-form-item>

              <el-form-item label="邮箱" prop="email">
                <el-input v-model="form.email" type="email" />
              </el-form-item>

              <el-form-item label="电话" prop="phone">
                <el-input v-model="form.phone" />
              </el-form-item>

              <el-form-item label="部门" prop="department">
                <el-input v-model="form.department" />
              </el-form-item>

              <el-form-item label="位置" prop="location">
                <el-input v-model="form.location" />
              </el-form-item>

              <el-form-item label="个人签名" prop="signature">
                <el-input
                  v-model="form.signature"
                  type="textarea"
                  :rows="3"
                  placeholder="请输入个人签名"
                />
              </el-form-item>

              <div class="form-actions">
                <el-button @click="handleReset">重置</el-button>
                <el-button type="primary" @click="handleSave" :loading="loading">
                  保存修改
                </el-button>
              </div>
            </el-form>
          </el-card>

          <!-- 修改密码 -->
          <el-card class="edit-card">
            <template #header>
              <span>修改密码</span>
            </template>
            <el-form
              ref="passwordFormRef"
              :model="passwordForm"
              :rules="passwordRules"
              label-width="100px"
            >
              <el-form-item label="当前密码" prop="oldPassword">
                <el-input
                  v-model="passwordForm.oldPassword"
                  type="password"
                  show-password
                />
              </el-form-item>

              <el-form-item label="新密码" prop="newPassword">
                <el-input
                  v-model="passwordForm.newPassword"
                  type="password"
                  show-password
                />
              </el-form-item>

              <el-form-item label="确认密码" prop="confirmPassword">
                <el-input
                  v-model="passwordForm.confirmPassword"
                  type="password"
                  show-password
                />
              </el-form-item>

              <div class="form-actions">
                <el-button @click="handleResetPassword">重置</el-button>
                <el-button type="primary" @click="handleChangePassword" :loading="passwordLoading">
                  修改密码
                </el-button>
              </div>
            </el-form>
          </el-card>
        </el-col>
      </el-row>
    </div>
  
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import * as authApi from '@/api/auth'

const formRef = ref(null)
const passwordFormRef = ref(null)
const loading = ref(false)
const passwordLoading = ref(false)

const userInfo = ref({
  username: 'admin',
  name: '管理员',
  email: 'admin@example.com',
  phone: '13800138000',
  role: '管理员',
  avatar: 'https://via.placeholder.com/100',
})

const form = ref({
  name: '',
  email: '',
  phone: '',
  department: '',
  location: '',
  signature: '',
})

const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: '',
})

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    {
      pattern: /^[\w\.-]+@[\w\.-]+\.\w+$/,
      message: '邮箱格式不正确',
      trigger: 'blur',
    },
  ],
}

const passwordRules = {
  oldPassword: [{ required: true, message: '请输入当前密码', trigger: 'blur' }],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6个字符', trigger: 'blur' },
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.value.newPassword) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur',
    },
  ],
}

const handleSave = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    loading.value = true
    await authApi.updateUser(userInfo.value.id, form.value)
    ElMessage.success('个人信息更新成功')
  } catch (error) {
    ElMessage.error('更新失败')
  } finally {
    loading.value = false
  }
}

const handleReset = () => {
  form.value = {
    name: userInfo.value.name,
    email: userInfo.value.email,
    phone: userInfo.value.phone,
  }
}

const handleChangePassword = async () => {
  if (!passwordFormRef.value) return

  try {
    await passwordFormRef.value.validate()
    passwordLoading.value = true
    await authApi.changePassword(
      passwordForm.value.oldPassword,
      passwordForm.value.newPassword
    )
    ElMessage.success('密码修改成功，请重新登录')
    handleResetPassword()
  } catch (error) {
    ElMessage.error('密码修改失败')
  } finally {
    passwordLoading.value = false
  }
}

const handleResetPassword = () => {
  passwordForm.value = {
    oldPassword: '',
    newPassword: '',
    confirmPassword: '',
  }
}

const handleChangeAvatar = () => {
  ElMessage.info('头像上传功能开发中...')
}

onMounted(() => {
  handleReset()
})
</script>

<style scoped lang="scss">
.profile-page {
  .profile-card {
    text-align: center;

    .profile-avatar {
      margin-bottom: 20px;

      :deep(.el-avatar) {
        border: 2px solid #e4e7eb;
        padding: 2px;
      }

      .el-button {
        margin-top: 10px;
      }
    }
  }

  .edit-card {
    margin-bottom: 20px;

    .form-actions {
      display: flex;
      gap: 10px;
    }
  }
}
</style>
