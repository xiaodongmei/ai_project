import { request } from '../../utils/request'

Page({
  data: {
    products: [],
    categories: [],
    currentCategory: 'all',
    searchText: '',
    loading: false,
    hasMore: true,
    page: 1,
    pageSize: 10,
    scrollTop: 0,
  },

  onLoad: function () {
    this.loadCategories()
    this.loadProducts()
  },

  // 加载分类
  loadCategories: function () {
    const app = getApp()
    request({
      url: app.globalData.apiUrl + '/products/categories',
      method: 'GET',
    })
      .then((res) => {
        const categories = res.data || res || []
        this.setData({
          categories: categories,
        })
      })
      .catch((err) => {
        console.error('加载分类失败:', err)
      })
  },

  // 加载产品列表
  loadProducts: function (reset = false) {
    if (this.data.loading) return

    const page = reset ? 1 : this.data.page
    const app = getApp()

    this.setData({ loading: true })

    let url = `${app.globalData.apiUrl}/products/list?page=${page}&page_size=${this.data.pageSize}`

    if (this.data.currentCategory !== 'all') {
      url += `&category_id=${this.data.currentCategory}`
    }

    if (this.data.searchText) {
      url += `&search=${encodeURIComponent(this.data.searchText)}`
    }

    request({
      url: url,
      method: 'GET',
    })
      .then((res) => {
        const newProducts = res.data || res || []
        const products = reset ? newProducts : this.data.products.concat(newProducts)

        this.setData({
          products: products,
          page: page + 1,
          hasMore: newProducts.length >= this.data.pageSize,
          loading: false,
        })
      })
      .catch((err) => {
        console.error('加载产品失败:', err)
        this.setData({ loading: false })
        wx.showToast({
          title: '加载失败',
          icon: 'none',
        })
      })
  },

  // 分类切换
  onCategoryChange: function (e) {
    const categoryId = e.currentTarget.dataset.id
    this.setData({
      currentCategory: categoryId,
      products: [],
      page: 1,
    })
    this.loadProducts(true)
  },

  // 搜索
  onSearch: function (e) {
    this.setData({
      searchText: e.detail.value,
    })
  },

  // 执行搜索
  performSearch: function () {
    this.setData({
      products: [],
      page: 1,
    })
    this.loadProducts(true)
  },

  // 清除搜索
  clearSearch: function () {
    this.setData({
      searchText: '',
      products: [],
      page: 1,
    })
    this.loadProducts(true)
  },

  // 产品详情
  viewProductDetail: function (e) {
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

  // 滚动到底部
  onReachBottom: function () {
    if (this.data.hasMore && !this.data.loading) {
      this.loadProducts()
    }
  },

  // 处理滚动事件
  onPageScroll: function (e) {
    this.setData({
      scrollTop: e.scrollTop,
    })
  },

  // 返回顶部
  scrollToTop: function () {
    this.setData({
      scrollTop: 0,
    })
  },
})
