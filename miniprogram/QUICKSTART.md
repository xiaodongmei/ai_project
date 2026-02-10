# 小程序快速开始指南

## 前置准备

### 1. 获取开发工具
- 下载并安装 [微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)
- 注册微信账号并申请小程序账号
- 获取小程序的 AppID

### 2. 克隆/下载项目
```bash
# 进入小程序目录
cd wellness-shop-system/miniprogram
```

### 3. 配置后端地址
编辑 `app.js` 文件：

```javascript
globalData: {
  apiUrl: 'http://YOUR_BACKEND_URL/api/v1', // 修改为实际的后端地址
  // 示例：http://localhost:8000/api/v1
}
```

## 在开发者工具中打开项目

1. 打开微信开发者工具
2. 点击 "新建/导入项目"
3. 选择项目类型为 "小程序"
4. 项目目录选择 `wellness-shop-system/miniprogram`
5. 输入小程序的 AppID
6. 点击创建

## 快速测试

### 测试账号信息
使用以下测试账号进行登录测试：
- **手机号**: 13800000001
- **密码**: 123456 或使用验证码登录

### 测试流程

#### 1. 登录测试
```
页面: /pages/login/index
- 切换到密码登录
- 输入手机号: 13800000001
- 输入密码: 123456
- 点击登录
```

#### 2. 浏览产品
```
页面: /pages/product/index
- 查看产品列表
- 点击分类进行筛选
- 使用搜索功能查找产品
- 点击产品进入详情
```

#### 3. 购物车操作
```
页面: /pages/cart/index
- 点击快速加购或进入产品详情后添加
- 在购物车页面调整数量
- 选中商品后点击结算
```

#### 4. 订单流程
```
页面: /pages/order/detail
- 填写收货地址
- 选择支付方式
- 添加订单备注（可选）
- 提交订单
- 进行支付（测试环境可跳过）
```

#### 5. 个人中心
```
页面: /pages/profile/index
- 查看用户信息
- 管理收货地址
- 查看订单统计
- 点击登出返回登录页
```

## 常见问题

### Q: 如何修改API地址？
A: 编辑 `/app.js` 中的 `apiUrl`：
```javascript
apiUrl: 'http://your-backend-url/api/v1'
```

### Q: 验证码怎么获取？
A: 点击 "获取验证码" 按钮，后端会发送验证码到手机（测试环境可能需要查看后端日志）。

### Q: 如何调试网络请求？
A:
1. 在开发者工具中打开 "Network" 标签
2. 可以看到所有的 HTTP 请求
3. 查看请求头和响应信息

### Q: 本地开发时如何处理跨域？
A: 在开发者工具中：
1. 右上角点击设置
2. 找到 "项目设置"
3. 勾选 "不校验合法域名..." 选项

### Q: 如何查看控制台日志？
A: 在开发者工具中点击 "Console" 标签，可以看到所有的console日志。

## 文件说明

### 核心文件

| 文件 | 说明 |
|------|------|
| `app.js` | 应用程序入口，配置全局变量 |
| `app.json` | 小程序配置文件，定义页面路由 |
| `utils/request.js` | HTTP请求工具，处理token管理 |
| `api/miniprogram.js` | API接口定义 |

### 页面文件

| 页面 | 功能 | 文件 |
|------|------|------|
| 登录 | 用户认证 | `/pages/login/` |
| 首页 | 首页展示 | `/pages/index/` |
| 产品 | 产品浏览 | `/pages/product/` |
| 购物车 | 购物车管理 | `/pages/cart/` |
| 订单 | 订单管理 | `/pages/order/` |
| 个人 | 用户中心 | `/pages/profile/` |

## 开发建议

### 1. 本地存储调试
在Console中查看本地存储：
```javascript
// 获取token
wx.getStorageSync('access_token')

// 获取用户信息
wx.getStorageSync('user')

// 获取购物车
wx.getStorageSync('cart')

// 清除所有存储
wx.clearStorageSync()
```

### 2. 页面跳转
```javascript
// 打开新页面
wx.navigateTo({ url: '/pages/product/index' })

// 用tab切换
wx.switchTab({ url: '/pages/profile/index' })

// 返回上一页
wx.navigateBack()

// 重新进入小程序
wx.reLaunch({ url: '/pages/index/index' })
```

### 3. 显示提示
```javascript
// 显示toast提示
wx.showToast({
  title: '操作成功',
  icon: 'success',
  duration: 1500
})

// 显示模态框
wx.showModal({
  title: '提示',
  content: '确定要删除吗？',
  success: (res) => {
    if (res.confirm) {
      // 用户点击了确定
    }
  }
})

// 显示加载
wx.showLoading({ title: '加载中...' })
wx.hideLoading()
```

### 4. 调试技巧
- 使用 `console.log()` 输出调试信息
- 在开发者工具的 Sources 标签中设置断点
- 使用 Network 标签查看网络请求
- 使用 Storage 标签查看本地存储

## 常见错误解决

### 错误: "未配置合法域名"
**解决**: 在开发者工具设置中勾选 "不校验合法域名、web-view(业务域名)、TLS 版本以及 HTTPS 证书"

### 错误: "401 Unauthorized"
**解决**:
1. 检查token是否过期
2. 重新登录获取新token
3. 检查后端认证配置

### 错误: "网络请求失败"
**解决**:
1. 检查后端服务是否启动
2. 检查API地址是否正确
3. 检查网络连接

### 错误: "页面不存在"
**解决**: 检查 `app.json` 中的页面配置是否正确

## 上线前检查清单

- [ ] 修改 `app.js` 中的 API 地址为生产环境地址
- [ ] 关闭开发者工具的调试选项
- [ ] 测试所有主要功能流程
- [ ] 检查是否有console.log调试代码
- [ ] 验证所有图片和资源是否加载正常
- [ ] 测试不同网络环境的性能
- [ ] 检查是否有内存泄漏
- [ ] 验证支付功能（如果使用真实支付）

## 获取帮助

### 文档资源
- [微信小程序官方文档](https://developers.weixin.qq.com/miniprogram/dev/framework/)
- [项目开发手册](./MINIPROGRAM_README.md)
- [实现总结](../MINIPROGRAM_IMPLEMENTATION.md)

### 常见问题
遇到问题时，优先查看：
1. 微信开发者工具的Console输出
2. Network标签中的请求信息
3. 项目文档的常见问题部分

## 下一步

1. ✅ 本地开发和测试
2. ✅ 与后端联调
3. ✅ 性能优化
4. ✅ 上线前测试
5. ✅ 提交审核发布

---

有任何问题，请查阅项目文档或联系开发团队！
