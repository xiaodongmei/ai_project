"""认证服务"""
from datetime import timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import (
    LoginResponse, UserResponse,
    LoginByPasswordRequest, LoginByPhoneRequest, LoginByWechatRequest,
    RegisterByPasswordRequest, RegisterByPhoneRequest, RegisterByWechatRequest,
)
from app.core.security import (
    hash_password, verify_password, create_access_token, create_refresh_token,
    get_wechat_user_info, generate_sms_code, send_sms_code
)
from app.core.config import settings
from fastapi import HTTPException, status


class AuthService:
    """认证服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ========== 账号密码认证 ==========

    async def login_by_password(self, req: LoginByPasswordRequest) -> LoginResponse:
        """账号密码登录"""
        # 查找用户
        query = select(User).where(User.username == req.username)
        result = await self.db.execute(query)
        user = result.scalars().first()

        if not user or not verify_password(req.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="账户已禁用"
            )

        return await self._create_login_response(user)


    async def register_by_password(self, req: RegisterByPasswordRequest) -> LoginResponse:
        """账号密码注册"""
        # 检查用户名是否已存在
        query = select(User).where(User.username == req.username)
        result = await self.db.execute(query)
        if result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )

        # 检查邮箱是否已存在
        query = select(User).where(User.email == req.email)
        result = await self.db.execute(query)
        if result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已注册"
            )

        # 创建新用户
        user = User(
            username=req.username,
            email=req.email,
            password_hash=hash_password(req.password),
            full_name=req.full_name or req.username,
            role="customer",
            is_active=True,
            login_types="password",
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return await self._create_login_response(user)


    # ========== 手机号认证 ==========

    async def send_phone_code(self, phone: str, type: str = "login") -> dict:
        """发送手机验证码"""
        code = generate_sms_code()

        # 调用SMS服务发送
        success = await send_sms_code(phone, code)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="发送验证码失败，请稍后重试"
            )

        # 这里应该存储验证码到Redis等缓存，设置过期时间（5分钟）
        # redis_key = f"sms_code:{type}:{phone}"
        # await redis.setex(redis_key, 300, code)

        return {
            "message": "验证码已发送",
            "phone": phone,
            "expires_in": 300
        }


    async def login_by_phone(self, req: LoginByPhoneRequest) -> LoginResponse:
        """手机号登录"""
        # 这里应该验证code，从Redis或数据库中检查
        # redis_key = f"sms_code:login:{req.phone}"
        # cached_code = await redis.get(redis_key)

        # if not cached_code or cached_code != req.code:
        #     raise HTTPException(...)

        # 查找或创建用户
        query = select(User).where(User.phone == req.phone)
        result = await self.db.execute(query)
        user = result.scalars().first()

        if not user:
            # 首次登录，创建新用户
            user = User(
                phone=req.phone,
                phone_verified=True,
                role="customer",
                is_active=True,
                login_types="phone",
            )
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)

        return await self._create_login_response(user)


    async def register_by_phone(self, req: RegisterByPhoneRequest) -> LoginResponse:
        """手机号注册"""
        # 验证code（应从缓存检查）

        # 检查手机号是否已注册
        query = select(User).where(User.phone == req.phone)
        result = await self.db.execute(query)
        if result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="手机号已注册"
            )

        # 创建新用户
        user = User(
            phone=req.phone,
            password_hash=hash_password(req.password),
            full_name=req.full_name or req.phone,
            phone_verified=True,
            role="customer",
            is_active=True,
            login_types="phone",
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return await self._create_login_response(user)


    # ========== 微信认证 ==========

    async def login_by_wechat(self, req: LoginByWechatRequest) -> LoginResponse:
        """微信登录/注册"""
        # 用code换取用户信息
        wechat_info = await get_wechat_user_info(req.code)

        if not wechat_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="微信授权失败"
            )

        # 查找或创建用户
        query = select(User).where(User.wechat_openid == wechat_info["openid"])
        result = await self.db.execute(query)
        user = result.scalars().first()

        if user:
            # 更新微信信息
            user.wechat_nickname = wechat_info.get("nickname")
            user.wechat_avatar = wechat_info.get("avatar")
            user.wechat_unionid = wechat_info.get("unionid")
            await self.db.commit()
            await self.db.refresh(user)
        else:
            # 创建新用户
            user = User(
                wechat_openid=wechat_info["openid"],
                wechat_unionid=wechat_info.get("unionid"),
                wechat_nickname=wechat_info.get("nickname"),
                wechat_avatar=wechat_info.get("avatar"),
                full_name=wechat_info.get("nickname", "微信用户"),
                role="customer",
                is_active=True,
                login_types="wechat",
            )
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)

        return await self._create_login_response(user)


    async def bind_wechat(self, user_id: int, code: str) -> dict:
        """绑定微信账号"""
        # 获取微信用户信息
        wechat_info = await get_wechat_user_info(code)

        if not wechat_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="微信授权失败"
            )

        # 查询用户
        user = await self.db.get(User, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )

        # 绑定微信
        user.wechat_openid = wechat_info["openid"]
        user.wechat_unionid = wechat_info.get("unionid")
        user.wechat_nickname = wechat_info.get("nickname")
        user.wechat_avatar = wechat_info.get("avatar")

        await self.db.commit()
        await self.db.refresh(user)

        return {"message": "微信绑定成功"}


    # ========== Token 管理 ==========

    async def refresh_token(self, refresh_token: str) -> dict:
        """刷新访问令牌"""
        from app.core.security import decode_token

        payload = decode_token(refresh_token)

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="刷新令牌无效"
            )

        user_id = payload.get("sub")
        user = await self.db.get(User, int(user_id))

        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户不存在或已禁用"
            )

        new_access_token = create_access_token({
            "sub": str(user.id),
            "username": user.username,
            "role": user.role,
        })

        return {
            "access_token": new_access_token,
            "token_type": "bearer",
        }


    # ========== 辅助方法 ==========

    async def _create_login_response(self, user: User) -> LoginResponse:
        """创建登录响应"""
        access_token = create_access_token({
            "sub": str(user.id),
            "username": user.username,
            "role": user.role,
        })

        refresh_token = create_refresh_token({
            "sub": str(user.id),
            "username": user.username,
            "role": user.role,
        })

        user_response = UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            phone=user.phone,
            avatar_url=user.avatar_url,
            wechat_nickname=user.wechat_nickname,
            alipay_nickname=user.alipay_nickname,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            phone_verified=user.phone_verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
            full_name=user.full_name,
            role=user.role,
        )

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=user_response,
        )
