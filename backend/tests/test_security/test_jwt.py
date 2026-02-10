"""JWT 令牌安全测试"""
import pytest
from datetime import timedelta
from app.core.security import create_access_token, verify_token
from app.core.config import settings


class TestJWTSecurity:
    """JWT 安全测试类"""

    def test_create_access_token(self):
        """测试创建访问令牌"""
        subject = "testuser"
        token = create_access_token(data={"sub": subject})

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_verify_valid_token(self):
        """测试验证有效令牌"""
        subject = "testuser"
        token = create_access_token(data={"sub": subject})

        payload = verify_token(token)
        assert payload is not None
        assert payload.get("sub") == subject

    def test_verify_invalid_token(self):
        """测试验证无效令牌"""
        invalid_token = "invalid.token.here"

        payload = verify_token(invalid_token)
        assert payload is None

    def test_verify_expired_token(self):
        """测试验证过期令牌"""
        subject = "testuser"
        # 创建已过期的令牌（1天前过期）
        token = create_access_token(
            data={"sub": subject},
            expires_delta=timedelta(days=-1)
        )

        payload = verify_token(token)
        # 过期的令牌应该返回 None 或失败
        assert payload is None

    def test_token_contains_user_data(self):
        """测试令牌包含用户数据"""
        user_data = {
            "sub": "testuser",
            "email": "test@example.com",
            "role": "admin"
        }
        token = create_access_token(data=user_data)

        payload = verify_token(token)
        assert payload is not None
        assert payload.get("sub") == "testuser"
        assert payload.get("email") == "test@example.com"
        assert payload.get("role") == "admin"

    def test_token_expiration_time(self):
        """测试令牌过期时间"""
        subject = "testuser"
        token = create_access_token(data={"sub": subject})

        payload = verify_token(token)
        assert payload is not None
        assert "exp" in payload

    def test_token_with_custom_expiration(self):
        """测试自定义过期时间的令牌"""
        subject = "testuser"
        custom_expiration = timedelta(hours=24)
        token = create_access_token(
            data={"sub": subject},
            expires_delta=custom_expiration
        )

        payload = verify_token(token)
        assert payload is not None
        assert payload.get("sub") == subject

    def test_different_subjects_different_tokens(self):
        """测试不同用户的令牌不同"""
        token1 = create_access_token(data={"sub": "user1"})
        token2 = create_access_token(data={"sub": "user2"})

        # 令牌应该不同
        assert token1 != token2

        # 验证内容应该不同
        payload1 = verify_token(token1)
        payload2 = verify_token(token2)

        assert payload1.get("sub") == "user1"
        assert payload2.get("sub") == "user2"

    def test_token_tampering(self):
        """测试令牌篡改检测"""
        subject = "testuser"
        token = create_access_token(data={"sub": subject})

        # 尝试篡改令牌的最后一个字符
        tampered_token = token[:-1] + ("A" if token[-1] != "A" else "B")

        payload = verify_token(tampered_token)
        # 篡改的令牌应该验证失败
        assert payload is None

    def test_empty_token(self):
        """测试空令牌"""
        payload = verify_token("")
        assert payload is None

    def test_none_token(self):
        """测试None令牌"""
        # 这可能会抛出异常或返回None，取决于实现
        try:
            payload = verify_token(None)
            assert payload is None
        except (TypeError, AttributeError):
            # 预期异常
            pass

    def test_token_with_multiple_claims(self):
        """测试包含多个声明的令牌"""
        claims = {
            "sub": "testuser",
            "username": "testuser",
            "email": "test@example.com",
            "role": "admin",
            "permissions": ["read", "write", "delete"]
        }
        token = create_access_token(data=claims)

        payload = verify_token(token)
        assert payload is not None
        assert payload.get("sub") == "testuser"
        assert payload.get("username") == "testuser"
        assert payload.get("email") == "test@example.com"
        assert payload.get("role") == "admin"
        assert "permissions" in payload
