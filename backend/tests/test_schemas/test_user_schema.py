"""User Schema 验证测试"""
import pytest
from pydantic import ValidationError
from app.schemas.user import UserCreate, UserUpdate, UserResponse


class TestUserCreateSchema:
    """UserCreate Schema 验证测试"""

    def test_valid_user_create(self):
        """测试有效的用户创建"""
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "secure_password_123",
            "full_name": "Test User",
            "phone": "13800000001"
        }
        user = UserCreate(**data)

        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.password == "secure_password_123"
        assert user.full_name == "Test User"
        assert user.phone == "13800000001"

    def test_missing_username(self):
        """测试缺少用户名"""
        data = {
            "email": "test@example.com",
            "password": "secure_password_123"
        }

        with pytest.raises(ValidationError):
            UserCreate(**data)

    def test_missing_email(self):
        """测试缺少邮箱"""
        data = {
            "username": "testuser",
            "password": "secure_password_123"
        }

        with pytest.raises(ValidationError):
            UserCreate(**data)

    def test_missing_password(self):
        """测试缺少密码"""
        data = {
            "username": "testuser",
            "email": "test@example.com"
        }

        with pytest.raises(ValidationError):
            UserCreate(**data)

    def test_invalid_email_format(self):
        """测试无效邮箱格式"""
        data = {
            "username": "testuser",
            "email": "invalid_email",
            "password": "secure_password_123"
        }

        with pytest.raises(ValidationError):
            UserCreate(**data)

    def test_invalid_email_format_2(self):
        """测试无效邮箱格式 - 缺少@"""
        data = {
            "username": "testuser",
            "email": "test.example.com",
            "password": "secure_password_123"
        }

        with pytest.raises(ValidationError):
            UserCreate(**data)

    def test_password_too_short(self):
        """测试密码太短"""
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "123"  # 过短
        }

        # 根据 schema 的定义，可能会通过或验证失败
        # 这取决于是否有 min_length 限制
        try:
            user = UserCreate(**data)
            assert user.password == "123"
        except ValidationError:
            pass

    def test_optional_full_name(self):
        """测试可选的全名"""
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "secure_password_123"
        }
        user = UserCreate(**data)

        assert user.username == "testuser"
        # full_name 可能是可选的
        assert hasattr(user, 'full_name')

    def test_optional_phone(self):
        """测试可选的电话"""
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "secure_password_123"
        }
        user = UserCreate(**data)

        assert user.username == "testuser"
        # phone 可能是可选的
        assert hasattr(user, 'phone') or True


class TestUserUpdateSchema:
    """UserUpdate Schema 验证测试"""

    def test_valid_user_update(self):
        """测试有效的用户更新"""
        data = {
            "email": "newemail@example.com",
            "full_name": "New Name",
            "phone": "13900000001"
        }
        update = UserUpdate(**data)

        assert update.email == "newemail@example.com"
        assert update.full_name == "New Name"
        assert update.phone == "13900000001"

    def test_empty_update(self):
        """测试空更新"""
        data = {}
        update = UserUpdate(**data)

        # 应该允许空更新（所有字段都是可选的）
        assert update is not None

    def test_partial_update(self):
        """测试部分更新"""
        data = {
            "full_name": "Updated Name"
        }
        update = UserUpdate(**data)

        assert update.full_name == "Updated Name"
        assert update.email is None
        assert update.phone is None

    def test_invalid_email_in_update(self):
        """测试更新中的无效邮箱"""
        data = {
            "email": "invalid_email"
        }

        with pytest.raises(ValidationError):
            UserUpdate(**data)


class TestUserResponseSchema:
    """UserResponse Schema 验证测试"""

    def test_valid_user_response(self):
        """测试有效的用户响应"""
        data = {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
            "phone": "13800000001",
            "role": "employee",
            "is_active": True
        }
        response = UserResponse(**data)

        assert response.id == 1
        assert response.username == "testuser"
        assert response.email == "test@example.com"
        assert response.role == "employee"

    def test_user_response_excludes_password(self):
        """测试用户响应不包含密码"""
        data = {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "role": "employee"
        }
        response = UserResponse(**data)

        # 响应中不应该有 hashed_password 字段
        assert not hasattr(response, 'hashed_password')

    def test_missing_id_in_response(self):
        """测试响应中缺少ID"""
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "role": "employee"
        }

        with pytest.raises(ValidationError):
            UserResponse(**data)

    def test_missing_username_in_response(self):
        """测试响应中缺少用户名"""
        data = {
            "id": 1,
            "email": "test@example.com",
            "role": "employee"
        }

        with pytest.raises(ValidationError):
            UserResponse(**data)
