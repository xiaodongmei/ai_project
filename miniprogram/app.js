App({
  onLaunch: function () {
    // 获取系统信息
    this.getSystemInfo()
    // 检查登录状态
    this.checkLogin()
  },

  onShow: function () {
    console.log('App Show')
  },

  onHide: function () {
    console.log('App Hide')
  },

  getSystemInfo: function () {
    const that = this
    wx.getSystemInfo({
      success: function (res) {
        that.globalData.systemInfo = res
      },
    })
  },

  checkLogin: function () {
    const that = this
    const accessToken = wx.getStorageSync('access_token')
    const userStr = wx.getStorageSync('user')

    if (accessToken && userStr) {
      // 已登录，保存用户信息和token
      that.globalData.token = accessToken
      that.globalData.userInfo = JSON.parse(userStr)
      // 验证 token 是否有效
      that.validateToken()
    } else {
      // 未登录，跳转到登录页
      wx.reLaunch({
        url: '/pages/login/index',
      })
    }
  },

  validateToken: function () {
    const that = this
    const accessToken = wx.getStorageSync('access_token')

    if (!accessToken) {
      wx.reLaunch({
        url: '/pages/login/index',
      })
      return
    }

    wx.request({
      url: this.globalData.apiUrl + '/users/profile',
      method: 'GET',
      header: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + accessToken,
      },
      success: function (res) {
        if (res.statusCode === 200) {
          const user = res.data
          that.globalData.userInfo = user
          wx.setStorageSync('user', JSON.stringify(user))
        }
      },
      fail: function () {
        // token 无效，清除并跳转到登录
        wx.removeStorageSync('access_token')
        wx.removeStorageSync('refresh_token')
        wx.removeStorageSync('user')
        wx.reLaunch({
          url: '/pages/login/index',
        })
      },
    })
  },

  globalData: {
    apiUrl: 'http://localhost:8000/api/v1', // 根据实际环境修改
    token: null,
    userInfo: null,
    systemInfo: null,
  },
})
