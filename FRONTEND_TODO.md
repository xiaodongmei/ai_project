# Vue 前端 - 待完成任务清单

## 订单管理模块

### 1. `src/pages/Orders.vue` - 订单列表页面

实现功能：
- 订单搜索和筛选（订单号、顾客名称、服务员、状态、日期范围）
- 订单列表展示（分页，10/20/50/100条）
- 订单状态过滤（全部、待结算、已完成、已取消、已退单）
- 订单详情查看（抽屉式）
- 订单编辑（修改订单信息、添加项目等）
- 订单支付管理（添加支付、查看支付记录）
- 订单操作（完成、取消、退货）
- 数据导出功能

核心字段：
```vue
{
  order_no: 'ORD20260119001',
  customer_name: '张三',
  employee_name: '店长',
  service_items: ['肩颈疗法', '拔罐'],
  amount: 99.99,
  discount: 10.00,
  actual_amount: 89.99,
  status: 'completed',
  payment_method: '微信支付',
  created_at: '2026-01-19 10:00:00',
}
```

### 2. `src/components/dialogs/OrderDialog.vue` - 订单创建/编辑

实现功能：
- 选择顾客
- 选择服务员
- 添加服务项目（可多选）
- 设置价格和折扣
- 选择支付方式
- 订单备注
- 表单验证

### 3. `src/components/dialogs/OrderPaymentDialog.vue` - 订单支付

实现功能：
- 选择支付方式（微信、支付宝、现金等）
- 输入支付金额
- 生成支付记录
- 显示支付状态

### 4. `src/components/drawers/OrderDrawer.vue` - 订单详情

实现功能：
- 显示订单基本信息
- 展示服务项目列表
- 显示支付记录
- 显示订单操作历史
- 操作按钮（编辑、支付、完成、取消等）

---

## 员工管理模块

### 5. `src/pages/Employees.vue` - 员工列表页面

实现功能：
- 员工搜索和筛选（姓名、岗位、部门、状态）
- 员工列表展示（分页）
- 新增员工
- 编辑员工信息
- 删除员工
- 员工详情查看
- 员工绩效查看
- 数据导出

核心字段：
```vue
{
  name: '店长',
  employee_id: '2003002',
  position: '调理师',
  department: '服务部',
  id_number: '110101199001011234',
  real_name_verified: true,
  salary: 3000.00,
  level: '高级',
  hire_date: '2025-01-01',
  status: 'active',
}
```

### 6. `src/components/dialogs/EmployeeDialog.vue` - 员工新增/编辑

实现功能：
- 输入员工基本信息
- 设置岗位和部门
- 设置薪资信息
- 实名认证状态
- 就职日期选择
- 表单验证

### 7. `src/components/drawers/EmployeeDrawer.vue` - 员工详情

实现功能：
- 显示员工基本信息
- 展示员工绩效数据
- 显示接待顾客数
- 显示提成统计
- 显示订单记录
- 操作按钮

---

## 数据统计模块

### 8. `src/pages/Statistics.vue` - 统计分析页面

实现功能：
- 日期范围选择
- 时间对比（今天、昨天、本周、本月、自定义）
- 收入统计图表
  - 日收入趋势线图
  - 周收入对比柱状图
  - 月度累计收入
- 客流量统计
  - 日客流量趋势
  - 新增顾客统计
- 渠道分析
  - 各渠道销售额占比饼图
  - 各渠道订单数对比
  - 各渠道转化率
- 员工排行
  - 销售额排行TOP 10
  - 接待客户数排行
  - 提成排行
- 产品销售
  - 销售量TOP 10
  - 销售额TOP 10
  - 产品类别销售分布
- 数据导出（多种格式）

### 9-13. 图表组件

- `src/components/charts/DailyRevenueChart.vue` - 日收入趋势
- `src/components/charts/WeeklyComparisonChart.vue` - 周对比
- `src/components/charts/TrafficChart.vue` - 客流量统计
- `src/components/charts/ChannelAnalysisChart.vue` - 渠道分析
- `src/components/charts/EmployeeRankingTable.vue` - 员工排行表

---

## 产品管理相关对话框

### 14. `src/components/dialogs/ProductDialog.vue` - 产品新增/编辑

实现功能：
- 输入产品基本信息（名称、描述、规格）
- 选择分类
- 设置价格（会员价、非会员价、成本价）
- 上传产品图片
- 设置库存信息
- 表单验证

### 15. `src/components/dialogs/CategoryDialog.vue` - 分类管理

实现功能：
- 分类列表展示
- 新增分类
- 编辑分类
- 删除分类
- 分类排序

### 16. `src/components/dialogs/StockDialog.vue` - 库存调整

实现功能：
- 显示当前库存
- 输入调整数量
- 选择调整原因（入库、出库、盘点等）
- 库存记录历史

---

## 通用公共组件

### 17. `src/components/Table.vue` - 数据表格组件

