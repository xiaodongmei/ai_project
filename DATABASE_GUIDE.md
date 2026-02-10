# 数据库指南

完整的数据库初始化、迁移和管理指南。

## 目录

1. [快速开始](#快速开始)
2. [数据库架构](#数据库架构)
3. [初始化数据库](#初始化数据库)
4. [Alembic 迁移](#alembic-迁移)
5. [数据备份与恢复](#数据备份与恢复)
6. [性能优化](#性能优化)
7. [常见问题](#常见问题)

---

## 快速开始

### 前置要求

- PostgreSQL 13+
- Python 3.9+
- SQLAlchemy 2.0+
- Alembic 1.13+

### 初始化步骤

```bash
# 1. 创建数据库
createdb wellness_shop

# 2. 运行初始化脚本
cd backend
python init_db.py

# 3. 验证初始化
psql wellness_shop -c "\dt"
```

---

## 数据库架构

### 数据库设计原则

- **规范化**: 遵循第三范式
- **一致性**: 使用外键约束
- **可扩展性**: 预留扩展字段
- **性能**: 适当的索引和分区

### 核心表

#### 1. users（用户表）

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'customer',
    is_active BOOLEAN DEFAULT true,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**字段说明：**
- `id`: 主键，自增
- `username`: 用户名，唯一
- `email`: 邮箱，唯一，用于验证
- `password_hash`: 密码哈希（bcrypt）
- `role`: 用户角色（admin, manager, employee, customer）
- `is_active`: 账户是否激活
- `last_login`: 最后登录时间

**索引：**
```sql
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
```

#### 2. customers（顾客表）

```sql
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) UNIQUE,
    email VARCHAR(100) UNIQUE,
    membership_status VARCHAR(20) DEFAULT 'regular',
    membership_level VARCHAR(20),
    points DECIMAL(10, 2) DEFAULT 0,
    total_consumption DECIMAL(10, 2) DEFAULT 0,
    address TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**字段说明：**
- `membership_status`: 会员状态（regular, vip, platinum）
- `points`: 积分（用于兑换）
- `total_consumption`: 总消费金额

**索引：**
```sql
CREATE INDEX idx_customers_phone ON customers(phone);
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_membership_status ON customers(membership_status);
```

#### 3. products（产品表）

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    member_price DECIMAL(10, 2),
    cost_price DECIMAL(10, 2),
    stock INTEGER DEFAULT 0,
    reorder_level INTEGER DEFAULT 10,
    status VARCHAR(20) DEFAULT 'active',
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**字段说明：**
- `category`: 产品分类（massage, treatment, product等）
- `member_price`: 会员价格
- `cost_price`: 成本价格
- `reorder_level`: 库存预警值
- `status`: 产品状态（active, inactive, discontinued）

**索引：**
```sql
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_status ON products(status);
CREATE INDEX idx_products_stock ON products(stock) WHERE stock < reorder_level;
```

#### 4. orders（订单表）

```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    employee_id INTEGER REFERENCES employees(id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivery_date TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    discount_amount DECIMAL(10, 2) DEFAULT 0,
    final_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    payment_method VARCHAR(20),
    payment_status VARCHAR(20) DEFAULT 'unpaid',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**状态流转：**
```
pending → processing → completed
  ↓
  └─→ cancelled
```

**索引：**
```sql
CREATE INDEX idx_orders_order_number ON orders(order_number);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_orders_payment_status ON orders(payment_status);
```

#### 5. order_items（订单项目表）

```sql
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**索引：**
```sql
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
```

#### 6. employees（员工表）

```sql
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(100) NOT NULL,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    department VARCHAR(50),
    position VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(100),
    hire_date DATE,
    status VARCHAR(20) DEFAULT 'active',
    salary DECIMAL(10, 2),
    commission_rate DECIMAL(5, 3) DEFAULT 0.1,
    performance_rating DECIMAL(3, 1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**索引：**
```sql
CREATE INDEX idx_employees_employee_id ON employees(employee_id);
CREATE INDEX idx_employees_department ON employees(department);
CREATE INDEX idx_employees_status ON employees(status);
```

#### 7. payments（支付表）

```sql
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    payment_method VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    transaction_id VARCHAR(100) UNIQUE,
    payment_date TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**索引：**
```sql
CREATE INDEX idx_payments_order_id ON payments(order_id);
CREATE INDEX idx_payments_transaction_id ON payments(transaction_id);
CREATE INDEX idx_payments_status ON payments(status);
```

### 表关系图

```
users
├── employees (user_id FK)
├── customers (user_id FK)
│   └── orders (customer_id FK)
│       ├── order_items (order_id FK)
│       │   └── products (product_id FK)
│       └── payments (order_id FK)
│
└── products

employees (id) → orders (employee_id)
```

---

## 初始化数据库

### 使用初始化脚本

```bash
# 进入后端目录
cd backend

# 运行初始化脚本
python init_db.py
```

**脚本执行内容：**
1. 创建数据库（如果不存在）
2. 创建所有表
3. 创建索引
4. 插入初始数据（可选）

### 手动初始化

```bash
# 1. 连接到 PostgreSQL
psql -U postgres

# 2. 创建数据库
CREATE DATABASE wellness_shop;

# 3. 连接到新数据库
\c wellness_shop

# 4. 创建表（运行 SQL 脚本）
\i path/to/schema.sql
```

### 初始化数据

```bash
# 添加默认管理员用户
python -c "
from app.db.base import create_admin_user
create_admin_user(
    username='admin',
    password='admin123',
    email='admin@example.com'
)
"
```

---

## Alembic 迁移

### 什么是 Alembic？

Alembic 是 SQLAlchemy 的数据库迁移工具，用于：
- 版本控制数据库结构
- 自动生成迁移脚本
- 升级和回滚数据库

### 初始化 Alembic

```bash
# 初始化 alembic
alembic init alembic

# 配置 alembic.ini
# 设置 sqlalchemy.url = postgresql://user:password@localhost/wellness_shop
```

### 生成迁移脚本

```bash
# 自动生成迁移脚本（检测模型变化）
alembic revision --autogenerate -m "add new column"

# 手动创建迁移脚本
alembic revision -m "custom migration message"
```

### 迁移脚本示例

```python
"""Add membership_level to customers

Revision ID: abc123def456
Revises: xyz789uvw012
Create Date: 2024-01-16 10:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = 'abc123def456'
down_revision = 'xyz789uvw012'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """升级数据库结构"""
    op.add_column(
        'customers',
        sa.Column('membership_level', sa.String(20), nullable=True)
    )
    op.create_index(
        'idx_customers_membership_level',
        'customers',
        ['membership_level']
    )


def downgrade() -> None:
    """回滚数据库结构"""
    op.drop_index('idx_customers_membership_level', 'customers')
    op.drop_column('customers', 'membership_level')
```

### 应用迁移

```bash
# 查看当前版本
alembic current

# 升级到最新版本
alembic upgrade head

# 升级指定版本
alembic upgrade <revision>

# 升级 N 个版本
alembic upgrade +2

# 查看迁移历史
alembic history

# 查看待应用的迁移
alembic history -r -2:head
```

### 回滚迁移

```bash
# 回滚到上一个版本
alembic downgrade -1

# 回滚指定版本
alembic downgrade <revision>

# 回滚 N 个版本
alembic downgrade -2

# 回滚所有迁移
alembic downgrade base
```

### 迁移最佳实践

1. **每个迁移应是原子的**
   - 一个迁移完成一个逻辑任务
   - 避免复杂的组合迁移

2. **测试迁移脚本**
   ```bash
   # 在测试数据库上测试
   alembic upgrade head -x testdb=True
   ```

3. **添加数据迁移**
   ```python
   def upgrade():
       # 添加新字段
       op.add_column('customers', sa.Column('status', sa.String(20)))

       # 更新现有数据
       connection = op.get_bind()
       connection.execute(
           "UPDATE customers SET status = 'active' WHERE id > 0"
       )
   ```

4. **版本控制**
   - 在 Git 中跟踪迁移文件
   - 不要修改已应用的迁移
   - 新增迁移用于修改

---

## 数据备份与恢复

### 备份数据库

#### 完整备份

```bash
# 使用 pg_dump 备份
pg_dump -h localhost -U postgres wellness_shop > backup.sql

# 备份为自定义格式（压缩）
pg_dump -h localhost -U postgres -Fc wellness_shop > backup.dump

# 仅备份数据（不包括结构）
pg_dump -h localhost -U postgres -a wellness_shop > data_only.sql

# 仅备份结构（不包括数据）
pg_dump -h localhost -U postgres -s wellness_shop > schema_only.sql
```

#### Docker 环境备份

```bash
# 备份 Docker 中的数据库
docker-compose exec postgres pg_dump -U postgres wellness_shop > backup.sql

# 备份为压缩格式
docker-compose exec postgres pg_dump -U postgres -Fc wellness_shop > backup.dump
```

#### 自动备份脚本

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/wellness-shop"
DB_NAME="wellness_shop"
DB_USER="postgres"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR

# 执行备份
pg_dump -U $DB_USER -Fc $DB_NAME > $BACKUP_DIR/db_$DATE.dump

# 压缩备份
gzip $BACKUP_DIR/db_$DATE.dump

# 删除 30 天前的备份
find $BACKUP_DIR -type f -mtime +30 -delete

echo "Backup completed: $BACKUP_DIR/db_$DATE.dump.gz"
```

### 恢复数据库

#### 从 SQL 文件恢复

```bash
# 恢复完整数据库
psql -h localhost -U postgres wellness_shop < backup.sql

# 恢复到空数据库（推荐）
dropdb wellness_shop
createdb wellness_shop
psql -h localhost -U postgres wellness_shop < backup.sql
```

#### 从自定义格式恢复

```bash
# 恢复 .dump 文件
pg_restore -h localhost -U postgres -d wellness_shop backup.dump

# 恢复前清空数据库
dropdb wellness_shop
createdb wellness_shop
pg_restore -h localhost -U postgres -d wellness_shop backup.dump
```

#### Docker 环境恢复

```bash
# 恢复数据库
docker-compose exec -T postgres psql -U postgres wellness_shop < backup.sql

# 从压缩文件恢复
gunzip -c backup.dump.gz | docker-compose exec -T postgres pg_restore -U postgres -d wellness_shop -
```

#### 选择性恢复

```bash
# 仅恢复特定表
pg_restore -h localhost -U postgres -d wellness_shop -t customers backup.dump

# 恢复多个表
pg_restore -h localhost -U postgres -d wellness_shop -t customers -t orders backup.dump

# 排除特定表
pg_restore -h localhost -U postgres -d wellness_shop -T logs backup.dump
```

### 备份验证

```bash
# 查看备份内容
pg_restore -l backup.dump | head -20

# 测试恢复（恢复到临时数据库）
createdb wellness_shop_test
pg_restore -h localhost -U postgres -d wellness_shop_test backup.dump

# 比较备份数据库和主数据库
diff <(psql wellness_shop -c "SELECT * FROM customers ORDER BY id") \
     <(psql wellness_shop_test -c "SELECT * FROM customers ORDER BY id")

# 清理测试数据库
dropdb wellness_shop_test
```

---

## 性能优化

### 索引优化

```sql
-- 查看缺失的索引
SELECT * FROM pg_stat_user_tables
WHERE schemaname = 'public'
AND seq_tup_read > 0;

-- 创建索引
CREATE INDEX idx_customers_created_at ON customers(created_at DESC);

-- 复合索引（用于频繁的联合查询）
CREATE INDEX idx_orders_customer_status ON orders(customer_id, status);

-- 部分索引（仅索引活跃的记录）
CREATE INDEX idx_orders_active ON orders(id) WHERE status != 'cancelled';

-- 检查索引使用情况
SELECT * FROM pg_stat_user_indexes ORDER BY idx_scan DESC;
```

### 查询优化

```sql
-- 使用 EXPLAIN ANALYZE 分析查询计划
EXPLAIN ANALYZE
SELECT c.*, COUNT(o.id) as order_count
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE c.membership_status = 'vip'
GROUP BY c.id;

-- 查看慢查询日志
ALTER SYSTEM SET log_min_duration_statement = 1000;
SELECT pg_reload_conf();

-- 获取慢查询
SELECT * FROM pg_stat_statements
ORDER BY mean_time DESC LIMIT 10;
```

### 表空间优化

```sql
-- 查看表大小
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- 查看索引大小
SELECT indexname, pg_size_pretty(pg_relation_size(indexrelid))
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC;

-- 清理死行（VACUUM）
VACUUM ANALYZE;

-- 重新组织表（REINDEX）
REINDEX TABLE customers;
```

### 连接池

```bash
# 配置 PgBouncer 连接池
# pgbouncer.ini

[databases]
wellness_shop = host=localhost port=5432 dbname=wellness_shop

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
min_pool_size = 10
reserve_pool_size = 5
```

---

## 常见问题

### Q: 如何修改现有表结构？

```bash
# 1. 生成迁移脚本
alembic revision --autogenerate -m "modify column name"

# 2. 检查生成的脚本
nano alembic/versions/<version>_modify_column_name.py

# 3. 应用迁移
alembic upgrade head
```

### Q: 如何添加新表？

```bash
# 1. 在 models 中定义新表
# app/models/new_table.py

from app.db.base import Base, IDMixin, TimestampMixin

class NewTable(Base, IDMixin, TimestampMixin):
    __tablename__ = "new_tables"
    # 定义字段...

# 2. 生成迁移
alembic revision --autogenerate -m "add new_table"

# 3. 应用迁移
alembic upgrade head
```

### Q: 备份出错：pg_dump: error: aborting restore?

```bash
# 使用 verbose 模式查看详细错误
pg_dump -h localhost -U postgres --verbose wellness_shop > backup.sql 2>&1 | tee backup.log

# 忽略错误继续恢复
pg_restore --on-error-continue -d wellness_shop backup.dump
```

### Q: 如何监控数据库性能？

```bash
# 查看活跃连接
SELECT datname, count(*) FROM pg_stat_activity GROUP BY datname;

# 查看锁定的进程
SELECT * FROM pg_locks WHERE NOT granted;

# 查看缓存命中率
SELECT
    sum(heap_blks_read) as heap_read,
    sum(heap_blks_hit) as heap_hit,
    sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) as ratio
FROM pg_statio_user_tables;
```

---

## 参考资源

- [PostgreSQL 官方文档](https://www.postgresql.org/docs/)
- [SQLAlchemy ORM 教程](https://docs.sqlalchemy.org/en/20/orm/)
- [Alembic 文档](https://alembic.sqlalchemy.org/)
- [PostgreSQL 性能优化](https://www.postgresql.org/docs/current/performance-tips.html)

---

**最后更新:** 2024年1月
**版本:** 1.0.0
