import { request } from '../../utils/request'

Page({
  data: {
    product: null,
    quantity: 1,
    specifications: [],
    selectedSpecs: {},
    loading: true,
    price: 0,
  },

  onLoad: function (options) {
    const productId = options.id
    if (productId) {
      this.loadProductDetail(productId)
    }
  },

  // 加载产品详情
  loadProductDetail: function (productId) {
    const app = getApp()

    request({
      url: `${app.globalData.apiUrl}/products/${productId}`,
      method: 'GET',
    })
      .then((res) => {
        const product = res.data || res
        this.setData({
          product: product,
          price: product.member_price || product.non_member_price,
          loading: false,
        })
        // 更新页面标题
        wx.setNavigationBarTitle({
          title: product.name,
        })
      })
      .catch((err) => {
        console.error('加载产品详情失败:', err)
        this.setData({ loading: false })
        wx.showToast({
          title: '加载失败',
          icon: 'none',
        })
      })
  },

  // 增加数量
  increaseQuantity: function () {
    this.setData({
      quantity: this.data.quantity + 1,
    })
  },

  // 减少数量
  decreaseQuantity: function () {
    if (this.data.quantity > 1) {
      this.setData({
        quantity: this.data.quantity - 1,
      })
    }
  },

  // 手动输入数量
  onQuantityInput: function (e) {
    let quantity = parseInt(e.detail.value) || 1
    if (quantity < 1) quantity = 1
    if (quantity > 999) quantity = 999

    this.setData({
      quantity: quantity,
    })
  },

  // 规格选择
  selectSpecification: function (e) {
    const spec = e.currentTarget.dataset.spec
    const selected = e.currentTarget.dataset.selected

    const selectedSpecs = { ...this.data.selectedSpecs }
    if (selectedSpecs[spec] === selected) {
      delete selectedSpecs[spec]
    } else {
      selectedSpecs[spec] = selected
    }

    this.setData({
      selectedSpecs: selectedSpecs,
    })
  },

  // 加入购物车
  addToCart: function () {
    const { product, quantity, selectedSpecs } = this.data

    const cartItems = wx.getStorageSync('cart') || []
    const cartItem = {
      id: product.id,
      name: product.name,
      price: this.data.price,
      image_url: product.image_url,
      quantity: quantity,
      specifications: selectedSpecs,
    }

    const existingItem = cartItems.find(
      (item) =>
        item.id === product.id &&
        JSON.stringify(item.specifications) === JSON.stringify(selectedSpecs)
    )

    if (existingItem) {
      existingItem.quantity += quantity
    } else {
      cartItems.push(cartItem)
    }

    wx.setStorageSync('cart', cartItems)

    wx.showToast({
      title: '已添加到购物车',
      icon: 'success',
      duration: 1500,
    })

    // 1.5秒后返回上一页
    setTimeout(() => {
      wx.navigateBack()
    }, 1500)
  },

  // 立即购买
  buyNow: function () {
    this.addToCart()
    setTimeout(() => {
      wx.navigateTo({
        url: '/pages/cart/index',
      })
    }, 1000)
  },

  // 分享
  onShareAppMessage: function () {
    const { product } = this.data
    return {
      title: product.name,
      path: `/pages/product/detail?id=${product.id}`,
      imageUrl: product.image_url,
    }
  },
})
