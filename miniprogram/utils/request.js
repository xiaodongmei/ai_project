/**
 * HTTP 请求工具
 */

// 处理请求队列，防止多个 token 刷新请求
let requestQueue = []
let isRefreshing = false

/**
 * 发起HTTP请求
 */
export const request = (options) => {
  return new Promise((resolve, reject) => {
    const accessToken = wx.getStorageSync('access_token')
    const refreshToken = wx.getStorageSync('refresh_token')

    // 如果token即将过期或已过期，先刷新token
    if (isTokenExpiring(accessToken) && refreshToken) {
      // 如果已在刷新中，将请求加入队列
      if (isRefreshing) {
        requestQueue.push(() => {
          performRequest(options, resolve, reject)
        })
      } else {
        // 开始刷新token
        isRefreshing = true
        refreshAccessToken(refreshToken)
          .then(() => {
            // 刷新成功，执行队列中的请求
            requestQueue.forEach((callback) => callback())
            requestQueue = []
            performRequest(options, resolve, reject)
          })
          .catch(() => {
            // 刷新失败，清除token并重定向到登录页
            wx.removeStorageSync('access_token')
            wx.removeStorageSync('refresh_token')
            wx.removeStorageSync('user')
            wx.redirectTo({
              url: '/pages/login/index',
            })
            reject(new Error('Token expired'))
          })
          .finally(() => {
            isRefreshing = false
          })
      }
    } else {
      performRequest(options, resolve, reject)
    }
  })
}

/**
 * 执行实际的请求
 */
function performRequest(options, resolve, reject) {
  const accessToken = wx.getStorageSync('access_token')

  // 构建请求头
  const headers = {
    'Content-Type': 'application/json',
    ...options.header,
  }

  if (accessToken) {
    headers['Authorization'] = `Bearer ${accessToken}`
  }

  wx.request({
    url: options.url,
    method: options.method || 'GET',
    data: options.data,
    header: headers,
    timeout: options.timeout || 10000,
    success: (res) => {
      if (res.statusCode === 200) {
        resolve(res.data)
      } else if (res.statusCode === 401) {
        // 未授权，清除token并重定向
        wx.removeStorageSync('access_token')
        wx.removeStorageSync('refresh_token')
        wx.removeStorageSync('user')
        wx.redirectTo({
          url: '/pages/login/index',
        })
        reject(res)
      } else if (res.statusCode >= 400) {
        reject(res)
      } else {
        resolve(res.data)
      }
    },
    fail: (err) => {
      // 网络错误
      wx.showToast({
        title: '网络请求失败',
        icon: 'none',
      })
      reject(err)
    },
  })
}

/**
 * 刷新访问令牌
 */
function refreshAccessToken(refreshToken) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: 'http://localhost:8000/api/v1/auth/refresh-token',
      method: 'POST',
      data: {
        refresh_token: refreshToken,
      },
      header: {
        'Content-Type': 'application/json',
      },
      success: (res) => {
        if (res.statusCode === 200) {
          const { access_token, refresh_token } = res.data
          wx.setStorageSync('access_token', access_token)
          if (refresh_token) {
            wx.setStorageSync('refresh_token', refresh_token)
          }
          resolve()
        } else {
          reject(new Error('Failed to refresh token'))
        }
      },
      fail: () => {
        reject(new Error('Network error'))
      },
    })
  })
}

/**
 * 检查token是否即将过期（剩余时间少于5分钟）
 */
function isTokenExpiring(token) {
  if (!token) return false

  try {
    // 解析JWT token
    const parts = token.split('.')
    if (parts.length !== 3) return false

    const payload = JSON.parse(atob(parts[1]))
    const expiresAt = payload.exp * 1000 // 转换为毫秒
    const now = Date.now()
    const remainingTime = expiresAt - now

    // 如果剩余时间少于5分钟（300秒），视为即将过期
    return remainingTime < 5 * 60 * 1000
  } catch (e) {
    return false
  }
}

/**
 * 获取存储的token
 */
export const getAccessToken = () => {
  return wx.getStorageSync('access_token')
}

/**
 * 获取存储的用户信息
 */
export const getUser = () => {
  const userStr = wx.getStorageSync('user')
  return userStr ? JSON.parse(userStr) : null
}

/**
 * 清除用户数据
 */
export const clearUserData = () => {
  wx.removeStorageSync('access_token')
  wx.removeStorageSync('refresh_token')
  wx.removeStorageSync('user')
}
