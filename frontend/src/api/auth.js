import client from './client'

// 用户登录
export const login = (username, password) => {
  return client.post('/auth/login', {
    username,
    password,
  })
}

// 发送验证码
export const sendCode = (phone) => {
  return client.post('/auth/send-code', {
    phone,
  })
}

// 用户注册
export const register = (data) => {
  return client.post('/auth/register', data)
}

// 刷新令牌
export const refreshToken = (refreshToken) => {
  return client.post('/auth/refresh', {
    refresh_token: refreshToken,
  })
}

// 获取当前用户信息
export const getCurrentUser = () => {
  return client.get('/users/profile')
}

// 更新用户信息
export const updateUser = (userId, data) => {
  return client.put(`/users/${userId}`, data)
}

// 修改密码
export const changePassword = (oldPassword, newPassword) => {
  return client.post('/users/change-password', {
    old_password: oldPassword,
    new_password: newPassword,
  })
}

// 登出
export const logout = () => {
  return client.post('/auth/logout')
}
