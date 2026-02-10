"""密码安全测试"""
import pytest
from app.core.security import hash_password, verify_password


class TestPasswordSecurity:
    """密码安全测试类"""

    def test_hash_password(self):
        """测试密码哈希"""
        password = "secure_password_123"
        hashed = hash_password(password)

        # 哈希值应该不等于原密码
        assert hashed != password
        # 哈希值应该不为空
        assert hashed is not None
        assert len(hashed) > 0

    def test_verify_correct_password(self):
        """测试验证正确密码"""
        password = "correct_password"
        hashed = hash_password(password)

        # 验证正确密码
        assert verify_password(password, hashed) is True

    def test_verify_incorrect_password(self):
        """测试验证错误密码"""
        password = "correct_password"
        wrong_password = "wrong_password"
        hashed = hash_password(password)

        # 验证错误密码
        assert verify_password(wrong_password, hashed) is False

    def test_hash_consistency(self):
        """测试哈希一致性"""
        password = "test_password"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        # 同一密码的两个哈希值应该不同（由于盐值）
        assert hash1 != hash2

        # 但都应该与密码验证匹配
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True

    def test_password_length_requirements(self):
        """测试密码长度要求"""
        short_password = "12345"  # 过短
        long_password = "a" * 256  # 很长
        normal_password = "secure_password_123"

        # 所有密码都应该能被哈希
        short_hashed = hash_password(short_password)
        long_hashed = hash_password(long_password)
        normal_hashed = hash_password(normal_password)

        assert verify_password(short_password, short_hashed) is True
        assert verify_password(long_password, long_hashed) is True
        assert verify_password(normal_password, normal_hashed) is True

    def test_special_characters_in_password(self):
        """测试特殊字符密码"""
        special_password = "P@ssw0rd!#$%^&*()"
        hashed = hash_password(special_password)

        assert verify_password(special_password, hashed) is True
        assert verify_password("P@ssw0rd!#$%^&*(", hashed) is False  # 缺少一个字符

    def test_unicode_password(self):
        """测试Unicode密码"""
        unicode_password = "密码@123"
        hashed = hash_password(unicode_password)

        assert verify_password(unicode_password, hashed) is True
        assert verify_password("密码@124", hashed) is False

    def test_case_sensitive_password(self):
        """测试密码大小写敏感性"""
        password = "MyPassword"
        hashed = hash_password(password)

        assert verify_password("MyPassword", hashed) is True
        assert verify_password("mypassword", hashed) is False
        assert verify_password("MYPASSWORD", hashed) is False

    def test_empty_password_hash(self):
        """测试空密码哈希"""
        empty_password = ""
        hashed = hash_password(empty_password)

        # 空密码应该也能被哈希和验证
        assert verify_password("", hashed) is True
        assert verify_password("anything", hashed) is False

    def test_password_with_spaces(self):
        """测试包含空格的密码"""
        password_with_spaces = "password with spaces 123"
        hashed = hash_password(password_with_spaces)

        assert verify_password("password with spaces 123", hashed) is True
        assert verify_password("passwordwith spaces 123", hashed) is False
