import client from './client'

// 获取产品列表
export const getProducts = (params) => {
  return client.get('/products', { params })
}

// 获取产品详情
export const getProductDetail = (productId) => {
  return client.get(`/products/${productId}`)
}

// 创建产品
export const createProduct = (data) => {
  return client.post('/products', data)
}

// 更新产品
export const updateProduct = (productId, data) => {
  return client.put(`/products/${productId}`, data)
}

// 删除产品
export const deleteProduct = (productId) => {
  return client.delete(`/products/${productId}`)
}

// 获取产品分类列表
export const getCategories = () => {
  return client.get('/product-categories')
}

// 获取分类详情
export const getCategoryDetail = (categoryId) => {
  return client.get(`/product-categories/${categoryId}`)
}

// 创建分类
export const createCategory = (data) => {
  return client.post('/product-categories', data)
}

// 更新分类
export const updateCategory = (categoryId, data) => {
  return client.put(`/product-categories/${categoryId}`, data)
}

// 删除分类
export const deleteCategory = (categoryId) => {
  return client.delete(`/product-categories/${categoryId}`)
}

// 批量更新库存
export const updateStock = (productId, quantity) => {
  return client.put(`/products/${productId}/stock`, { quantity })
}

// 获取产品销售统计
export const getProductSales = (params) => {
  return client.get('/products/sales', { params })
}

// 批量导入产品
export const importProducts = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return client.post('/products/import', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

// 导出产品列表
export const exportProducts = (params) => {
  return client.get('/products/export', { params, responseType: 'blob' })
}
