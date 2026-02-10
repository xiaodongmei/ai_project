/**
 * Pinia 用户存储测试
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// 定义一个测试用的 store
const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || '')
  const isAuthenticated = computed(() => !!token.value && !!user.value)

  const setUser = (userData) => {
    user.value = userData
  }

  const setToken = (newToken) => {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
    } else {
      localStorage.removeItem('token')
    }
  }

  const logout = () => {
    user.value = null
    token.value = ''
    localStorage.removeItem('token')
  }

  return {
    user,
    token,
    isAuthenticated,
    setUser,
    setToken,
    logout,
  }
})

describe('User Store (Pinia)', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.clearAllMocks()
  })

  it('should initialize with empty state', () => {
    const store = useUserStore()
    expect(store.user).toBeNull()
    expect(store.token).toBe('')
    expect(store.isAuthenticated).toBe(false)
  })

  it('should set user data', () => {
    const store = useUserStore()
    const userData = {
      id: 1,
      username: 'testuser',
      email: 'test@example.com',
      role: 'employee',
    }

    store.setUser(userData)
    expect(store.user).toEqual(userData)
  })

  it('should set token and save to localStorage', () => {
    const store = useUserStore()
    const token = 'test-token-123'

    store.setToken(token)
    expect(store.token).toBe(token)
    expect(localStorage.setItem).toHaveBeenCalledWith('token', token)
  })

  it('should compute isAuthenticated correctly', () => {
    const store = useUserStore()

    // 未认证状态
    expect(store.isAuthenticated).toBe(false)

    // 设置用户和令牌
    store.setUser({ id: 1, username: 'testuser' })
    store.setToken('test-token')
    expect(store.isAuthenticated).toBe(true)

    // 清除用户
    store.setUser(null)
    expect(store.isAuthenticated).toBe(false)
  })

  it('should logout and clear data', () => {
    const store = useUserStore()

    // 设置初始状态
    store.setUser({ id: 1, username: 'testuser' })
    store.setToken('test-token')
    expect(store.isAuthenticated).toBe(true)

    // 登出
    store.logout()
    expect(store.user).toBeNull()
    expect(store.token).toBe('')
    expect(store.isAuthenticated).toBe(false)
    expect(localStorage.removeItem).toHaveBeenCalledWith('token')
  })

  it('should preserve token from localStorage on init', () => {
    localStorage.setItem('token', 'stored-token')
    const store = useUserStore()
    expect(store.token).toBe('stored-token')
  })

  it('should handle clearing token', () => {
    const store = useUserStore()
    store.setToken('test-token')
    expect(store.token).toBe('test-token')

    store.setToken('')
    expect(store.token).toBe('')
    expect(localStorage.removeItem).toHaveBeenCalledWith('token')
  })

  it('should maintain user role', () => {
    const store = useUserStore()
    const adminUser = {
      id: 1,
      username: 'admin',
      role: 'admin',
    }

    store.setUser(adminUser)
    expect(store.user.role).toBe('admin')
  })

  it('should handle user profile updates', () => {
    const store = useUserStore()
    const initialUser = {
      id: 1,
      username: 'testuser',
      email: 'old@example.com',
    }

    store.setUser(initialUser)
    expect(store.user.email).toBe('old@example.com')

    // 更新用户信息
    const updatedUser = {
      ...initialUser,
      email: 'new@example.com',
    }
    store.setUser(updatedUser)
    expect(store.user.email).toBe('new@example.com')
  })

  it('should support multiple tokens', () => {
    const store = useUserStore()

    // 设置第一个令牌
    store.setToken('token-1')
    expect(store.token).toBe('token-1')

    // 设置第二个令牌（覆盖）
    store.setToken('token-2')
    expect(store.token).toBe('token-2')
    expect(localStorage.setItem).toHaveBeenLastCalledWith('token', 'token-2')
  })
})
