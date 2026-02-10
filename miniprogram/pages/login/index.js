import { request } from '../../utils/request'

Page({
  data: {
    phone: '',
    password: '',
    loading: false,
    showPassword: false,
    loginMode: 'password', // 'password' or 'code'
    verificationCode: '',
    codeCountdown: 0,
  },

  // 手机号输入
  onPhoneInput: function (e) {
    this.setData({
      phone: e.detail.value,
    })
  },

  // 密码输入
  onPasswordInput: function (e) {
    this.setData({
      password: e.detail.value,
    })
  },

  // 验证码输入
  onCodeInput: function (e) {
    this.setData({
      verificationCode: e.detail.value,
    })
  },

  // 切换密码显示
  togglePasswordVisibility: function () {
    this.setData({
      showPassword: !this.data.showPassword,
    })
  },

  // 切换登录模式
  switchLoginMode: function (e) {
    const mode = e.currentTarget.dataset.mode
    this.setData({
      loginMode: mode,
      phone: '',
      password: '',
      verificationCode: '',
      codeCountdown: 0,
    })
  },

  // 密码登录
  loginWithPassword: function () {
    const { phone, password } = this.data

    if (!phone) {
      wx.showToast({
        title: '请输入手机号',
        icon: 'none',
      })
      return
    }

    if (!password) {
      wx.showToast({
        title: '请输入密码',
        icon: 'none',
      })
      return
    }

    this.performLogin({
      phone: phone,
      password: password,
    })
  },

  // 验证码登录
  loginWithCode: function () {
    const { phone, verificationCode } = this.data

    if (!phone) {
      wx.showToast({
        title: '请输入手机号',
        icon: 'none',
      })
      return
    }

    if (!verificationCode) {
      wx.showToast({
        title: '请输入验证码',
        icon: 'none',
      })
      return
    }

    this.performLogin({
      phone: phone,
      verification_code: verificationCode,
    })
  },

  // 发送验证码
  sendVerificationCode: function () {
    const { phone, codeCountdown } = this.data

    if (!phone) {
      wx.showToast({
        title: '请先输入手机号',
        icon: 'none',
      })
      return
    }

    if (codeCountdown > 0) {
      return
    }

    const app = getApp()

    request({
      url: `${app.globalData.apiUrl}/auth/send-code`,
      method: 'POST',
      data: { phone: phone },
    })
      .then(() => {
        wx.showToast({
          title: '验证码已发送',
          icon: 'success',
        })

        // 开始倒计时
        let countdown = 60
        this.setData({ codeCountdown: countdown })

        const timer = setInterval(() => {
          countdown--
          this.setData({ codeCountdown: countdown })

          if (countdown <= 0) {
            clearInterval(timer)
          }
        }, 1000)
      })
      .catch((err) => {
        console.error('发送验证码失败:', err)
        wx.showToast({
          title: '发送失败',
          icon: 'none',
        })
      })
  },

  // 执行登录
  performLogin: function (credentials) {
    const app = getApp()

    this.setData({ loading: true })

    request({
      url: `${app.globalData.apiUrl}/auth/login`,
      method: 'POST',
      data: credentials,
    })
      .then((res) => {
        const result = res.data || res
        const { access_token, refresh_token, user } = result

        // 保存token
        wx.setStorageSync('access_token', access_token)
        if (refresh_token) {
          wx.setStorageSync('refresh_token', refresh_token)
        }

        // 保存用户信息
        if (user) {
          wx.setStorageSync('user', JSON.stringify(user))
        }

        wx.showToast({
          title: '登录成功',
          icon: 'success',
        })

        // 等待提示消失后跳转
        setTimeout(() => {
          wx.reLaunch({
            url: '/pages/index/index',
          })
        }, 1500)
      })
      .catch((err) => {
        console.error('登录失败:', err)
        let errorMessage = '登录失败'

        if (err.data && err.data.detail) {
          errorMessage = err.data.detail
        } else if (err.message) {
          errorMessage = err.message
        }

        wx.showToast({
          title: errorMessage,
          icon: 'none',
        })
      })
      .finally(() => {
        this.setData({ loading: false })
      })
  },

  // 微信授权登录
  loginWithWeChat: function () {
    const app = getApp()

    wx.login({
      success: (res) => {
        if (res.code) {
          this.setData({ loading: true })

          request({
            url: `${app.globalData.apiUrl}/auth/wechat-login`,
            method: 'POST',
            data: { code: res.code },
          })
            .then((result) => {
              const { access_token, refresh_token, user } = result.data || result

              wx.setStorageSync('access_token', access_token)
              if (refresh_token) {
                wx.setStorageSync('refresh_token', refresh_token)
              }

              if (user) {
                wx.setStorageSync('user', JSON.stringify(user))
              }

              wx.showToast({
                title: '登录成功',
                icon: 'success',
              })

              setTimeout(() => {
                wx.reLaunch({
                  url: '/pages/index/index',
                })
              }, 1500)
            })
            .catch((err) => {
              console.error('微信登录失败:', err)
              wx.showToast({
                title: '微信登录失败',
                icon: 'none',
              })
            })
            .finally(() => {
              this.setData({ loading: false })
            })
        }
      },
    })
  },
})
