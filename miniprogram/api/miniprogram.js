/**
 * 小程序 API 接口定义
 */

import { request } from '../utils/request'

const API_URL = wx.getApp().globalData.apiUrl

// ============= 产品相关 =============

export const ProductAPI = {
  /**
   * 获取产品分类列表
   */
  getCategories() {
    return request({
      url: `${API_URL}/products/categories`,
      method: 'GET',
    })
  },

  /**
   * 获取产品列表
   */
  getProducts(params) {
    return request({
      url: `${API_URL}/products/list`,
      method: 'GET',
      data: params,
    })
  },

  /**
   * 获取推荐产品
   */
  getFeaturedProducts() {
    return request({
      url: `${API_URL}/products/featured`,
      method: 'GET',
    })
  },

  /**
   * 获取产品详情
   */
  getProductDetail(productId) {
    return request({
      url: `${API_URL}/products/${productId}`,
      method: 'GET',
    })
  },
}

// ============= 订单相关 =============

export const OrderAPI = {
  /**
   * 创建订单
   */
  createOrder(data) {
    return request({
      url: `${API_URL}/orders/create`,
      method: 'POST',
      data: data,
    })
  },

  /**
   * 获取我的订单
   */
  getMyOrders(params) {
    return request({
      url: `${API_URL}/orders/my-orders`,
      method: 'GET',
      data: params,
    })
  },

  /**
   * 获取订单详情
   */
  getOrderDetail(orderId) {
    return request({
      url: `${API_URL}/orders/${orderId}`,
      method: 'GET',
    })
  },

  /**
   * 取消订单
   */
  cancelOrder(orderId) {
    return request({
      url: `${API_URL}/orders/${orderId}/cancel`,
      method: 'POST',
    })
  },

  /**
   * 删除订单
   */
  deleteOrder(orderId) {
    return request({
      url: `${API_URL}/orders/${orderId}`,
      method: 'DELETE',
    })
  },

  /**
   * 获取支付信息
   */
  getPaymentInfo(orderId) {
    return request({
      url: `${API_URL}/orders/${orderId}/payment`,
      method: 'POST',
    })
  },

  /**
   * 获取订单统计
   */
  getStatistics() {
    return request({
      url: `${API_URL}/orders/statistics`,
      method: 'GET',
    })
  },
}

// ============= 用户相关 =============

export const UserAPI = {
  /**
   * 获取用户信息
   */
  getProfile() {
    return request({
      url: `${API_URL}/users/profile`,
      method: 'GET',
    })
  },

  /**
   * 更新用户地址
   */
  updateAddress(data) {
    return request({
      url: `${API_URL}/users/update-address`,
      method: 'POST',
      data: data,
    })
  },

  /**
   * 更新用户信息
   */
  updateProfile(data) {
    return request({
      url: `${API_URL}/users/update-profile`,
      method: 'POST',
      data: data,
    })
  },
}

// ============= 认证相关 =============

export const AuthAPI = {
  /**
   * 密码登录
   */
  loginWithPassword(phone, password) {
    return request({
      url: `${API_URL}/auth/login`,
      method: 'POST',
      data: {
        phone: phone,
        password: password,
      },
    })
  },

  /**
   * 验证码登录
   */
  loginWithCode(phone, verificationCode) {
    return request({
      url: `${API_URL}/auth/login`,
      method: 'POST',
      data: {
        phone: phone,
        verification_code: verificationCode,
      },
    })
  },

  /**
   * 发送验证码
   */
  sendVerificationCode(phone) {
    return request({
      url: `${API_URL}/auth/send-code`,
      method: 'POST',
      data: {
        phone: phone,
      },
    })
  },

  /**
   * 微信登录
   */
  loginWithWeChat(code) {
    return request({
      url: `${API_URL}/auth/wechat-login`,
      method: 'POST',
      data: {
        code: code,
      },
    })
  },

  /**
   * 刷新token
   */
  refreshToken(refreshToken) {
    return request({
      url: `${API_URL}/auth/refresh-token`,
      method: 'POST',
      data: {
        refresh_token: refreshToken,
      },
    })
  },
}

// ============= 支付相关 =============

export const PaymentAPI = {
  /**
   * 获取微信支付参数
   */
  getWeChatPaymentParams(orderId) {
    return request({
      url: `${API_URL}/payments/wechat`,
      method: 'POST',
      data: {
        order_id: orderId,
      },
    })
  },

  /**
   * 更新支付状态
   */
  updatePaymentStatus(orderId, status) {
    return request({
      url: `${API_URL}/payments/status`,
      method: 'POST',
      data: {
        order_id: orderId,
        status: status,
      },
    })
  },
}
