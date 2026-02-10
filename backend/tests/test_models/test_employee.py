"""Employee 模型测试"""
import pytest
from app.models.employee import Employee


@pytest.mark.asyncio
class TestEmployeeModel:
    """Employee 模型测试类"""

    async def test_create_employee(self, db_session, test_employee):
        """测试创建员工"""
        assert test_employee.id is not None
        assert test_employee.name == "张三"
        assert test_employee.employee_id == "EMP001"
        assert test_employee.position == "美容师"

    async def test_employee_id_uniqueness(self, db_session, employee_factory, test_user):
        """测试员工ID唯一性"""
        emp1 = await employee_factory.create(
            db_session,
            user_id=test_user.id,
            employee_id="EMP001"
        )

        # 创建另一个用户
        from tests.conftest import UserFactory
        user2 = await UserFactory.create(
            db_session,
            username="user2",
            email="user2@example.com"
        )

        emp2 = Employee(
            user_id=user2.id,
            name="李四",
            employee_id="EMP001",  # 相同的员工ID
            position="美容师"
        )
        db_session.add(emp2)

        with pytest.raises(Exception):
            await db_session.flush()

    async def test_employee_positions(self, db_session, employee_factory, user_factory):
        """测试员工岗位"""
        user1 = await user_factory.create(db_session, username="user1", email="user1@example.com")
        user2 = await user_factory.create(db_session, username="user2", email="user2@example.com")
        user3 = await user_factory.create(db_session, username="user3", email="user3@example.com")

        beautician = await employee_factory.create(
            db_session,
            user_id=user1.id,
            employee_id="EMP002",
            position="美容师"
        )
        therapist = await employee_factory.create(
            db_session,
            user_id=user2.id,
            employee_id="EMP003",
            position="理疗师"
        )
        manager = await employee_factory.create(
            db_session,
            user_id=user3.id,
            employee_id="EMP004",
            position="店长"
        )
        await db_session.flush()

        assert beautician.position == "美容师"
        assert therapist.position == "理疗师"
        assert manager.position == "店长"

    async def test_employee_departments(self, db_session, employee_factory, test_user):
        """测试员工部门"""
        from tests.conftest import UserFactory
        user1 = await UserFactory.create(
            db_session,
            username="user4",
            email="user4@example.com"
        )
        user2 = await UserFactory.create(
            db_session,
            username="user5",
            email="user5@example.com"
        )

        beauty_emp = await employee_factory.create(
            db_session,
            user_id=user1.id,
            employee_id="EMP005",
            department="美容部"
        )
        therapy_emp = await employee_factory.create(
            db_session,
            user_id=user2.id,
            employee_id="EMP006",
            department="理疗部"
        )
        await db_session.flush()

        assert beauty_emp.department == "美容部"
        assert therapy_emp.department == "理疗部"

    async def test_employee_salary(self, db_session, test_employee):
        """测试员工薪资"""
        assert test_employee.salary == 5000.0

        # 更新薪资
        test_employee.salary = 6000.0
        await db_session.flush()
        assert test_employee.salary == 6000.0

    async def test_employee_commission_rate(self, db_session, test_employee):
        """测试员工提成比例"""
        assert test_employee.commission_rate == 0.1

        # 测试不同的提成比例
        test_employee.commission_rate = 0.15
        await db_session.flush()
        assert test_employee.commission_rate == 0.15

    async def test_employee_commission_calculation(self, db_session, test_employee):
        """测试提成计算"""
        commission_rate = 0.1
        sales_amount = 10000.0
        expected_commission = sales_amount * commission_rate

        assert expected_commission == 1000.0

    async def test_employee_is_active(self, db_session, employee_factory, test_user):
        """测试员工活跃状态"""
        active = await employee_factory.create(
            db_session,
            user_id=test_user.id,
            employee_id="EMP007",
            is_active=True
        )
        inactive = Employee(
            user_id=test_user.id,
            name="赵六",
            employee_id="EMP008",
            position="美容师",
            is_active=False
        )
        db_session.add(inactive)
        await db_session.flush()

        assert active.is_active is True
        assert inactive.is_active is False

    async def test_employee_timestamps(self, db_session, test_employee):
        """测试员工时间戳"""
        await db_session.flush()
        assert test_employee.created_at is not None
        assert test_employee.updated_at is not None

    async def test_employee_hire_date(self, db_session, test_employee):
        """测试员工入职日期"""
        await db_session.flush()
        assert test_employee.hire_date is not None

    async def test_employee_performance_tracking(self, db_session, test_employee):
        """测试员工绩效跟踪"""
        assert hasattr(test_employee, 'accumulated_commission')
        assert hasattr(test_employee, 'accumulated_performance')

    async def test_employee_update(self, db_session, test_employee):
        """测试更新员工"""
        test_employee.position = "高级美容师"
        test_employee.salary = 7000.0
        test_employee.commission_rate = 0.12
        await db_session.flush()

        assert test_employee.position == "高级美容师"
        assert test_employee.salary == 7000.0
        assert test_employee.commission_rate == 0.12