功能：
- 列配置（类型、宽度、格式化）
- 分页
- 排序
- 过滤
- 多选
- 展开行
- 自定义操作列

### 18. `src/components/SearchForm.vue` - 搜索表单组件

功能：
- 动态表单字段生成
- 搜索、重置、高级搜索
- 查询条件记忆
- 快速筛选器

### 19. `src/components/Pagination.vue` - 分页组件

功能：
- 自定义页码数
- 自定义每页数量
- 总数显示
- 跳页功能

### 20. `src/components/Modal.vue` - 模态框组件

功能：
- 标题和内容插槽
- 页脚按钮定制
- 加载状态
- 宽度自定义

### 21. `src/components/ConfirmDialog.vue` - 确认对话框

功能：
- 确认/取消按钮
- 警告/错误/成功三种类型
- 自定义文本

### 22. `src/components/Upload.vue` - 文件上传组件

功能：
- 单文件/多文件上传
- 文件类型验证
- 大小限制
- 进度展示
- 拖拽上传

---

## 样式和主题

### 23. `src/styles/variables.scss` - CSS 变量定义

```scss
// 颜色
$primary-color: #409eff;
$success-color: #67c23a;
$warning-color: #e6a23c;
$danger-color: #f56c6c;
$info-color: #909399;

// 尺寸
$border-radius: 4px;
$transition-duration: 0.3s;

// 阴影
$box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
```

### 24. `src/styles/global.scss` - 全局样式

- 重置浏览器默认样式
- 公共样式定义
- Element Plus 主题覆盖
- 响应式布局辅助

### 25. `src/styles/mixins.scss` - SCSS 混合函数

```scss
// 弹性布局快捷方式
@mixin flex-center

// 文字截断
@mixin text-truncate

// 响应式媒体查询
@mixin respond-to

// 其他常用混合
```

---

## 其他页面

### 26. `src/pages/Profile.vue` - 个人资料页面

实现功能：
- 显示个人信息
- 编辑个人资料
- 修改密码
- 头像上传

### 27. `src/pages/Settings.vue` - 系统设置页面

实现功能：
- 店铺基本信息设置
- 营业时间设置
- 通知设置
- 系统权限管理
- 备份和恢复

---

## 高级功能（可选）

### 28. 权限管理系统
- 角色定义
- 权限分配
- 功能可见性控制

### 29. 数据导出系统
- Excel 导出
- PDF 导出
- CSV 导出

### 30. 打印功能
- 订单打印
- 报表打印
- 标签打印

### 31. 消息通知系统
- WebSocket 实时通知
- 消息列表管理
- 消息标记已读

### 32. 操作审计日志
- 用户操作记录
- 数据变更记录
- 操作追溯

---

## 开发优先级

### P0 优先（立即开始）
1. 订单管理页面（Orders.vue、OrderDialog.vue）
2. 员工管理页面（Employees.vue、EmployeeDialog.vue）
3. 数据统计页面（Statistics.vue）
4. 产品对话框（ProductDialog.vue、CategoryDialog.vue）

### P1 优先（紧接着）
1. 通用公共组件
2. 样式文件
3. 详情抽屉组件（OrderDrawer、EmployeeDrawer）
4. 统计图表组件

### P2 优先（之后）
1. 其他页面（Profile、Settings）
2. 高级功能
3. 测试用例
4. 文档完善

---

## 预计工作量

| 任务 | 预计时间 | 优先级 |
|-----|--------|------|
| 订单管理模块 | 4小时 | P0 |
| 员工管理模块 | 3小时 | P0 |
| 数据统计模块 | 5小时 | P0 |
| 产品对话框 | 2小时 | P0 |
| 公共组件库 | 4小时 | P1 |
| 样式系统 | 2小时 | P1 |
| 详情抽屉 | 3小时 | P1 |
| 其他页面 | 2小时 | P2 |
| 高级功能 | 8小时 | P2 |
| 测试和优化 | 6小时 | P2 |
| **总计** | **~40小时** | |

---

## 开发检查清单

### 代码质量
- [ ] 遵循 Vue 3 Composition API 最佳实践
- [ ] 使用 TypeScript（可选但推荐）
- [ ] 代码注释完整
- [ ] 错误处理完善
- [ ] 加载状态处理

### 用户体验
- [ ] 响应式设计
- [ ] 加载动画
- [ ] 错误提示
- [ ] 成功反馈
- [ ] 键盘快捷键支持

### 性能优化
- [ ] 代码分割
- [ ] 图片优化
- [ ] 缓存策略
- [ ] 虚拟列表（大数据）
- [ ] 防抖/节流

### 安全性
- [ ] 防止 XSS
- [ ] 防止 CSRF
- [ ] 输入验证
- [ ] 数据加密
- [ ] 权限检查

---

**最后更新**: 2026-01-28
**建议完成时间**: 1-2周
