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
    