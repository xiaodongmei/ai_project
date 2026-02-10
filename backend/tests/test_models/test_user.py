"""User 模型测试"""
import pytest
from app.core.security import verify_password, hash_password
from app.models.user import User


@pytest.mark.asyncio
class TestUserModel:
    """User 模型测试类"""

    async def test_create_user(self, db_session, test_user):
        """测试创建用户"""
        assert test_user.id is not None
        assert test_user.username == "testuser"
        assert test_user.email == "test@example.com"
        assert test_user.full_name == "Test User"
        assert test_user.phone == "13800000001"

    async def test_user_password_hashing(self, db_session, test_user):
        """测试用户密码哈希"""
        assert test_user.hashed_password != "password123"
        assert verify_password("password123", test_user.hashed_password)
        assert not verify_password("wrongpassword", test_user.hashed_password)

    async def test_user_role(self, db_session, user_factory):
        """测试用户角色"""
        admin = await user_factory.create(db_session, role="admin")
        employee = await user_factory.create(
            db_session,
            username="emp",
            email="emp@example.com",
            role="employee"
        )
        customer = await user_factory.create(
            db_session,
            username="cust",
            email="cust@example.com",
            role="customer"
        )

        await db_session.flush()

        assert admin.role == "admin"
        assert employee.role == "employee"
        assert customer.role == "customer"

    async def test_user_is_active(self, db_session, user_factory):
        """测试用户活跃状态"""
        active_user = await user_factory.create(db_session, is_active=True)
        inactive_user = await user_factory.create(
            db_session,
            username="inactive",
            email="inactive@example.com",
            is_active=False
        )

        await db_session.flush()

        assert active_user.is_active is True
        assert inactive_user.is_active is False

    async def test_user_is_superuser(self, db_session, user_factory):
        """测试超级用户标志"""
        normal_user = await user_factory.create(db_session, is_superuser=False)
        super_user = await user_factory.create(
            db_session,
            username="super",
            email="super@example.com",
            is_superuser=True
        )

        await db_session.flush()

        assert normal_user.is_superuser is False
        assert super_user.is_superuser is True

    async def test_user_timestamps(self, db_session, test_user):
        """测试用户时间戳"""
        await db_session.flush()
        assert test_user.created_at is not None
        assert test_user.updated_at is not None

    async def test_duplicate_username(self, db_session, user_factory):
        """测试重复用户名"""
        user1 = await user_factory.create(db_session, username="duplicate")
        user2 = User(
            username="duplicate",
            email="user2@example.com",
            hashed_password=hash_password("pass"),
            full_name="User 2"
        )
        db_session.add(user2)

        with pytest.raises(Exception):  # 数据库约束异常
            await db_session.flush()

    async def test_duplicate_email(self, db_session, user_factory):
        """测试重复邮箱"""
        user1 = await user_factory.create(db_session, email="duplicate@example.com")
        user2 = User(
            username="user2",
            email="duplicate@example.com",
            hashed_password=hash_password("pass"),
            full_name="User 2"
        )
        db_session.add(user2)

        with pytest.raises(Exception):  # 数据库约束异常
            await db_session.flush()

    async def test_user_update(self, db_session, test_user):
        """测试更新用户"""
        test_user.full_name = "Updated Name"
        test_user.phone = "13900000002"
        await db_session.flush()

        assert test_user.full_name == "Updated Name"
        assert test_user.phone == "13900000002"

    async def test_user_fields_not_null(self, db_session):
        """测试非空字段约束"""
        invalid_user = User(
            username=None,
            email="test@example.com",
            hashed_password="hashed",
            full_name="Test"
        )
        db_session.add(invalid_user)

        with pytest.raises(Exception):
            await db_session.flush()
