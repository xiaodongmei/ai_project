import { request } from '../../utils/request'

Page({
  data: {
    order: null,
    orderItems: [],
    type: 'view', // 'view' or 'new'
    loading: true,
    deliveryAddress: '',
    remarks: '',
    paymentMethod: 'wechat',
    submitting: false,
  },

  onLoad: function (options) {
    const { id, type } = options

    if (type === 'new') {
      // 新订单模式
      this.loadCartItemsForOrder()
      this.loadUserInfo()
    } else if (id) {
      // 查看现有订单
      this.loadOrderDetail(id)
    }
  },

  // 加载购物车商品用于创建订单
  loadCartItemsForOrder: function () {
    const orderItems = wx.getStorageSync('orderItems') || []
    this.setData({
      orderItems: orderItems,
      type: 'new',
      loading: false,
    })
  },

  // 加载用户信息
  loadUserInfo: function () {
    const app = getApp()
    const userStr = wx.getStorageSync('user')
    const user = userStr ? JSON.parse(userStr) : null

    if (user && user.address) {
      this.setData({
        deliveryAddress: user.address,
      })
    }
  },

  // 加载订单详情
  loadOrderDetail: function (orderId) {
    const app = getApp()

    request({
      url: `${app.globalData.apiUrl}/orders/${orderId}`,
      method: 'GET',
    })
      .then((res) => {
        const order = res.data || res
        this.setData({
          order: order,
          type: 'view',
          loading: false,
        })
        // 更新页面标题
        wx.setNavigationBarTitle({
          title: '订单详情',
        })
      })
      .catch((err) => {
        console.error('加载订单详情失败:', err)
        this.setData({ loading: false })
        wx.showToast({
          title: '加载失败',
          icon: 'none',
        })
      })
  },

  // 修改收货地址
  onAddressChange: function (e) {
    this.setData({
      deliveryAddress: e.detail.value,
    })
  },

  // 修改备注
  onRemarksChange: function (e) {
    this.setData({
      remarks: e.detail.value,
    })
  },

  // 选择支付方式
  selectPaymentMethod: function (e) {
    this.setData({
      paymentMethod: e.currentTarget.dataset.method,
    })
  },

  // 编辑地址
  editAddress: function () {
    wx.navigateTo({
      url: '/pages/profile/index?action=editAddress',
    })
  },

  // 计算总金额
  calculateTotal: function () {
    const total = this.data.orderItems.reduce((sum, item) => {
      return sum + item.price * item.quantity
    }, 0)
    return total.toFixed(2)
  },

  // 提交订单
  submitOrder: function () {
    const { orderItems, deliveryAddress, remarks, paymentMethod } = this.data

    if (orderItems.length === 0) {
      wx.showToast({
        title: '订单为空',
        icon: 'none',
      })
      return
    }

    if (!deliveryAddress) {
      wx.showToast({
        title: '请输入收货地址',
        icon: 'none',
      })
      return
    }

    this.setData({ submitting: true })

    const app = getApp()
    const orderData = {
      items: orderItems,
      delivery_address: deliveryAddress,
      remarks: remarks,
      payment_method: paymentMethod,
      total_amount: this.calculateTotal(),
    }

    request({
      url: `${app.globalData.apiUrl}/orders/create`,
      method: 'POST',
      data: orderData,
    })
      .then((res) => {
        const newOrder = res.data || res

        // 清空购物车
        wx.removeStorageSync('cart')
        wx.removeStorageSync('orderItems')

        wx.showToast({
          title: '订单已提交',
          icon: 'success',
        })

        // 等待支付
        setTimeout(() => {
          if (paymentMethod === 'wechat') {
            this.initiateWeChat Payment(newOrder.id)
          } else {
            // 跳转到订单详情
            wx.redirectTo({
              url: `/pages/order/index`,
            })
          }
        }, 1500)
      })
      .catch((err) => {
        console.error('提交订单失败:', err)
        wx.showToast({
          title: '提交失败',
          icon: 'none',
        })
      })
      .finally(() => {
        this.setData({ submitting: false })
      })
  },

  // 发起微信支付
  initiateWeChatPayment: function (orderId) {
    const app = getApp()

    request({
      url: `${app.globalData.apiUrl}/orders/${orderId}/payment`,
      method: 'POST',
    })
      .then((res) => {
        const paymentInfo = res.data || res

        wx.requestPayment({
          timeStamp: paymentInfo.timeStamp,
          nonceStr: paymentInfo.nonceStr,
          package: paymentInfo.package,
          signType: 'RSA',
          paySign: paymentInfo.paySign,
          success: (res) => {
            wx.showToast({
              title: '支付成功',
              icon: 'success',
            })
            setTimeout(() => {
              wx.redirectTo({
                url: `/pages/order/index`,
              })
            }, 1500)
          },
          fail: (err) => {
            console.error('支付失败:', err)
            wx.showToast({
              title: '支付失败',
              icon: 'none',
            })
          },
        })
      })
      .catch((err) => {
        console.error('获取支付信息失败:', err)
        wx.showToast({
          title: '获取支付信息失败',
          icon: 'none',
        })
      })
  },

  // 取消订单
  cancelOrder: function () {
    if (!this.data.order || !this.data.order.id) return

    wx.showModal({
      title: '确认取消',
      content: '确定要取消这个订单吗？',
      success: (res) => {
        if (res.confirm) {
          this.performCancelOrder()
        }
      },
    })
  },

  // 执行取消
  performCancelOrder: function () {
    const app = getApp()
    const orderId = this.data.order.id

    request({
      url: `${app.globalData.apiUrl}/orders/${orderId}/cancel`,
      method: 'POST',
    })
      .then(() => {
        wx.showToast({
          title: '已取消',
          icon: 'success',
        })
        setTimeout(() => {
          wx.navigateBack()
        }, 1500)
      })
      .catch((err) => {
        console.error('取消订单失败:', err)
        wx.showToast({
          title: '取消失败',
          icon: 'none',
        })
      })
  },
})
