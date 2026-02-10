Page({
  data: {
    cartItems: [],
    selectedItems: new Set(),
    totalPrice: 0,
    totalQuantity: 0,
    isEditMode: false,
  },

  onShow: function () {
    this.loadCart()
  },

  // 从本地存储加载购物车
  loadCart: function () {
    const cartItems = wx.getStorageSync('cart') || []
    this.setData({
      cartItems: cartItems,
    })
    this.calculateTotal()
  },

  // 选择/取消选择商品
  toggleItemSelection: function (e) {
    const index = e.currentTarget.dataset.index
    const selectedItems = new Set(this.data.selectedItems)

    if (selectedItems.has(index)) {
      selectedItems.delete(index)
    } else {
      selectedItems.add(index)
    }

    this.setData({
      selectedItems: selectedItems,
    })
    this.calculateTotal()
  },

  // 全选/取消全选
  toggleSelectAll: function () {
    const { cartItems, selectedItems } = this.data

    if (selectedItems.size === cartItems.length) {
      // 取消全选
      this.setData({
        selectedItems: new Set(),
      })
    } else {
      // 全选
      const newSelected = new Set()
      cartItems.forEach((_, index) => {
        newSelected.add(index)
      })
      this.setData({
        selectedItems: newSelected,
      })
    }
    this.calculateTotal()
  },

  // 增加数量
  increaseQuantity: function (e) {
    const index = e.currentTarget.dataset.index
    const cartItems = [...this.data.cartItems]
    cartItems[index].quantity += 1
    this.setData({ cartItems })
    this.saveCart()
    this.calculateTotal()
  },

  // 减少数量
  decreaseQuantity: function (e) {
    const index = e.currentTarget.dataset.index
    const cartItems = [...this.data.cartItems]

    if (cartItems[index].quantity > 1) {
      cartItems[index].quantity -= 1
      this.setData({ cartItems })
      this.saveCart()
      this.calculateTotal()
    }
  },

  // 手动输入数量
  onQuantityInput: function (e) {
    const index = e.currentTarget.dataset.index
    let quantity = parseInt(e.detail.value) || 1

    if (quantity < 1) quantity = 1
    if (quantity > 999) quantity = 999

    const cartItems = [...this.data.cartItems]
    cartItems[index].quantity = quantity
    this.setData({ cartItems })
    this.saveCart()
    this.calculateTotal()
  },

  // 删除商品
  removeItem: function (e) {
    const index = e.currentTarget.dataset.index
    const cartItems = [...this.data.cartItems]
    cartItems.splice(index, 1)

    const selectedItems = new Set(this.data.selectedItems)
    selectedItems.delete(index)

    this.setData({
      cartItems,
      selectedItems,
    })
    this.saveCart()
    this.calculateTotal()

    wx.showToast({
      title: '已删除',
      icon: 'success',
      duration: 1500,
    })
  },

  // 批量删除选中的商品
  deleteSelectedItems: function () {
    const { cartItems, selectedItems } = this.data

    if (selectedItems.size === 0) {
      wx.showToast({
        title: '请先选择商品',
        icon: 'none',
      })
      return
    }

    wx.showModal({
      title: '确认删除',
      content: `确定删除选中的${selectedItems.size}件商品吗？`,
      success: (res) => {
        if (res.confirm) {
          const newCartItems = cartItems.filter((_, index) => !selectedItems.has(index))
          this.setData({
            cartItems: newCartItems,
            selectedItems: new Set(),
          })
          this.saveCart()
          this.calculateTotal()

          wx.showToast({
            title: '已删除',
            icon: 'success',
          })
        }
      },
    })
  },

  // 计算总价和总数量
  calculateTotal: function () {
    const { cartItems, selectedItems } = this.data
    let totalPrice = 0
    let totalQuantity = 0

    cartItems.forEach((item, index) => {
      if (selectedItems.has(index)) {
        totalPrice += item.price * item.quantity
        totalQuantity += item.quantity
      }
    })

    this.setData({
      totalPrice: totalPrice.toFixed(2),
      totalQuantity: totalQuantity,
    })
  },

  // 保存购物车到本地存储
  saveCart: function () {
    wx.setStorageSync('cart', this.data.cartItems)
  },

  // 继续购物
  continueShopping: function () {
    wx.switchTab({
      url: '/pages/product/index',
    })
  },

  // 结算
  checkout: function () {
    const { selectedItems, totalQuantity, totalPrice } = this.data

    if (selectedItems.size === 0) {
      wx.showToast({
        title: '请先选择商品',
        icon: 'none',
      })
      return
    }

    const selectedProducts = this.data.cartItems.filter((_, index) => selectedItems.has(index))

    // 保存订单信息到本地，用于订单确认页面
    wx.setStorageSync('orderItems', selectedProducts)

    wx.navigateTo({
      url: '/pages/order/detail?type=new',
    })
  },

  // 清空购物车
  clearCart: function () {
    wx.showModal({
      title: '清空购物车',
      content: '确定清空购物车吗？',
      success: (res) => {
        if (res.confirm) {
          this.setData({
            cartItems: [],
            selectedItems: new Set(),
          })
          this.saveCart()
          this.calculateTotal()

          wx.showToast({
            title: '已清空',
            icon: 'success',
          })
        }
      },
    })
  },

  // 切换编辑模式
  toggleEditMode: function () {
    this.setData({
      isEditMode: !this.data.isEditMode,
      selectedItems: new Set(),
    })
    this.calculateTotal()
  },
})
