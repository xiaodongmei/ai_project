"""Product 模型测试"""
import pytest
from app.models.product import Product, ProductCategory


@pytest.mark.asyncio
class TestProductCategoryModel:
    """ProductCategory 模型测试类"""

    async def test_create_category(self, db_session, test_category):
        """测试创建分类"""
        assert test_category.id is not None
        assert test_category.name == "美容护肤"
        assert test_category.description == "美容护肤产品"

    async def test_category_is_active(self, db_session, category_factory):
        """测试分类活跃状态"""
        active = await category_factory.create(db_session, is_active=True)
        inactive = await category_factory.create(
            db_session,
            name="停用分类",
            is_active=False
        )
        await db_session.flush()

        assert active.is_active is True
        assert inactive.is_active is False

    async def test_category_display_order(self, db_session, category_factory):
        """测试分类显示顺序"""
        cat1 = await category_factory.create(db_session, display_order=1)
        cat2 = await category_factory.create(
            db_session,
            name="分类2",
            display_order=2
        )
        await db_session.flush()

        assert cat1.display_order == 1
        assert cat2.display_order == 2


@pytest.mark.asyncio
class TestProductModel:
    """Product 模型测试类"""

    async def test_create_product(self, db_session, test_product):
        """测试创建产品"""
        assert test_product.id is not None
        assert test_product.name == "面膜"
        assert test_product.description == "补水面膜"
        assert test_product.stock == 100

    async def test_product_pricing(self, db_session, test_product):
        """测试产品价格"""
        assert test_product.member_price == 88.0
        assert test_product.non_member_price == 99.0
        assert test_product.cost_price == 30.0

    async def test_product_stock_management(self, db_session, test_product):
        """测试库存管理"""
        assert test_product.stock == 100

        # 减少库存
        test_product.stock -= 10
        await db_session.flush()
        assert test_product.stock == 90

        # 增加库存
        test_product.stock += 5
        await db_session.flush()
        assert test_product.stock == 95

    async def test_product_low_stock_threshold(self, db_session, test_product):
        """测试低库存警告"""
        assert test_product.low_stock_threshold == 10

        # 测试库存是否低于警告值
        is_low_stock = test_product.stock <= test_product.low_stock_threshold
        assert is_low_stock is False

        # 减少库存至低值
        test_product.stock = 5
        await db_session.flush()

        is_low_stock = test_product.stock <= test_product.low_stock_threshold
        assert is_low_stock is True

    async def test_product_image_url(self, db_session, test_product):
        """测试产品图片URL"""
        assert test_product.image_url == "https://example.com/product.jpg"

        # 更新图片
        test_product.image_url = "https://example.com/new_product.jpg"
        await db_session.flush()
        assert test_product.image_url == "https://example.com/new_product.jpg"

    async def test_product_specification_and_unit(self, db_session, test_product):
        """测试规格和单位"""
        assert test_product.specification == "20ml"
        assert test_product.unit == "盒"

    async def test_product_rating_and_sales(self, db_session, test_product):
        """测试评分和销售数"""
        assert test_product.rating == 4.8
        assert test_product.sales_count == 50

    async def test_product_profit_calculation(self, db_session, test_product):
        """测试利润计算"""
        member_profit = test_product.member_price - test_product.cost_price
        non_member_profit = test_product.non_member_price - test_product.cost_price

        assert member_profit == 58.0  # 88 - 30
        assert non_member_profit == 69.0  # 99 - 30

    async def test_product_is_in_stock(self, db_session, test_product):
        """测试库存状态"""
        assert test_product.stock > 0

        test_product.stock = 0
        await db_session.flush()
        assert test_product.stock == 0

    async def test_product_with_category(self, db_session, test_product, test_category):
        """测试产品与分类关联"""
        assert test_product.category_id == test_category.id

    async def test_product_update(self, db_session, test_product):
        """测试更新产品"""
        test_product.name = "新面膜"
        test_product.member_price = 99.0
        test_product.stock = 50
        await db_session.flush()

        assert test_product.name == "新面膜"
        assert test_product.member_price == 99.0
        assert test_product.stock == 50

    async def test_multiple_products_in_category(self, db_session, product_factory, test_category):
        """测试分类下多个产品"""
        prod1 = await product_factory.create(
            db_session,
            category_id=test_category.id,
            name="产品1"
        )
        prod2 = await product_factory.create(
            db_session,
            category_id=test_category.id,
            name="产品2"
        )
        await db_session.flush()

        assert prod1.category_id == test_category.id
        assert prod2.category_id == test_category.id
