/**
 * 店铺配置和行业模板 API
 */
import request from './client'

/** 获取当前店铺完整配置（合并行业模板+自定义） */
export function getShopConfig() {
  return request.get('/config/shop')
}

/** 更新店铺配置 */
export function updateShopConfig(data) {
  return request.put('/config/shop', data)
}

/** 获取所有行业模板列表 */
export function getIndustryTemplates() {
  return request.get('/config/templates')
}

/** 获取指定行业模板详情 */
export function getIndustryTemplateDetail(industryType) {
  return request.get(`/config/templates/${industryType}`)
}
