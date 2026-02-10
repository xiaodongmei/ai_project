import { request } from '../../utils/request'

Page({
  data: {
    orders: [],
    currentTab: 'all',
    loading: false,
    hasMore: true,
    page: 1,
    pageSize: 10,
  },

  onShow: function () {
    this.loadOrders()
  },

  // 加载订单列表
  loadOrders: function (reset = false) {
    if (this.data.loading) return

    const page = reset ? 1 : this.data.page
    const app = getApp()

    this.setData({ loading: true })

    let url = `${app.globalData.apiUrl}/orders/my-orders?page=${page}&page_size=${this.data.pageSize}`

    if (this.data.currentTab !== 'all') {
      url += `&status=${this.data.currentTab}`
    }

    request({
      url: url,
      method: 'GET',
    })
      .then((res) => {
        const newOrders = res.data || res || []
        const orders = reset ? newOrders : this.data.orders.concat(newOrders)

        this.setData({
          orders: orders,
          page: page + 1,
          hasMore: newOrders.length >= this.data.pageSize,
          loading: false,
        })
      })
      .catch((err) => {
        console.error('加载订单失败:', err)
        this.setData({ loading: false })
        wx.showToast({
          title: '加载失败',
          icon: 'none',
        })
      })
  },

  // 切换标签
  onTabChange: function (e) {
    const tab = e.currentTarget.dataset.tab
    this.setData({
      currentTab: tab,
      orders: [],
      page: 1,
    })
    this.loadOrders(true)
  },

  // 查看订单详情
  viewOrderDetail: function (e) {
    const orderId = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/order/detail?id=${orderId}`,
    })
  },

  // 取消订单
  cancelOrder: function (e) {
    const orderId = e.currentTarget.dataset.id

    wx.showModal({
      title: '确认取消',
      content: '确定要取消这个订单吗？',
      success: (res) => {
        if (res.confirm) {
          this.performCancelOrder(orderId)
        }
      },
    })
  },

  // 执行取消订单
  performCancelOrder: function (orderId) {
    const app = getApp()

    request({
      url: `${app.globalData.apiUrl}/orders/${orderId}/cancel`,
      method: 'POST',
    })
      .then(() => {
        wx.showToast({
          title: '已取消',
          icon: 'success',
        })
        this.loadOrders(true)
      })
      .catch((err) => {
        console.error('取消订单失败:', err)
        wx.showToast({
          title: '取消失败',
          icon: 'none',
        })
      })
  },

  // 删除订单
  deleteOrder: function (e) {
    const orderId = e.currentTarget.dataset.id

    wx.showModal({
      title: '确认删除',
      content: '删除后将无法恢复，确定继续？',
      success: (res) => {
        if (res.confirm) {
          this.performDeleteOrder(orderId)
        }
      },
    })
  },

  // 执行删除订单
  performDeleteOrder: function (orderId) {
    const app = getApp()

    request({
      url: `${app.globalData.apiUrl}/orders/${orderId}`,
      method: 'DELETE',
    })
      .then(() => {
        wx.showToast({
          title: '已删除',
          icon: 'success',
        })
        this.loadOrders(true)
      })
      .catch((err) => {
        console.error('删除订单失败:', err)
        wx.showToast({
          title: '删除失败',
          icon: 'none',
        })
      })
  },

  // 获取状态标签
  getStatusLabel: function (status) {
    const statusMap = {
      pending: '待支付',
      completed: '已完成',
      cancelled: '已取消',
      refunded: '已退款',
    }
    return statusMap[status] || status
  },

  // 滚动到底部
  onReachBottom: function () {
    if (this.data.hasMore && !this.data.loading) {
      this.loadOrders()
    }
  },
})
