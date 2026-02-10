import { request, getUser, clearUserData } from '../../utils/request'

Page({
  data: {
    user: null,
    editingAddress: false,
    address: '',
    phone: '',
    statistics: {
      totalOrders: 0,
      pendingOrders: 0,
      completedOrders: 0,
      totalSpent: 0,
    },
  },

  onShow: function () {
    this.loadUserInfo()
    this.loadStatistics()
  },

  // 加载用户信息
  loadUserInfo: function () {
    const userStr = wx.getStorageSync('user')
    const user = userStr ? JSON.parse(userStr) : null

    if (user) {
      this.setData({
        user: user,
        address: user.address || '',
        phone: user.phone || '',
      })
    } else {
      // 从后端获取用户信息
      this.fetchUserInfo()
    }
  },

  // 从后端获取用户信息
  fetchUserInfo: function () {
    const app = getApp()

    request({
      url: `${app.globalData.apiUrl}/users/profile`,
      method: 'GET',
    })
      .then((res) => {
        const user = res.data || res
        wx.setStorageSync('user', JSON.stringify(user))
        this.setData({
          user: user,
          address: user.address || '',
          phone: user.phone || '',
        })
      })
      .catch((err) => {
        console.error('加载用户信息失败:', err)
      })
  },

  // 加载统计信息
  loadStatistics: function () {
    const app = getApp()

    request({
      url: `${app.globalData.apiUrl}/orders/statistics`,
      method: 'GET',
    })
      .then((res) => {
        const stats = res.data || res
        this.setData({
          statistics: {
            totalOrders: stats.total_orders || 0,
            pendingOrders: stats.pending_orders || 0,
            completedOrders: stats.completed_orders || 0,
            totalSpent: stats.total_spent || 0,
          },
        })
      })
      .catch((err) => {
        console.error('加载统计信息失败:', err)
      })
  },

  // 编辑地址
  editAddress: function () {
    this.setData({
      editingAddress: true,
    })
  },

  // 保存地址
  saveAddress: function () {
    const { address, phone } = this.data

    if (!address) {
      wx.showToast({
        title: '请输入收货地址',
        icon: 'none',
      })
      return
    }

    const app = getApp()

    request({
      url: `${app.globalData.apiUrl}/users/update-address`,
      method: 'POST',
      data: {
        address: address,
        phone: phone,
      },
    })
      .then((res) => {
        const user = { ...this.data.user, address, phone }
        wx.setStorageSync('user', JSON.stringify(user))
        this.setData({
          user: user,
          editingAddress: false,
        })

        wx.showToast({
          title: '已保存',
          icon: 'success',
        })
      })
      .catch((err) => {
        console.error('保存地址失败:', err)
        wx.showToast({
          title: '保存失败',
          icon: 'none',
        })
      })
  },

  // 取消编辑
  cancelEdit: function () {
    this.setData({
      editingAddress: false,
    })
    this.loadUserInfo()
  },

  // 修改地址
  onAddressChange: function (e) {
    this.setData({
      address: e.detail.value,
    })
  },

  // 修改电话
  onPhoneChange: function (e) {
    this.setData({
      phone: e.detail.value,
    })
  },

  // 我的订单
  goToOrders: function () {
    wx.switchTab({
      url: '/pages/order/index',
    })
  },

  // 收藏列表
  goToFavorites: function () {
    wx.navigateTo({
      url: '/pages/profile/favorites',
    })
  },

  // 帮助中心
  goToHelp: function () {
    wx.navigateTo({
      url: '/pages/profile/help',
    })
  },

  // 关于我们
  goToAbout: function () {
    wx.navigateTo({
      url: '/pages/profile/about',
    })
  },

  // 登出
  logout: function () {
    wx.showModal({
      title: '确认登出',
      content: '确定要登出吗？',
      success: (res) => {
        if (res.confirm) {
          clearUserData()
          wx.reLaunch({
            url: '/pages/login/index',
          })
        }
      },
    })
  },

  // 分享小程序
  onShareAppMessage: function () {
    return {
      title: '养生店管理系统',
      path: '/pages/index/index',
    }
  },
})
