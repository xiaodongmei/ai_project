import client from './client'

// 获取仪表板数据
export const getDashboardData = (params) => {
  return client.get('/statistics/dashboard', { params })
}

// 获取日统计数据
export const getDailyStatistics = (params) => {
  return client.get('/statistics/daily', { params })
}

// 获取收入统计
export const getRevenueStatistics = (params) => {
  return client.get('/statistics/revenue', { params })
}

// 获取客流量统计
export const getTrafficStatistics = (params) => {
  return client.get('/statistics/traffic', { params })
}

// 获取渠道统计
export const getChannelStatistics = (params) => {
  return client.get('/statistics/channels', { params })
}

// 获取员工绩效统计
export const getEmployeePerformanceStatistics = (params) => {
  return client.get('/statistics/employees/performance', { params })
}

// 获取员工提成统计
export const getEmployeeCommissionStatistics = (params) => {
  return client.get('/statistics/employees/commission', { params })
}

// 获取产品销售统计
export const getProductSalesStatistics = (params) => {
  return client.get('/statistics/products/sales', { params })
}

// 获取产品分类销售统计
export const getCategorySalesStatistics = (params) => {
  return client.get('/statistics/categories/sales', { params })
}

// 获取时间段销售对比
export const getSalesComparison = (params) => {
  return client.get('/statistics/sales-comparison', { params })
}

// 导出统计数据
export const exportStatistics = (type, params) => {
  return client.get(`/statistics/${type}/export`, { params, responseType: 'blob' })
}
