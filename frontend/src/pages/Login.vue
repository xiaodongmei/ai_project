<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <h1>养生店管理系统</h1>
        <p>Wellness Shop Management System</p>
      </div>

      <el-form
        ref="formRef"
        :model="loginForm"
        :rules="rules"
        @keyup.enter="handleLogin"
        class="login-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="用户名或邮箱"
            prefix-icon="User"
            clearable
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码"
            prefix-icon="Lock"
            clearable
            show-password
          />
        </el-form-item>

        <el-form-item>
          <el-checkbox v-model="rememberMe">记住账号</el-checkbox>
          <el-link type="primary" href="#" class="forgot-link">忘记密码？</el-link>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            @click="handleLogin"
            class="login-btn"
          >
            {{ loading ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>
      </el-form>

      <div class="login-footer">
        <p>还没有账号？<el-link type="primary" @click="goRegister">立即注册</el-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'
import * as authApi from '@/api/auth'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref(null)
const loading = ref(false)
const rememberMe = ref(false)

const loginForm = ref({
  username: localStorage.getItem('remember_username') || '',
  password: '',
})

const rules = {
  username: [
    { required: true, message: '请输入用户名或邮箱', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度为3-50个字符', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6个字符', trigger: 'blur' },
  ],
}

const handleLogin = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    loading.value = true

    // 调用登录 API
    const response = await authApi.login(loginForm.value.username, loginForm.value.password)

    // 保存 token 和用户信息到 store
    if (response && response.access_token) {
      // 使用 userStore 保存登录状态
      userStore.setTokens({
        access_token: response.access_token,
        refresh_token: response.refresh_token || response.access_token
      })

      // 设置用户信息
      if (response.user) {
        userStore.setUser(response.user)
      } else {
        // 如果没有返回用户信息，创建默认用户对象
        userStore.setUser({
          username: loginForm.value.username,
          role: '管理员'
        })
      }

      // 记住账号
      if (rememberMe.value) {
        localStorage.setItem('remember_username', loginForm.value.username)
      } else {
        localStorage.removeItem('remember_username')
      }

      ElMessage.success('登录成功！')

      // 直接跳转到仪表盘
      await router.push('/dashboard')
    } else {
      ElMessage.error('登录失败：服务器返回数据异常')
      console.error('Login response:', response)
    }
  } catch (error) {
    console.error('Login error:', error)

    // 更完善的错误处理
    let errorMessage = '登录失败，请检查用户名和密码'

    if (error.response) {
      errorMessage = error.response.data?.detail || error.response.data?.message || errorMessage
    } else if (error.message) {
      errorMessage = error.message
    }

    ElMessage.error(errorMessage)
  } finally {
    loading.value = false
  }
}

const goRegister = () => {
  router.push('/register')
}


</script>

<style scoped lang="scss">
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
  width: 100%;
  max-width: 420px;
  padding: 50px 30px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;

  h1 {
    font-size: 28px;
    margin: 0 0 8px 0;
    color: #333;
    font-weight: 600;
  }

  p {
    font-size: 14px;
    color: #999;
    margin: 0;
  }
}

.login-form {
  :deep(.el-form-item) {
    margin-bottom: 22px;
  }

  :deep(.el-input__wrapper) {
    background-color: #f5f7fa;

    &:hover {
      background-color: #f0f2f5;
    }
  }

  :deep(.el-checkbox__label) {
    color: #666;
    font-size: 14px;
  }

  .forgot-link {
    float: right;
    font-size: 14px;
  }
}

.login-btn {
  width: 100%;
  height: 40px;
  font-size: 16px;
  font-weight: 500;
  border-radius: 4px;
  margin-top: 20px;
}

.login-footer {
  text-align: center;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;

  p {
    font-size: 12px;
    color: #999;
    margin: 0;
  }
}

@media (max-width: 480px) {
  .login-box {
    padding: 30px 20px;
  }

  .login-header h1 {
    font-size: 24px;
  }
}
</style>
