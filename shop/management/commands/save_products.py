from django.core.management.base import BaseCommand
from shop.models import Brand, Category, Product, Review, CartProduct
from lxml import html
import requests


headers = {
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0'
}


def save_branded(brand: str):
  URL = 'https://kaspi.kz/shop/c/smartphones/brand-{brand}'
  response = requests.get(URL, headers=headers)
  tree = html.fromstring(response.text)
  print(response.text)
  


class Command(BaseCommand):
  def add_arguments(self, parser) -> None:
    parser.add_argument('path', type=str)
    
  def handle(self, **options):
    for model_objects in [Model.objects.all() for Model in (Brand, Category, Product, Review, CartProduct)]:
      for model_object in model_objects:
        model_object.delete()
    save_branded('samsung')
    
    