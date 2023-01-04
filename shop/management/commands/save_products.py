from django.core.management.base import BaseCommand
from shop.models import Brand, Category, Product, Review, CartProduct
from lxml import html
import requests


BASE_URL = 'https://kz.e-katalog.com/'
HEADERS = {
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0'
}


def save_branded(brand: str):
  """ 
  TODO: Сделать парсинг сайта e-catalog. Достаточно будет 
  трех страницы продуктов каждого из: смартфонов, ноутбуков, игровых консолей.
  """
  tree = html.fromstring(requests.get(BASE_URL + 'list/122/pr-1358/', headers=HEADERS).text)
  for a in tree.xpath('//a[@class="model-short-title no-u"]'):
    smartphone_tree = html.fromstring(requests.get(BASE_URL + a.get('href'), headers=HEADERS).text)
    print(smartphone_tree.xpath('//div[@class="desc-short-prices"]/a/div/span[@itemprop="lowPrice"]/text()')[0])

  


class Command(BaseCommand):
  def add_arguments(self, parser) -> None:
    parser.add_argument('path', type=str)
    
  def handle(self, **options):
    for model_objects in [Model.objects.all() for Model in (Brand, Category, Product, Review, CartProduct)]:
      for model_object in model_objects:
        model_object.delete()
    save_branded('samsung')
    
    