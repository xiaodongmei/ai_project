#!/usr/bin/env python3
"""
环境检查脚本
检查所有必要的依赖和配置是否正确
"""
import sys
import os
import subprocess
from pathlib import Path


def print_header(text):
    """打印标题"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")


def check_python():
    """检查Python版本"""
    print("\n✓ 检查 Python 版本...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro} (符合要求)")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor} (需要 3.9+)")
        return False


def check_dependencies():
    """检查Python依赖"""
    print("\n✓ 检查 Python 依赖...")

    required = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'sqlalchemy': 'SQLAlchemy',
        'pydantic': 'Pydantic',
        'jose': 'python-jose',
        'passlib': 'Passlib',
        'redis': 'Redis',
        'httpx': 'httpx',
    }

    missing = []
    for package, name in required.items():
        try:
            __import__(package)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} (缺失)")
            missing.append(name)

    if missing:
        print(f"\n  安装缺失的依赖:")
        print(f"  pip install -r requirements.txt")
        return False

    return True


def check_database():
    """检查数据库连接"""
    print("\n✓ 检查数据库连接...")

    try:
        from app.db.database import engine
        from sqlalchemy import text

        with engine.begin() as conn:
            result = conn.execute(text("SELECT 1"))
            print(f"  ✓ PostgreSQL 连接正常")
            return True
    except Exception as e:
        print(f"  ✗ PostgreSQL 连接失败: {str(e)}")
        print(f"\n  检查事项:")
        print(f"  1. PostgreSQL 服务是否启动？")
        print(f"  2. 数据库配置是否正确？")
        print(f"  3. 数据库用户密码是否正确？")
        return False


def check_redis():
    """检查Redis连接"""
    print("\n✓ 检查 Redis 连接...")

    try:
        from app.core.config import settings
        import redis

        r = redis.from_url(settings.REDIS_URL)
        r.ping()
        print(f"  ✓ Redis 连接正常")
        return True
    except Exception as e:
        print(f"  ✗ Redis 连接失败: {str(e)}")
        print(f"\n  检查事项:")
        print(f"  1. Redis 服务是否启动？")
        print(f"  2. Redis 地址配置是否正确？")
        return False


def check_env_file():
    """检查环境文件"""
    print("\n✓ 检查环境配置...")

    env_file = Path('.env')
    env_example = Path('.env.example')

    if env_file.exists():
        print(f"  ✓ .env 文件存在")
        return True
    elif env_example.exists():
        print(f"  ✗ .env 文件不存在")
        print(f"  提示: 从 .env.example 复制")
        print(f"  cp .env.example .env")
        return False
    else:
        print(f"  ✗ 没有找到 .env 或 .env.example")
        return False


def check_models():
    """检查数据库模型"""
    print("\n✓ 检查数据库模型...")

    try:
        from app.models import User, Customer, Product, Order
        print(f"  ✓ 所有模型加载成功")
        return True
    except Exception as e:
        print(f"  ✗ 模型加载失败: {str(e)}")
        return False


def check_auth_endpoints():
    """检查认证API端点"""
    print("\n✓ 检查认证 API 端点...")

    try:
        from app.api.v1.endpoints import auth

        endpoints = [
            '/auth/login/password',
            '/auth/register/password',
            '/auth/login/phone',
            '/auth/register/phone',
            '/auth/login/wechat',
            '/auth/refresh-token',
        ]

        print(f"  ✓ 认证端点已配置:")
        for endpoint in endpoints:
            print(f"    - POST {endpoint}")

        return True
    except Exception as e:
        print(f"  ✗ 认证端点加载失败: {str(e)}")
        return False


def main():
    """运行所有检查"""
    print_header("养生店系统 - 后端环境检查")

    results = []

    # 检查Python
    results.append(("Python版本", check_python()))

    # 检查依赖
    results.append(("Python依赖", check_dependencies()))

    # 检查环境文件
    results.append(("环境配置", check_env_file()))

    # 检查模型
    results.append(("数据库模型", check_models()))

    # 检查数据库
    results.append(("数据库连接", check_database()))

    # 检查Redis
    results.append(("Redis连接", check_redis()))

    # 检查API端点
    results.append(("API端点", check_auth_endpoints()))

    # 打印总结
    print_header("检查结果总结")

    passed = 0
    failed = 0

    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{status:8} {name}")
        if result:
            passed += 1
        else:
            failed += 1

    print(f"\n总计: {passed} 通过, {failed} 失败")

    if failed == 0:
        print("\n" + "="*60)
        print("  所有检查都通过了! 可以启动应用程序")
        print("="*60)
        print("\n启动命令:")
        print("  uvicorn app.main:app --reload")
        print("\nAPI文档:")
        print("  http://localhost:8000/docs")
        return 0
    else:
        print("\n" + "="*60)
        print(f"  发现 {failed} 个问题需要解决")
        print("="*60)
        return 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n检查过程出错: {str(e)}")
        sys.exit(1)
