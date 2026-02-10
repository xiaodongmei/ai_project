import client from './client'

export const roomsApi = {
  // 获取房间列表
  getRooms(params = {}) {
    return client.get('/rooms', { params })
  },

  // 获取房间总览统计
  getSummary() {
    return client.get('/rooms/summary')
  },

  // 获取技师列表
  getTechnicians() {
    return client.get('/rooms/technicians')
  },

  // 获取单个房间
  getRoom(roomId) {
    return client.get(`/rooms/${roomId}`)
  },

  // 创建房间
  createRoom(data) {
    return client.post('/rooms', data)
  },

  // 更新房间
  updateRoom(roomId, data) {
    return client.put(`/rooms/${roomId}`, data)
  },

  // 删除房间
  deleteRoom(roomId) {
    return client.delete(`/rooms/${roomId}`)
  },

  // 开床
  openBed(roomId, bedId, data) {
    return client.post(`/rooms/${roomId}/beds/${bedId}/open`, data)
  },

  // 结账
  checkoutBed(roomId, bedId) {
    return client.post(`/rooms/${roomId}/beds/${bedId}/checkout`)
  },

  // 延长服务
  extendService(roomId, bedId, data) {
    return client.post(`/rooms/${roomId}/beds/${bedId}/extend`, data)
  },

  // 更换技师
  changeTechnician(roomId, bedId, data) {
    return client.post(`/rooms/${roomId}/beds/${bedId}/change-technician`, data)
  },

  // 获取所有可用房间
  getAvailableRooms() {
    return client.get('/rooms/available/list')
  },
}
