# 前端测试指南

## 📋 前端测试框架

### 安装 Vitest

```bash
cd frontend
npm install --save-dev vitest happy-dom @vitest/ui
```

### 已实现的测试

#### 1. 单元测试 (Unit Tests)

**API 客户端测试**
- `src/__tests__/unit/api/client.spec.js` - HTTP 客户端和拦截器 (9个测试)

**工具函数测试**
- `src/__tests__/unit/utils/date.spec.js` - 日期工具函数 (11个测试)

**状态管理测试**
- `src/__tests__/unit/store/user.spec.js` - Pinia 用户存储 (12个测试)

**单元测试总数**: 32个测试

#### 2. 集成测试 (Integration Tests)

**路由测试**
- `src/__tests__/integration/router.spec.js` - Vue Router 导航和守卫 (13个测试)

**集成测试总数**: 13个测试

---

## 🚀 运行测试

### 更新 package.json

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext .vue,.js,.jsx,.cjs,.mjs --fix --ignore-path .gitignore",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  }
}
```

### 运行所有测试

```bash
npm run test
```

### 运行特定测试文件

```bash
# 运行 API 客户端测试
npm run test -- src/__tests__/unit/api/client.spec.js

# 运行所有单元测试
npm run test -- src/__tests__/unit/

# 运行所有集成测试
npm run test -- src/__tests__/integration/
```

### 运行特定测试

```bash
# 运行包含 "should" 的测试
npm run test -- --grep "should"

# 运行某个测试套件
npm run test -- --grep "HTTP Client"
```

### 生成覆盖率报告

```bash
# 基本覆盖率报告
npm run test:coverage

# 生成详细的 HTML 报告
npm run test:coverage -- --reporter=html
```

### 监视模式

```bash
# 自动运行测试（当文件改变时）
npm run test -- --watch
```

### UI 模式

```bash
# 在浏览器中查看测试结果
npm run test:ui
```

---

## 📝 测试文件结构

```
frontend/src/
├── __tests__/
│   ├── setup.js                    # 测试全局设置
│   ├── unit/
│   │   ├── api/
│   │   │   └── client.spec.js      # HTTP 客户端测试
│   │   ├── utils/
│   │   │   └── date.spec.js        # 日期工具测试
│   │   ├── store/
│   │   │   └── user.spec.js        # 用户 store 测试
│   │   └── components/
│   │       ├── MetricCard.spec.js
│   │       ├── RevenueChart.spec.js
│   │       └── *.spec.js
│   └── integration/
│       ├── router.spec.js          # 路由集成测试
│       ├── auth.spec.js            # 认证流程测试
│       └── workflows.spec.js       # 业务流程测试
├── api/
├── components/
├── pages/
├── router/
├── store/
└── utils/
```

---

## 🧪 编写测试

### 基本测试结构

```javascript
import { describe, it, expect } from 'vitest'

describe('Feature Name', () => {
  it('should do something', () => {
    expect(1 + 1).toBe(2)
  })

  it('should handle error', () => {
    expect(() => {
      throw new Error('Test')
    }).toThrow('Test')
  })
})
```

### 异步测试

```javascript
import { describe, it, expect, beforeEach, afterEach } from 'vitest'

describe('Async Operations', () => {
  beforeEach(() => {
    // 测试前执行
  })

  afterEach(() => {
    // 测试后执行
  })

  it('should handle promises', async () => {
    const result = await Promise.resolve('data')
    expect(result).toBe('data')
  })

  it('should handle async/await', async () => {
    const fetchData = async () => {
      return 'async-data'
    }
    const data = await fetchData()
    expect(data).toBe('async-data')
  })
})
```

### Mock 和 Spy

```javascript
import { describe, it, expect, vi } from 'vitest'

describe('Mocking', () => {
  it('should mock functions', () => {
    const mockFn = vi.fn()
    mockFn('arg1', 'arg2')

    expect(mockFn).toHaveBeenCalled()
    expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2')
  })

  it('should mock return value', () => {
    const mockFn = vi.fn().mockReturnValue('mocked')
    expect(mockFn()).toBe('mocked')
  })

  it('should mock module', async () => {
    vi.mock('axios', () => ({
      default: {
        get: vi.fn(),
      },
    }))
  })
})
```

### 组件测试

```javascript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import MyComponent from '@/components/MyComponent.vue'

describe('MyComponent', () => {
  it('should render', () => {
    const wrapper = mount(MyComponent)
    expect(wrapper.exists()).toBe(true)
  })

  it('should accept props', () => {
    const wrapper = mount(MyComponent, {
      props: {
        title: 'Test Title',
      },
    })
    expect(wrapper.props('title')).toBe('Test Title')
  })

  it('should emit events', async () => {
    const wrapper = mount(MyComponent)
    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted('click')).toBeTruthy()
  })
})
```

---

## 📊 覆盖率目标

| 模块 | 目标覆盖率 | 状态 |
|------|----------|------|
| API Clients | >= 90% | 待测量 |
| Utils | >= 85% | 待测量 |
| Store | >= 90% | 待测量 |
| Components | >= 75% | 待测量 |
| Routers | >= 90% | 待测量 |
| **总体** | **>= 75%** | **待测量** |

---

## 🔧 故障排除

### 导入错误

```javascript
// 使用 @ 别名
import MyComponent from '@/components/MyComponent.vue'

// 而不是
import MyComponent from '../../../components/MyComponent.vue'
```

### localStorage 错误

```javascript
// Mock localStorage（已在 setup.js 中配置）
global.localStorage = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
}
```

### 异步超时

```javascript
// 增加超时时间
it('should fetch data', async () => {
  // ...
}, 10000) // 10 秒超时
```

---

## 📚 参考资源

### Vitest
- [Vitest 官方文档](https://vitest.dev/)
- [Vitest API](https://vitest.dev/api/)

### Vue Test Utils
- [Vue Test Utils 文档](https://test-utils.vuejs.org/)

### Testing Best Practices
- [Testing Library](https://testing-library.com/)
- [Vue Testing 最佳实践](https://vuejs.org/guide/scaling-up/testing.html)

---

## 📈 下一步待实现

### 需要添加的测试

1. **组件单元测试**
   - `MetricCard.spec.js`
   - `RevenueChart.spec.js`
   - `ChannelChart.spec.js`
   - `CustomerDialog.spec.js`
   - 其他组件

2. **页面测试**
   - `Login.spec.js`
   - `Dashboard.spec.js`
   - `Customers.spec.js`
   - `Products.spec.js`

3. **API 端点测试**
   - `customer-api.spec.js`
   - `product-api.spec.js`
   - `order-api.spec.js`
   - `auth-api.spec.js`

4. **更多集成测试**
   - `auth-flow.spec.js` - 认证流程
   - `customer-flow.spec.js` - 顾客管理流程
   - `order-flow.spec.js` - 订单流程

5. **E2E 测试**（可选）
   - 使用 Playwright 或 Cypress
   - 完整用户场景测试

---

**最后更新**: 2026-01-28
**作者**: DeepV Code AI
**状态**: 前端测试框架已搭建
