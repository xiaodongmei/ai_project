"""安全工具"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
import httpx
import random
import string

from app.core.config import settings

# 密码加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer 认证
security = HTTPBearer()


# ========== 密码管理 ==========

def hash_password(password: str) -> str:
    """对密码进行哈希处理"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


# ========== Token 管理 ==========

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """创建刷新令牌"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """解码令牌"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except JWTError:
        return None


async def get_current_user(credentials: HTTPAuthCredentials = Depends(security)):
    """获取当前用户"""
    token = credentials.credentials
    payload = decode_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


# ========== 手机验证码 ==========

def generate_sms_code(length: int = 6) -> str:
    """生成短信验证码"""
    return "".join(random.choices(string.digits, k=length))


async def send_sms_code(phone: str, code: str) -> bool:
    """
    发送短信验证码（集成阿里云/腾讯云等）
    这里使用示例，实际应配置真实SMS服务
    """
    # TODO: 集成真实的SMS服务提供商
    # 示例使用阿里云或腾讯云
    print(f"[SMS] 发送验证码到 {phone}: {code}")
    return True


# ========== 微信相关 ==========

async def get_wechat_user_info(code: str) -> Optional[dict]:
    """
    通过微信授权code获取用户信息
    """
    try:
        # 第一步：用code换取access_token
        token_url = "https://api.weixin.qq.com/sns/oauth2/access_token"
        params = {
            "appid": settings.WECHAT_APP_ID,
            "secret": settings.WECHAT_APP_SECRET,
            "code": code,
            "grant_type": "authorization_code",
        }

        async with httpx.AsyncClient() as client:
            token_response = await client.get(token_url, params=params)
            token_data = token_response.json()

            if "errcode" in token_data:
                return None

            access_token = token_data.get("access_token")
            openid = token_data.get("openid")
            unionid = token_data.get("unionid")

            # 第二步：用access_token获取用户信息
            user_url = "https://api.weixin.qq.com/sns/userinfo"
            user_params = {
                "access_token": access_token,
                "openid": openid,
                "lang": "zh_CN",
            }

            user_response = await client.get(user_url, params=user_params)
            user_info = user_response.json()

            if "errcode" in user_info:
                return None

            return {
                "openid": openid,
                "unionid": unionid,
                "nickname": user_info.get("nickname"),
                "avatar": user_info.get("headimgurl"),
                "province": user_info.get("province"),
                "city": user_info.get("city"),
                "sex": user_info.get("sex"),
            }
    except Exception as e:
        print(f"Error getting wechat user info: {e}")
        return None


async def verify_wechat_signature(signature: str, timestamp: str, nonce: str, echostr: str) -> Optional[str]:
    """
    验证微信签名（用于服务器验证）
    """
    import hashlib

    data = [settings.WECHAT_TOKEN, timestamp, nonce]
    data.sort()
    data = "".join(data)

    sha1 = hashlib.sha1()
    sha1.update(data.encode("utf-8"))
    calculated_signature = sha1.hexdigest()

    if calculated_signature == signature:
        return echostr
    return None


# ========== 权限检查 ==========

def verify_admin(payload: dict) -> bool:
    """验证是否为管理员"""
    return payload.get("role") == "admin"


def verify_employee(payload: dict) -> bool:
    """验证是否为员工"""
    return payload.get("role") in ["admin", "employee"]


def verify_customer(payload: dict) -> bool:
    """验证是否为客户"""
    return payload.get("role") in ["admin", "employee", "customer"]
