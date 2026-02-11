/**
 * 服务项目管理 API
 */
import request from './client'

/** 获取服务项目列表 */
export function getServiceItems(params) {
  return request.get('/service-items', { params })
}

/** 获取单个服务项目 */
export function getServiceItem(id) {
  return request.get(`/service-items/${id}`)
}

/** 创建服务项目 */
export function createServiceItem(data) {
  return request.post('/service-items', data)
}

/** 更新服务项目 */
export function updateServiceItem(id, data) {
  return request.put(`/service-items/${id}`, data)
}

/** 删除服务项目 */
export function deleteServiceItem(id) {
  return request.delete(`/service-items/${id}`)
}

/** 重置为行业模板默认服务 */
export function resetServiceItems() {
  return request.post('/service-items/reset')
}
