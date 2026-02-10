import client from './client'

// 获取订单列表
export const getOrders = (params) => {
  return client.get('/orders', { params })
}

// 获取订单详情
export const getOrderDetail = (orderId) => {
  return client.get(`/orders/${orderId}`)
}

// 创建订单
export const createOrder = (data) => {
  return client.post('/orders', data)
}

// 更新订单
export const updateOrder = (orderId, data) => {
  return client.put(`/orders/${orderId}`, data)
}

// 删除订单
export const deleteOrder = (orderId) => {
  return client.delete(`/orders/${orderId}`)
}

// 更新订单状态
export const updateOrderStatus = (orderId, status) => {
  return client.patch(`/orders/${orderId}/status`, { status })
}

// 获取订单的支付记录
export const getOrderPayments = (orderId) => {
  return client.get(`/orders/${orderId}/payments`)
}

// 添加订单支付
export const addOrderPayment = (orderId, data) => {
  return client.post(`/orders/${orderId}/payments`, data)
}

// 取消订单
export const cancelOrder = (orderId, reason = '') => {
  return client.post(`/orders/${orderId}/cancel`, { reason })
}

// 退货订单
export const refundOrder = (orderId, data) => {
  return client.post(`/orders/${orderId}/refund`, data)
}

// 完成订单
export const completeOrder = (orderId) => {
  return client.post(`/orders/${orderId}/complete`)
}

// 获取订单统计
export const getOrderStatistics = (params) => {
  return client.get('/orders/statistics', { params })
}

// 批量导出订单
export const exportOrders = (params) => {
  return client.get('/orders/export', { params, responseType: 'blob' })
}
