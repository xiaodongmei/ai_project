import axios from 'axios'
import router from '../router'

// 创建 axios 实例
const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
client.interceptors.request.use(
  (config) => {
    // 添加认证令牌
    const token = localStorage.getItem('access_token') || localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
client.interceptors.response.use(
  (response) => {
    // 如果响应本身就包含data，直接返回response.data
    // 否则返回整个response对象
    return response.data || response
  },
  (error) => {
    if (error.response) {
      const { status, data } = error.response

      if (status === 401) {
        // 认证失败，清除 token 并跳转登录
        localStorage.removeItem('access_token')
        localStorage.removeItem('token')
        router.push('/login')
      } else if (status === 403) {
        // 权限不足
        console.error('Permission denied')
      }
    }

    return Promise.reject(error)
  }
)

export default client
