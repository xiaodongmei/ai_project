import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as authApi from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('access_token') || '')
  const refreshToken = ref(localStorage.getItem('refresh_token') || '')
  const isAuthenticated = computed(() => !!accessToken.value)

  // ========== 用户信息管理 ==========

  const setUser = (userData) => {
    user.value = userData
  }

  const setTokens = (tokens) => {
    accessToken.value = tokens.access_token
    refreshToken.value = tokens.refresh_token
    localStorage.setItem('access_token', tokens.access_token)
    localStorage.setItem('refresh_token', tokens.refresh_token)
  }

  const logout = () => {
    user.value = null
    accessToken.value = ''
    refreshToken.value = ''
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  // ========== 账号密码认证 ==========

  const loginByPassword = async (username, password) => {
    try {
      const response = await authApi.loginByPassword(username, password)
      setTokens(response)
      setUser(response.user)
      return response
    } catch (error) {
      throw error
    }
  }

  const registerByPassword = async (data) => {
    try {
      const response = await authApi.registerByPassword(data)
      setTokens(response)
      setUser(response.user)
      return response
    } catch (error) {
      throw error
    }
  }

  // ========== 手机号认证 ==========

  const sendPhoneCode = async (phone, type = 'login') => {
    try {
      const response = await authApi.sendPhoneCode(phone, type)
      return response
    } catch (error) {
      throw error
    }
  }

  const loginByPhone = async (phone, code) => {
    try {
      const response = await authApi.loginByPhone(phone, code)
      setTokens(response)
      setUser(response.user)
      return response
    } catch (error) {
      throw error
    }
  }

  const registerByPhone = async (data) => {
    try {
      const response = await authApi.registerByPhone(data)
      setTokens(response)
      setUser(response.user)
      return response
    } catch (error) {
      throw error
    }
  }

  // ========== 微信认证 ==========

  const loginByWechat = async (code, userInfo = null) => {
    try {
      const response = await authApi.loginByWechat(code, userInfo)
      setTokens(response)
      setUser(response.user)
      return response
    } catch (error) {
      throw error
    }
  }

  const bindWechat = async (code) => {
    try {
      if (!user.value) {
        throw new Error('未找到用户信息')
      }
      const response = await authApi.bindWechat(user.value.id, code)
      return response
    } catch (error) {
      throw error
    }
  }

  // ========== Token 管理 ==========

  const refreshAccessToken = async () => {
    try {
      if (!refreshToken.value) {
        logout()
        return
      }
      const response = await authApi.refreshToken(refreshToken.value)
      setTokens(response)
      return response
    } catch (error) {
      logout()
      throw error
    }
  }

  return {
    user,
    accessToken,
    refreshToken,
    isAuthenticated,
    setUser,
    setTokens,
    logout,
    // 账号密码
    loginByPassword,
    registerByPassword,
    // 手机号
    sendPhoneCode,
    loginByPhone,
    registerByPhone,
    // 微信
    loginByWechat,
    bindWechat,
    // Token管理
    refreshAccessToken,
  }
})
