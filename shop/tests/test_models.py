from django.test import TestCase
from shop import models
import json


class ProductTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        models.Product.objects.create(
            name='Смартфон Samsung Galaxy A12 32GB Black (SM-A125F)',
            price=96780,
            category=models.Category.objects.create(
                name='Смартфоны и планшеты'),
            brand=models.Brand.objects.create(name='Samsung', image_url=''),
            properties=json.loads("""
            {
              "specifications": {
                "Цвет": "Черный"
              }
            }
            """)
        )

    def test_color_is_black(self):
        product = models.Product.objects.get(id=1)
        specifications = product.properties['specifications']
        print(specifications['Цвет'], 'Черный')

    def test_brand_is_samsung(self):
        product = models.Product.objects.get(id=1)
        self.assertEquals(product.brand.name, 'Samsung')
