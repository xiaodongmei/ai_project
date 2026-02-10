# 贡献指南

感谢你有兴趣为养生店管理系统做出贡献！本文档指导你如何参与项目开发。

## 目录

1. [行为准则](#行为准则)
2. [开始贡献](#开始贡献)
3. [开发工作流](#开发工作流)
4. [代码规范](#代码规范)
5. [提交 Pull Request](#提交-pull-request)
6. [报告 Bug](#报告-bug)
7. [建议新功能](#建议新功能)
8. [文档贡献](#文档贡献)

---

## 行为准则

### 我们的承诺

为了营造一个开放、友好、包容的社区，我们承诺：

- 尊重所有参与者，无论其身份、背景或经验
- 对建设性的批评和不同意见持开放态度
- 专注于对社区最有益的讨论
- 对社区成员的言行负责

### 不可接受的行为

以下行为在社区中不可接受：

- 骚扰、辱骂或威胁他人
- 发布他人的私人信息
- 发表不尊重、轻蔑或贬低的评论
- 任何其他可能被合理地认为在职业环境中不适当的行为

### 举报流程

如遇到不可接受的行为，请通过以下方式举报：

- 发送邮件至：developers@wellness-shop.com
- 在 GitHub 上提交私密问题
- 联系项目维护者

我们致力于快速、公正地处理所有举报。

---

## 开始贡献

### 贡献的方式

1. **代码贡献**
   - 修复 Bug
   - 实现新功能
   - 改进现有代码
   - 性能优化

2. **文档贡献**
   - 改进 README
   - 添加使用示例
   - 翻译文档
   - 修正文档错误

3. **测试贡献**
   - 编写单元测试
   - 编写集成测试
   - 报告测试遗漏

4. **反馈贡献**
   - 报告 Bug
   - 建议功能改进
   - 性能问题报告

### 前置条件

- Git 基础知识
- Python 3.9+（后端开发）
- Node.js 16+（前端开发）
- GitHub 账户

---

## 开发工作流

### 1. Fork 项目

在 GitHub 上 Fork 项目到你的账户。

```bash
# 点击 Fork 按钮
# https://github.com/username/wellness-shop-system
```

### 2. Clone 仓库

```bash
# 克隆你的 Fork
git clone https://github.com/your-username/wellness-shop-system.git
cd wellness-shop-system

# 添加上游仓库
git remote add upstream https://github.com/original/wellness-shop-system.git
```

### 3. 创建特性分支

```bash
# 更新本地 main 分支
git fetch upstream
git checkout main
git merge upstream/main

# 创建新分支
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
# 或
git checkout -b docs/your-docs-improvement
```

**分支命名规范：**
- `feature/` - 新功能
- `fix/` - Bug 修复
- `docs/` - 文档改进
- `refactor/` - 代码重构
- `test/` - 测试相关
- `perf/` - 性能优化
- `chore/` - 构建、配置等

### 4. 进行更改

编写代码并遵循项目的代码规范（见下节）。

### 5. 测试更改

```bash
# 后端测试
cd backend
python -m pytest tests/

# 前端测试
cd frontend
npm run test

# 代码质量检查
# 详见代码规范部分
```

### 6. Commit 更改

遵循 Conventional Commits 规范：

```bash
git add .
git commit -m "type(scope): subject

body (optional)

footer (optional)"
```

**类型：**
- `feat` - 新功能
- `fix` - Bug 修复
- `docs` - 文档
- `style` - 代码风格（无逻辑变化）
- `refactor` - 代码重构
- `perf` - 性能优化
- `test` - 测试
- `chore` - 构建、依赖等

**示例：**
```bash
git commit -m "feat(auth): add two-factor authentication

- Implement TOTP support
- Add QR code generation
- Update user schema

Closes #123"
```

### 7. 推送到 Fork

```bash
git push origin feature/your-feature-name
```

### 8. 提交 Pull Request

在 GitHub 上提交 PR，详见 [提交 Pull Request](#提交-pull-request)。

---

## 代码规范

### Python 代码规范（后端）

#### 格式化

使用 Black 进行代码格式化：

```bash
# 安装 Black
pip install black

# 格式化单个文件
black app/models/customer.py

# 格式化整个目录
black app/

# 检查格式（不修改）
black --check app/
```

#### Linting

使用 Flake8 进行代码检查：

```bash
# 安装 Flake8
pip install flake8

# 检查代码
flake8 app/

# 检查并忽略某些规则
flake8 app/ --ignore=E501,W503
```

#### Import 排序

使用 isort 整理导入：

```bash
# 安装 isort
pip install isort

# 整理导入
isort app/

# 检查
isort --check-only app/
```

#### 代码示例

```python
"""Module docstring explaining the purpose."""

from typing import Optional, List
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/")
async def list_customers(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Get list of customers.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session

    Returns:
        Dictionary with customers list
    """
    # Implementation
    pass


def validate_email(email: str) -> bool:
    """Validate email format."""
    import re
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None
```

**规范要点：**
- 遵循 PEP 8
- 使用类型注解
- 添加文档字符串
- 最大行长 88 字符（Black 默认）
- 使用有意义的变量名
- 注释应说明"为什么"而非"做什么"

### JavaScript/Vue 代码规范（前端）

#### ESLint 配置

```bash
# 检查代码
npm run lint

# 自动修复
npm run lint -- --fix
```

#### 代码示例

```javascript
/**
 * Customer management module
 */

import { defineComponent } from 'vue';
import { useCustomerStore } from '@/store/customer';
import CustomerForm from '@/components/CustomerForm.vue';

export default defineComponent({
  name: 'CustomerPage',
  components: {
    CustomerForm,
  },
  setup() {
    const customerStore = useCustomerStore();

    const handleCreate = async (formData) => {
      try {
        await customerStore.createCustomer(formData);
        // Show success message
      } catch (error) {
        // Show error message
      }
    };

    return {
      handleCreate,
    };
  },
});
```

**规范要点：**
- 使用 Composition API
- 使用 camelCase 命名变量和函数
- 使用 PascalCase 命名组件
- 添加 JSDoc 注释
- 最多一个组件每个文件

### 通用规范

#### 注释

```python
# 不好：说明了做什么
x = x + 1  # Increment x by 1

# 好：说明了为什么
# 用户点击按钮时需要增加计数
counter += 1
```

#### 命名规范

```python
# 常量（全大写）
MAX_RETRIES = 3
DATABASE_URL = "..."

# 类（帕斯卡尔命名法）
class CustomerManager:
    pass

# 函数和变量（蛇形命名法）
def get_customer_by_id(customer_id: int):
    pass

total_amount = 0
```

#### 函数和方法

```python
def process_order(
    order_id: int,
    customer_id: int,
    force: bool = False,
) -> dict:
    """
    Process an order.

    Args:
        order_id: The ID of the order to process
        customer_id: The customer's ID
        force: Whether to force processing (default: False)

    Returns:
        Dictionary with processing result

    Raises:
        ValueError: If order not found
        PermissionError: If user lacks permission
    """
    pass
```

---

## 提交 Pull Request

### PR 模板

```markdown
## Description
简要描述你的改动内容。

## Related Issues
关联的 Issue：#123

## Changes Made
- [ ] 修复功能 X
- [ ] 添加功能 Y
- [ ] 更新文档

## Testing
- [ ] 添加/更新了单元测试
- [ ] 添加/更新了集成测试
- [ ] 本地测试通过

## Screenshots（如果适用）
添加相关的截图

## Breaking Changes
描述任何重大变化（如有）

## Checklist
- [ ] 代码遵循项目风格指南
- [ ] 文档已更新
- [ ] 没有产生新的警告
- [ ] 添加了适当的测试
- [ ] 测试通过
```

### PR 检查清单

提交 PR 前，请确保：

- [ ] 分支基于最新的 `main`
- [ ] 提交信息清晰、准确
- [ ] 代码通过格式化检查
- [ ] 没有新的 Lint 警告
- [ ] 测试全部通过
- [ ] 代码覆盖率未降低
- [ ] 文档已更新
- [ ] 没有合并冲突

### PR 审核流程

1. 至少一名维护者审核
2. 通过所有自动化检查
3. 地址审核意见
4. 获批后合并

---

## 报告 Bug

### Bug 报告模板

```markdown
## 描述 Bug
清晰、简洁地描述 Bug 是什么。

## 复现步骤
1. 进入 '...'
2. 点击 '...'
3. 向下滚动到 '...'
4. 看到错误

## 预期行为
描述你期望发生的行为。

## 实际行为
描述实际发生了什么。

## 环境
- OS: [例如 macOS 12.1]
- 浏览器: [例如 Chrome 96]
- 版本: [例如 1.0.0]
- Python 版本: [例如 3.10]
- Node 版本: [例如 16.13]

## 日志和错误信息
粘贴相关的日志或错误信息。

## 附加上下文
其他可能有帮助的信息。
```

### 报告 Bug 的最佳实践

- **标题清晰**: "登录失败" ❌ vs "输入非 ASCII 字符时登录按钮不可用" ✅
- **提供最小复现**: 尽可能简化步骤
- **查看已存在的 Issues**: 避免重复报告
- **包含环境信息**: OS、浏览器、版本等
- **附加日志**: 错误堆栈跟踪很有帮助

---

## 建议新功能

### 功能建议模板

```markdown
## 功能描述
简要描述你想要的功能。

## 问题陈述
这个功能解决什么问题？

## 建议的解决方案
你建议如何实现？

## 替代方案
是否有其他方式实现？

## 附加上下文
其他背景信息。
```

### 建议功能的最佳实践

- 搜索已存在的功能请求
- 解释为什么这个功能有用
- 提供具体的用例
- 考虑实现的复杂性

---

## 文档贡献

### 文档风格指南

#### 标题

使用 Markdown 标题层级：

```markdown
# 主标题（H1）
## 次级标题（H2）
### 小节（H3）
```

#### 代码块

使用代码块并指定语言：

````markdown
```python
def hello():
    print("Hello, World!")
```

```bash
npm install
```
````

#### 链接

```markdown
[链接文本](https://example.com)
[相对链接](./path/to/file.md)
```

#### 列表

```markdown
- 无序项目 1
- 无序项目 2

1. 有序项目 1
2. 有序项目 2
```

#### 表格

```markdown
| 列 1 | 列 2 | 列 3 |
|------|------|------|
| 数据 | 数据 | 数据 |
```

### 文档位置

- 用户文档：`/docs/user-guide/`
- API 文档：`API_DOCUMENTATION.md`
- 开发文档：`DEVELOPMENT.md`
- 部署文档：`DEPLOYMENT.md`
- 项目说明：`README.md`

---

## 开发环境设置

### 后端开发环境

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 安装 pre-commit hooks
pre-commit install

# 运行测试
pytest

# 启动开发服务器
uvicorn app.main:app --reload
```

### 前端开发环境

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 运行测试
npm run test

# 检查代码
npm run lint
```

---

## 获取帮助

### 资源

- **文档**: 查看 `/docs` 目录
- **示例**: 查看 `examples/` 目录
- **讨论**: GitHub Discussions
- **邮件**: developers@wellness-shop.com

### 联系方式

- **Issues**: GitHub Issues（技术问题）
- **邮件**: contact@wellness-shop.com
- **Discord**: [加入我们的 Discord](https://discord.gg/xxxxx)

---

## 贡献者们

感谢所有为此项目做出贡献的人！

---

## 许可证

通过贡献代码，你同意在与项目相同的许可证下发布你的贡献（MIT License）。

---

**最后更新:** 2024年1月
**版本:** 1.0.0
