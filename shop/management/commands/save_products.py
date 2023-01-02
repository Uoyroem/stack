from django.core.management.base import BaseCommand
from shop.models import Brand, Category, Product, Review, CartProduct
import json


class Command(BaseCommand):
  def add_arguments(self, parser) -> None:
    parser.add_argument('path', type=str)
    
  def handle(self, **options):
    for model_objects in [Model.objects.all() for Model in (Brand, Category, Product, Review, CartProduct)]:
      for model_object in model_objects:
        model_object.delete()
    
    with open(options['path']) as file:
      categories = json.loads(file.read())
      for category in categories:
        category_model_object = Category.objects.create(name=category['name'])
        for brand in category['brands']:
          brand_model_object = Brand.objects.create(name=brand['name'])
          for product in brand['products']:
            Product.objects.create(
                category=category_model_object, brand=brand_model_object, **product)
    