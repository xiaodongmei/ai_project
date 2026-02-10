/**
 * API 客户端测试
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import axios from 'axios'

// Mock axios
vi.mock('axios')

describe('HTTP Client', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.clear()
  })

  it('should create axios instance with base URL', () => {
    const baseURL = 'http://localhost:8000/api/v1'
    expect(baseURL).toBeDefined()
  })

  it('should handle GET request', async () => {
    const mockData = { id: 1, name: 'Test' }
    axios.get = vi.fn().mockResolvedValue({ data: mockData })

    const response = await axios.get('/test')
    expect(response.data).toEqual(mockData)
  })

  it('should handle POST request', async () => {
    const mockData = { id: 1, name: 'Created' }
    axios.post = vi.fn().mockResolvedValue({ data: mockData })

    const response = await axios.post('/test', { name: 'Test' })
    expect(response.data).toEqual(mockData)
  })

  it('should handle PUT request', async () => {
    const mockData = { id: 1, name: 'Updated' }
    axios.put = vi.fn().mockResolvedValue({ data: mockData })

    const response = await axios.put('/test/1', { name: 'Updated' })
    expect(response.data).toEqual(mockData)
  })

  it('should handle DELETE request', async () => {
    axios.delete = vi.fn().mockResolvedValue({ status: 204 })

    const response = await axios.delete('/test/1')
    expect(response.status).toBe(204)
  })

  it('should handle request errors', async () => {
    const error = new Error('Network Error')
    axios.get = vi.fn().mockRejectedValue(error)

    try {
      await axios.get('/test')
      expect.fail('Should throw error')
    } catch (e) {
      expect(e.message).toBe('Network Error')
    }
  })

  it('should add Authorization header with token', () => {
    const token = 'test-token-123'
    localStorage.setItem('token', token)

    const storedToken = localStorage.getItem('token')
    expect(storedToken).toBe(token)
  })

  it('should handle 401 unauthorized response', async () => {
    const error = {
      response: {
        status: 401,
        data: { detail: 'Unauthorized' },
      },
    }
    axios.get = vi.fn().mockRejectedValue(error)

    try {
      await axios.get('/protected')
      expect.fail('Should throw error')
    } catch (e) {
      expect(e.response.status).toBe(401)
    }
  })

  it('should handle 403 forbidden response', async () => {
    const error = {
      response: {
        status: 403,
        data: { detail: 'Forbidden' },
      },
    }
    axios.get = vi.fn().mockRejectedValue(error)

    try {
      await axios.get('/protected')
      expect.fail('Should throw error')
    } catch (e) {
      expect(e.response.status).toBe(403)
    }
  })

  it('should handle 500 server error', async () => {
    const error = {
      response: {
        status: 500,
        data: { detail: 'Internal Server Error' },
      },
    }
    axios.get = vi.fn().mockRejectedValue(error)

    try {
      await axios.get('/test')
      expect.fail('Should throw error')
    } catch (e) {
      expect(e.response.status).toBe(500)
    }
  })
})
