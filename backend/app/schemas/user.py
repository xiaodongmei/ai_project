"""用户 Pydantic 模式"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime


# ========== 基础模式 ==========

class UserBase(BaseModel):
    """用户基础模式"""
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: str = "customer"


class UserResponse(BaseModel):
    """用户响应模式"""
    id: int
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    wechat_nickname: Optional[str] = None
    alipay_nickname: Optional[str] = None
    is_active: bool
    is_superuser: bool
    phone_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserInDB(UserBase):
    """用户数据库模式"""
    id: int
    username: Optional[str] = None
    email: Optional[str] = None
    password_hash: Optional[str] = None
    wechat_openid: Optional[str] = None
    wechat_unionid: Optional[str] = None
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True


# ========== 登录相关 ==========

class LoginByPasswordRequest(BaseModel):
    """账号密码登录"""
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)


class LoginByPhoneRequest(BaseModel):
    """手机号登录"""
    phone: str = Field(..., pattern=r"^1[3-9]\d{9}$")
    code: str = Field(..., min_length=6, max_length=6)


class LoginByWechatRequest(BaseModel):
    """微信扫码登录"""
    code: str = Field(...)  # 微信授权code
    userInfo: Optional[dict] = None  # 用户信息（可选）


class LoginResponse(BaseModel):
    """登录响应"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


# ========== 注册相关 ==========

class RegisterByPasswordRequest(BaseModel):
    """账号密码注册"""
    username: str = Field(..., min_length=3, max_length=100, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        """验证密码复杂度"""
        if not any(c.isupper() for c in v) and not any(c.isdigit() for c in v):
            raise ValueError("密码需包含大写字母或数字")
        return v


class RegisterByPhoneRequest(BaseModel):
    """手机号注册"""
    phone: str = Field(..., pattern=r"^1[3-9]\d{9}$")
    code: str = Field(..., min_length=6, max_length=6)
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None


class RegisterByWechatRequest(BaseModel):
    """微信注册"""
    code: str = Field(...)
    nickname: Optional[str] = None
    avatar: Optional[str] = None


# ========== 手机验证相关 ==========

class SendPhoneCodeRequest(BaseModel):
    """发送手机验证码请求"""
    phone: str = Field(..., pattern=r"^1[3-9]\d{9}$")
    type: str = Field(..., description="login | register | reset_password")


class VerifyPhoneCodeRequest(BaseModel):
    """验证手机验证码请求"""
    phone: str = Field(..., pattern=r"^1[3-9]\d{9}$")
    code: str = Field(..., min_length=6, max_length=6)


# ========== Token 相关 ==========

class TokenData(BaseModel):
    """令牌数据"""
    sub: str  # user_id
    username: Optional[str] = None
    role: str = "customer"
    exp: int


class RefreshTokenRequest(BaseModel):
    """刷新令牌请求"""
    refresh_token: str


class TokenResponse(BaseModel):
    """令牌响应"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# ========== 用户更新 ==========

class UserUpdate(BaseModel):
    """用户更新模式"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = Field(None, min_length=6)
    avatar_url: Optional[str] = None
