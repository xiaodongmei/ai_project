import client from './client'

// 获取顾客列表
export const getCustomers = (params) => {
  return client.get('/customers', { params })
}

// 获取顾客详情
export const getCustomerDetail = (customerId) => {
  return client.get(`/customers/${customerId}`)
}

// 创建顾客
export const createCustomer = (data) => {
  return client.post('/customers', data)
}

// 更新顾客信息
export const updateCustomer = (customerId, data) => {
  return client.put(`/customers/${customerId}`, data)
}

// 删除顾客
export const deleteCustomer = (customerId) => {
  return client.delete(`/customers/${customerId}`)
}

// 获取顾客的消费记录
export const getCustomerOrders = (customerId, params) => {
  return client.get(`/customers/${customerId}/orders`, { params })
}

// 获取顾客的卡券
export const getCustomerCards = (customerId) => {
  return client.get(`/customers/${customerId}/cards`)
}

// 获取顾客的会员信息
export const getCustomerMembership = (customerId) => {
  return client.get(`/customers/${customerId}/membership`)
}

// 批量导入顾客
export const importCustomers = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return client.post('/customers/import', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

// 导出顾客列表
export const exportCustomers = (params) => {
  return client.get('/customers/export', { params, responseType: 'blob' })
}
