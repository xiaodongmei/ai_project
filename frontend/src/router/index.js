import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/dashboard',
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../pages/Login.vue'),
    meta: {
      requiresAuth: false,
    },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../pages/Register.vue'),
    meta: {
      requiresAuth: false,
    },
  },
  {
    path: '/',
    component: () => import('../layouts/MainLayout.vue'),
    meta: {
      requiresAuth: true,
    },
    children: [
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('../pages/Dashboard.vue'),
        meta: {
          title: '仪表板',
        },
      },
      {
        path: '/customers',
        name: 'Customers',
        component: () => import('../pages/Customers.vue'),
        meta: {
          title: '顾客管理',
        },
      },
      {
        path: '/products',
        name: 'Products',
        component: () => import('../pages/Products.vue'),
        meta: {
          title: '产品管理',
        },
      },
      {
        path: '/orders',
        name: 'Orders',
        component: () => import('../pages/Orders.vue'),
        meta: {
          title: '订单管理',
        },
      },
      {
        path: '/employees',
        name: 'Employees',
        component: () => import('../pages/Employees.vue'),
        meta: {
          title: '员工管理',
        },
      },

      {
        path: '/statistics',
        name: 'Statistics',
        component: () => import('../pages/Statistics.vue'),
        meta: {
          title: '数据统计',
        },
      },
      {
        path: '/profile',
        name: 'Profile',
        component: () => import('../pages/Profile.vue'),
        meta: {
          title: '个人资料',
        },
      },
      {
        path: '/settings',
        name: 'Settings',
        component: () => import('../pages/Settings.vue'),
        meta: {
          title: '系统设置',
        },
      },
      {
        path: '/rooms',
        name: 'Rooms',
        component: () => import('../pages/Rooms.vue'),
        meta: {
          title: '服务空间',
        },
      },
      {
        path: '/appointments',
        name: 'Appointments',
        component: () => import('../pages/Appointments.vue'),
        meta: {
          title: '预约管理',
        },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const accessToken = localStorage.getItem('access_token')

  if (to.meta.requiresAuth && !accessToken) {
    // 需要认证但没有token，重定向到登录页
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && accessToken) {
    // 已登录，重定向到仪表盘
    next('/dashboard')
  } else {
    next()
  }
})

export default router
