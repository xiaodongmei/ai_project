import { request } from '../utils/request'

const API_BASE_URL = 'http://localhost:8000/api/v1'

/**
 * 账号密码登录
 */
export const loginByPassword = (username, password) => {
  return request({
    url: `${API_BASE_URL}/auth/login/password`,
    method: 'POST',
    data: {
      username,
      password,
    },
  })
}

/**
 * 账号密码注册
 */
export const registerByPassword = (data) => {
  return request({
    url: `${API_BASE_URL}/auth/register/password`,
    method: 'POST',
    data: {
      username: data.username,
      email: data.email,
      password: data.password,
      full_name: data.fullName,
    },
  })
}

/**
 * 发送手机验证码
 */
export const sendPhoneCode = (phone, type = 'login') => {
  return request({
    url: `${API_BASE_URL}/auth/send-phone-code`,
    method: 'POST',
    data: {
      phone,
      type,
    },
  })
}

/**
 * 手机号登录
 */
export const loginByPhone = (phone, code) => {
  return request({
    url: `${API_BASE_URL}/auth/login/phone`,
    method: 'POST',
    data: {
      phone,
      code,
    },
  })
}

/**
 * 手机号注册
 */
export const registerByPhone = (data) => {
  return request({
    url: `${API_BASE_URL}/auth/register/phone`,
    method: 'POST',
    data: {
      phone: data.phone,
      code: data.code,
      password: data.password,
      full_name: data.fullName,
    },
  })
}

/**
 * 微信登录/注册
 */
export const loginByWechat = (code, userInfo = null) => {
  return request({
    url: `${API_BASE_URL}/auth/login/wechat`,
    method: 'POST',
    data: {
      code,
      userInfo,
    },
  })
}

/**
 * 绑定微信账号
 */
export const bindWechat = (userId, code) => {
  return request({
    url: `${API_BASE_URL}/auth/bind-wechat/${userId}`,
    method: 'POST',
    data: {
      code,
    },
  })
}

/**
 * 刷新访问令牌
 */
export const refreshToken = (refreshToken) => {
  return request({
    url: `${API_BASE_URL}/auth/refresh-token`,
    method: 'POST',
    data: {
      refresh_token: refreshToken,
    },
  })
}
