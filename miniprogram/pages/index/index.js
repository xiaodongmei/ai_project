import { request } from '../../utils/request'

Page({
  data: {
    banners: [],
    categories: [],
    featuredProducts: [],
    loading: true,
  },

  onLoad: function () {
    this.loadHomeData()
  },

  // 加载首页数据
  loadHomeData: function () {
    this.loadBanners()
    this.loadCategories()
    this.loadFeaturedProducts()
  },

  // 加载轮播图
  loadBanners: function () {
    const app = getApp()

    // 模拟轮播图数据 - 实际应从API获取
    const banners = [
      {
        id: 1,
        image: '/images/banner1.png',
        title: '热销产品',
      },
      {
        id: 2,
        image: '/images/banner2.png',
        title: '优惠活动',
      },
      {
        id: 3,
        image: '/images/banner3.png',
        title: '新品上市',
      },
    ]

    this.setData({
      banners: banners,
    })
  },

  // 加载分类
  loadCategories: function () {
    const app = getApp()

    request({
      url: `${app.globalData.apiUrl}/products/categories`,
      method: 'GET',
    })
      .then((res) => {
        const categories = res.data || res || []
        this.setData({
          categories: categories.slice(0, 6), // 只显示6个分类
        })
      })
      .catch((err) => {
        console.error('加载分类失败:', err)
      })
  },

  // 加载推荐产品
  loadFeaturedProducts: function () {
    const app = getApp()

    request({
      url: `${app.globalData.apiUrl}/products/featured`,
      method: 'GET',
    })
      .then((res) => {
        const products = res.data || res || []
        this.setData({
          featuredProducts: products.slice(0, 6),
          loading: false,
        })
      })
      .catch((err) => {
        console.error('加载推荐产品失败:', err)
        this.setData({ loading: false })
      })
  },

  // 轮播图点击
  onBannerTap: function (e) {
    const banner = e.currentTarget.dataset.banner
    // 可以根据banner类型跳转到不同页面
    wx.navigateTo({
      url: '/pages/product/index',
    })
  },

  // 分类点击
  onCategoryTap: function (e) {
    const categoryId = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/product/index?categoryId=${categoryId}`,
    })
  },

  // 产品点击
  onProductTap: function (e) {
    const productId = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/product/detail?id=${productId}`,
    })
  },

  // 快速加入购物车
  quickAddToCart: function (e) {
    const product = e.currentTarget.dataset.product
    const cartItems = wx.getStorageSync('cart') || []

    const existingItem = cartItems.find((item) => item.id === product.id)
    if (existingItem) {
      existingItem.quantity += 1
    } else {
      cartItems.push({
        id: product.id,
        name: product.name,
        price: product.member_price || product.non_member_price,
        image_url: product.image_url,
        quantity: 1,
      })
    }

    wx.setStorageSync('cart', cartItems)
    wx.showToast({
      title: '已添加到购物车',
      icon: 'success',
      duration: 1500,
    })
  },

  // 下拉刷新
  onPullDownRefresh: function () {
    this.loadHomeData()
    wx.stopPullDownRefresh()
  },

  // 搜索
  onSearch: function () {
    wx.navigateTo({
      url: '/pages/product/index',
    })
  },
})
