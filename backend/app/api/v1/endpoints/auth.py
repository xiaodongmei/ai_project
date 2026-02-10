"""认证端点"""
from fastapi import APIRouter, Response
from pydantic import BaseModel
import time

router = APIRouter(prefix="/auth", tags=["auth"])

# 临时存储验证码（演示用，实际应使用 Redis）
verification_codes = {}


class LoginRequest(BaseModel):
    username: str
    password: str


class SendCodeRequest(BaseModel):
    phone: str


class RegisterRequest(BaseModel):
    phone: str
    code: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict


class RegisterResponse(BaseModel):
    message: str
    user: dict = None


@router.post("/send-code")
async def send_code(request: SendCodeRequest):
    """发送验证码 - 演示用，固定返回 123456"""
    code = "123456"
    # 存储验证码和时间戳（5分钟过期）
    verification_codes[request.phone] = {
        "code": code,
        "timestamp": time.time()
    }

    return {
        "message": "验证码已发送",
        "phone": request.phone,
        "code": code  # 演示环境直接返回
    }


@router.post("/register", response_model=RegisterResponse)
async def register(request: RegisterRequest):
    """用户注册"""
    # 验证验证码
    if request.phone not in verification_codes:
        return {
            "message": "请先获取验证码",
        }

    stored_data = verification_codes[request.phone]
    stored_code = stored_data.get("code")

    # 检查验证码是否过期（5分钟）
    if time.time() - stored_data.get("timestamp", 0) > 300:
        del verification_codes[request.phone]
        return {
            "message": "验证码已过期，请重新获取",
        }

    if stored_code != request.code:
        return {
            "message": "验证码错误",
        }

    # 清除使用过的验证码
    del verification_codes[request.phone]

    return {
        "message": "注册成功",
        "user": {
            "id": 1,
            "phone": request.phone,
            "role": "customer"
        }
    }


@router.options("/login")
@router.options("/send-code")
@router.options("/register")
@router.options("/logout")
async def cors_preflight(response: Response):
    """处理所有 CORS 预检请求"""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Max-Age"] = "86400"
    response.status_code = 204  # No Content
    return None


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """用户登录 - 演示用，任何用户名密码都可登录"""
    # 简单演示：任何用户名和密码都可以登录
    return {
        "access_token": f"token-{request.username}-{int(time.time())}",
        "token_type": "bearer",
        "user": {
            "id": 1,
            "username": request.username,
            "email": f"{request.username}@example.com",
            "role": "admin"
        }
    }


@router.post("/logout")
async def logout():
    """用户登出"""
    return {"message": "登出成功"}
