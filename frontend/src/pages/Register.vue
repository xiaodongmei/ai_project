<template>
  <div class="register-container">
    <div class="register-box">
      <div class="register-header">
        <h1>养生店管理系统</h1>
        <p>Wellness Shop Management System</p>
      </div>

      <el-form
        ref="formRef"
        :model="registerForm"
        :rules="rules"
        class="register-form"
      >
        <el-form-item prop="phone">
          <el-input
            v-model="registerForm.phone"
            placeholder="请输入手机号"
            prefix-icon="Phone"
            clearable
            maxlength="11"
          />
        </el-form-item>

        <el-form-item prop="code">
          <div class="code-input-group">
            <el-input
              v-model="registerForm.code"
              placeholder="请输入验证码"
              prefix-icon="Message"
              clearable
              maxlength="6"
            />
            <el-button
              :disabled="codeButtonDisabled"
              @click="sendCode"
              class="code-button"
            >
              {{ codeButtonText }}
            </el-button>
          </div>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            @click="handleRegister"
            class="register-btn"
          >
            {{ loading ? '注册中...' : '注册' }}
          </el-button>
        </el-form-item>
      </el-form>

      <div class="register-divider">
        <span>或</span>
      </div>

      <div class="register-methods">
        <el-button class="wechat-btn" @click="handleWechatLogin">
          <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%2309B83E' d='M12 0C5.4 0 0 4.2 0 9.6c0 3 1.4 5.7 3.7 7.4-.2 1.5-.9 3.5-2.1 4.8 2.3-.6 4.5-2.1 5.9-3.5 1 .1 2.1.2 3.2.2 6.6 0 12-4.2 12-9.6S18.6 0 12 0z'/%3E%3C/svg%3E" alt="微信" />
          微信登录
        </el-button>
      </div>

      <div class="register-footer">
        <p>已有账号？<el-link type="primary" @click="goLogin">去登录</el-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import * as authApi from '@/api/auth'

const router = useRouter()
const formRef = ref(null)
const loading = ref(false)
const codeButtonDisabled = ref(false)
const codeCountdown = ref(0)
const codeButtonText = ref('获取验证码')

const registerForm = ref({
  phone: '',
  code: '',
})

const rules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '手机号码格式不正确', trigger: 'blur' },
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { len: 6, message: '验证码为6位', trigger: 'blur' },
  ],
}

const sendCode = async () => {
  // 验证手机号
  if (!registerForm.value.phone) {
    ElMessage.warning('请输入手机号')
    return
  }

  if (!/^1[3-9]\d{9}$/.test(registerForm.value.phone)) {
    ElMessage.warning('手机号码格式不正确')
    return
  }

  try {
    loading.value = true
    // 调用发送验证码 API
    await authApi.sendCode(registerForm.value.phone)
    ElMessage.success('验证码已发送')

    // 开始倒计时
    codeButtonDisabled.value = true
    codeCountdown.value = 60

    const timer = setInterval(() => {
      codeCountdown.value--
      codeButtonText.value = `${codeCountdown.value}秒后重试`

      if (codeCountdown.value <= 0) {
        clearInterval(timer)
        codeButtonDisabled.value = false
        codeButtonText.value = '重新获取'
      }
    }, 1000)
  } catch (error) {
    const message = error.response?.data?.detail || '发送验证码失败'
    ElMessage.error(message)
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    loading.value = true

    // 调用注册 API
    const response = await authApi.register({
      phone: registerForm.value.phone,
      code: registerForm.value.code,
    })

    if (response && (response.message || response.user)) {
      ElMessage.success('注册成功，请登录')
      router.push('/login')
    } else {
      ElMessage.error('注册失败，请重试')
    }
  } catch (error) {
    console.error('Register error:', error)
    const message = error.response?.data?.detail || '注册失败，请重试'
    ElMessage.error(message)
  } finally {
    loading.value = false
  }
}

const handleWechatLogin = () => {
  ElMessage.info('微信登录功能开发中')
  // 后续可集成微信登录
}

const goLogin = () => {
  router.push('/login')
}
</script>

<style scoped lang="scss">
.register-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.register-box {
  width: 100%;
  max-width: 420px;
  padding: 50px 30px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
}

.register-header {
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

.register-form {
  :deep(.el-form-item) {
    margin-bottom: 22px;
  }

  :deep(.el-input__wrapper) {
    background-color: #f5f7fa;

    &:hover {
      background-color: #f0f2f5;
    }
  }
}

.code-input-group {
  display: flex;
  gap: 10px;
  align-items: center;

  :deep(.el-input) {
    flex: 1;
  }
}

.code-button {
  white-space: nowrap;
  padding: 0 16px;
  height: 40px;

  &:disabled {
    opacity: 0.6;
  }
}

.register-btn {
  width: 100%;
  height: 40px;
  font-size: 16px;
  font-weight: 500;
  border-radius: 4px;
  margin-top: 20px;
}

.register-divider {
  display: flex;
  align-items: center;
  margin: 30px 0;
  color: #ccc;

  &::before,
  &::after {
    content: '';
    flex: 1;
    height: 1px;
    background-color: #ddd;
  }

  span {
    padding: 0 10px;
    font-size: 12px;
    color: #999;
  }
}

.register-methods {
  display: flex;
  gap: 10px;

  .wechat-btn {
    width: 100%;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    background-color: #09b83e;
    border-color: #09b83e;
    color: white;
    font-size: 14px;

    &:hover {
      background-color: #07a030;
      border-color: #07a030;
      color: white;
    }

    img {
      width: 18px;
      height: 18px;
    }
  }
}

.register-footer {
  text-align: center;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;

  p {
    font-size: 14px;
    color: #666;
    margin: 0;

    :deep(.el-link) {
      font-size: 14px;
      margin-left: 5px;
    }
  }
}

@media (max-width: 480px) {
  .register-box {
    padding: 30px 20px;
  }

  .register-header h1 {
    font-size: 24px;
  }

  .code-input-group {
    flex-direction: column;

    .code-button {
      width: 100%;
    }
  }
}
</style>
