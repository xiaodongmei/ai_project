/**
 * 路由集成测试
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { createRouter, createMemoryHistory } from 'vue-router'

// Mock routes
const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: { template: '<div>Dashboard</div>' },
    meta: { requiresAuth: true },
  },
  {
    path: '/login',
    name: 'Login',
    component: { template: '<div>Login</div>' },
    meta: { requiresAuth: false },
  },
  {
    path: '/customers',
    name: 'Customers',
    component: { template: '<div>Customers</div>' },
    meta: { requiresAuth: true },
  },
  {
    path: '/products',
    name: 'Products',
    component: { template: '<div>Products</div>' },
    meta: { requiresAuth: true },
  },
  {
    path: '/orders',
    name: 'Orders',
    component: { template: '<div>Orders</div>' },
    meta: { requiresAuth: true },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: { template: '<div>Not Found</div>' },
  },
]

describe('Router Integration', () => {
  let router

  beforeEach(() => {
    router = createRouter({
      history: createMemoryHistory(),
      routes,
    })
  })

  it('should navigate to dashboard', async () => {
    await router.push('/')
    expect(router.currentRoute.value.name).toBe('Dashboard')
  })

  it('should navigate to login', async () => {
    await router.push('/login')
    expect(router.currentRoute.value.name).toBe('Login')
  })

  it('should navigate to customers', async () => {
    await router.push('/customers')
    expect(router.currentRoute.value.name).toBe('Customers')
  })

  it('should navigate to products', async () => {
    await router.push('/products')
    expect(router.currentRoute.value.name).toBe('Products')
  })

  it('should navigate to orders', async () => {
    await router.push('/orders')
    expect(router.currentRoute.value.name).toBe('Orders')
  })

  it('should handle invalid routes', async () => {
    await router.push('/invalid-route')
    expect(router.currentRoute.value.name).toBe('NotFound')
  })

  it('should track navigation history', async () => {
    const history = []
    router.beforeEach((to) => {
      history.push(to.name)
    })

    await router.push('/login')
    await router.push('/dashboard')
    await router.push('/customers')

    expect(history).toContain('Login')
    expect(history).toContain('Customers')
  })

  it('should provide route meta information', () => {
    const dashboardRoute = routes.find(r => r.name === 'Dashboard')
    const loginRoute = routes.find(r => r.name === 'Login')

    expect(dashboardRoute.meta.requiresAuth).toBe(true)
    expect(loginRoute.meta.requiresAuth).toBe(false)
  })

  it('should resolve route by name', () => {
    const route = router.getRoutes().find(r => r.name === 'Customers')
    expect(route).toBeDefined()
    expect(route.path).toBe('/customers')
  })

  it('should handle dynamic segments', async () => {
    // 添加带有动态参数的路由
    router.addRoute({
      path: '/customers/:id',
      name: 'CustomerDetail',
      component: { template: '<div>Customer Detail</div>' },
    })

    await router.push('/customers/123')
    expect(router.currentRoute.value.params.id).toBe('123')
  })

  it('should support named route navigation', async () => {
    await router.push({ name: 'Customers' })
    expect(router.currentRoute.value.name).toBe('Customers')
  })

  it('should support query parameters', async () => {
    await router.push({
      name: 'Customers',
      query: { page: '2', sort: 'name' },
    })

    expect(router.currentRoute.value.query.page).toBe('2')
    expect(router.currentRoute.value.query.sort).toBe('name')
  })

  it('should support redirect', async () => {
    router.addRoute({
      path: '/dashboard',
      redirect: '/',
    })

    await router.push('/dashboard')
    // 重定向后应该在 / 路径
    expect(router.currentRoute.value.path).toBe('/')
  })
})
