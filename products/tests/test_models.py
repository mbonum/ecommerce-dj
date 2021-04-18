from django.test import TestCase

from apps.products.models import Category, Product


class TestCategoryModel(TestCase):
    def setUp(self):
        self.data1 = Category.objects.create(name="book", slug="book")

    def test_category_model_entry(self):
        """Test Product model data insertion/types/field attributes"""
        data = self.data1
        self.assertTrue(isinstance(data, Category))


class TestProductModel(TestCase):
    def setUp(self):
        self.data1 = Product.objects.create(name_product="book", slug="book")

    def test_product_model_entry(self):
        """Test Product model data insertion/types/field attributes"""
        data = self.data1
        self.assertTrue(isinstance(data, Product))

    def test_product_model_entry(self):
        """Test Product model return name"""
        data = self.data1
        self.assertEqual(str(data), "book")
