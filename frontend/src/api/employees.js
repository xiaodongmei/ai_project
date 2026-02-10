import client from './client'

// 获取员工列表
export const getEmployees = (params) => {
  return client.get('/employees', { params })
}

// 获取员工详情
export const getEmployeeDetail = (employeeId) => {
  return client.get(`/employees/${employeeId}`)
}

// 创建员工
export const createEmployee = (data) => {
  return client.post('/employees', data)
}

// 更新员工信息
export const updateEmployee = (employeeId, data) => {
  return client.put(`/employees/${employeeId}`, data)
}

// 删除员工
export const deleteEmployee = (employeeId) => {
  return client.delete(`/employees/${employeeId}`)
}

// 获取员工绩效
export const getEmployeePerformance = (employeeId, params) => {
  return client.get(`/employees/${employeeId}/performance`, { params })
}

// 获取员工提成
export const getEmployeeCommission = (employeeId, params) => {
  return client.get(`/employees/${employeeId}/commission`, { params })
}

// 获取员工接待列表
export const getEmployeeOrders = (employeeId, params) => {
  return client.get(`/employees/${employeeId}/orders`, { params })
}

// 获取员工排行榜
export const getEmployeeRanking = (params) => {
  return client.get('/employees/ranking', { params })
}

// 批量导入员工
export const importEmployees = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return client.post('/employees/import', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

// 导出员工列表
export const exportEmployees = (params) => {
  return client.get('/employees/export', { params, responseType: 'blob' })
}
