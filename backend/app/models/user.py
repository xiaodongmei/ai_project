"""用户模型"""
from sqlalchemy import Boolean, Column, String, Integer, Text, Enum as SQLEnum
from app.db.base import Base, TimestampMixin, IDMixin
import enum


class LoginType(str, enum.Enum):
    """登录类型枚举"""
    PASSWORD = "password"  # 账号密码
    PHONE = "phone"  # 手机号
    WECHAT = "wechat"  # 微信
    ALIPAY = "alipay"  # 支付宝


class User(Base, IDMixin, TimestampMixin):
    """用户模型"""
    __tablename__ = "users"

    # 账号信息
    username = Column(String(100), unique=True, nullable=True, index=True)  # 用户名（可选）
    email = Column(String(255), unique=True, nullable=True, index=True)  # 邮箱（可选）
    password_hash = Column(String(255), nullable=True)  # 密码哈希（可选）

    # 个人信息
    full_name = Column(String(255), nullable=True)
    phone = Column(String(20), unique=True, nullable=True, index=True)  # 手机号
    avatar_url = Column(String(500), nullable=True)  # 头像URL

    # 微信信息
    wechat_openid = Column(String(100), unique=True, nullable=True, index=True)  # 微信OpenID
    wechat_unionid = Column(String(100), unique=True, nullable=True)  # 微信UnionID
    wechat_nickname = Column(String(255), nullable=True)  # 微支昵称
    wechat_avatar = Column(String(500), nullable=True)  # 微信头像

    # 支付宝信息
    alipay_id = Column(String(100), unique=True, nullable=True)
    alipay_nickname = Column(String(255), nullable=True)

    # 账号状态
    role = Column(String(50), default="customer", nullable=False)  # admin/employee/customer
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # 登录类型记录（JSON数组字符串：["password", "wechat"]）
    login_types = Column(Text, nullable=True)  # 该用户支持的登录方式

    # 手机验证
    phone_verified = Column(Boolean, default=False)
    phone_verify_code = Column(String(6), nullable=True)  # 验证码
    phone_verify_expires = Column(Integer, nullable=True)  # 验证码过期时间戳
