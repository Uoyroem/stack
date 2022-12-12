from django.db import models
from django.urls import reverse
from users.models import Profile
import re


class Product(models.Model):
    name = models.CharField(max_length=256)
    price = models.FloatField()
    category = models.ForeignKey('shop.Category', on_delete=models.CASCADE)
    brand = models.ForeignKey('shop.Brand', on_delete=models.CASCADE)
    favorite = models.ManyToManyField(Profile, related_name='favorite_products', blank=True)
    compare = models.ManyToManyField(Profile, related_name='compare_products', blank=True)
    description = models.TextField(null=True, blank=True)
    specifications = models.JSONField(null=True, blank=True)
    image_url = models.URLField()

    def get_price(self) -> str:
        return ' '.join(re.findall(r'\d{1,3}', str(round(self.price))[::-1]))[::-1] + ' ₸'
    
    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"id": self.id})
    

class Category(models.Model):
    name = models.CharField(max_length=256)
    parent = models.ForeignKey('shop.Category', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=256)
    image_url = models.URLField()
    
    def __str__(self) -> str:
        return self.name
    
    
class Review(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='product_reviews', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    rating = models.IntegerField()
    review_text = models.TextField()
    
    def __str__(self) -> str:
        return super().__str__()