from django.db import models
from django.urls import reverse
from users.models import Profile
import re


class Product(models.Model):
    name = models.CharField(max_length=256)
    price = models.FloatField()
    category = models.ForeignKey('shop.Category', on_delete=models.CASCADE)
    brand = models.ForeignKey('shop.Brand', on_delete=models.CASCADE)
    favorite = models.ManyToManyField(
        Profile, related_name='favorite_products', blank=True)
    compare = models.ManyToManyField(
        Profile, related_name='compare_products', blank=True)
    description = models.TextField(null=True, blank=True)
    properties = models.JSONField(null=True, blank=True)

    def first_image(self):
        return self.images()[0]

    def after_first_image(self):
        return self.images()[1:]

    def images(self) -> list[str]:
        return self.properties['images']

    def specifications(self) -> list[str]:
        specifications = self.properties['specifications']
        return map(
            lambda name: f'<span class="specification-name">{name}: </span><span class="specification-value">{specifications[name]}</span>',
            specifications)

    def to_favorite_url(self) -> str:
        return reverse('to_favorite', kwargs={'pk': self.id})

    def to_compare_url(self) -> str:
        return reverse('to_compare', kwargs={'pk': self.id})

    def to_cart_url(self) -> str:
        return reverse('to_cart', kwargs={'pk': self.id})

    def get_price(self) -> str:
        return ' '.join(re.findall(r'\d{1,3}', str(round(self.price))[::-1]))[::-1] + ' ₸'

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.id})

    def bread_crumps(self):
        return self.category.bread_crumps()

    def get_as_cart(self):
        cart_product = CartProduct.objects.filter(product=self).first()
        return cart_product


class Category(models.Model):
    name = models.CharField(max_length=256)
    parent = models.ForeignKey(
        'shop.Category', on_delete=models.CASCADE, null=True, blank=True)

    def bread_crumps(self):
        divider = '<span class="user-select-none me-3 ms-3">/</span>'
        html = '<a class="lnk" href="{% url \'index\' %}">Главная</a>'
        html += divider
        html += f'<a class="lnk" href="{self.get_absolute_url()}">{self}</a>'
        return html

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return "category_detail"


class Brand(models.Model):
    name = models.CharField(max_length=256)
    image_url = models.URLField()

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE,
                               related_name='product_reviews', null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    rating = models.IntegerField()
    review_text = models.TextField()

    def __str__(self) -> str:
        return super().__str__()


class CartProduct(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='cart_products'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='cart_products')
    count = models.IntegerField()

    def __str__(self) -> str:
        return self.product.__str__()
    
    def get_increment_url(self) -> str:
        return reverse('cart_increment', kwargs={
            'pk': self.id
        })
    
    def get_decrement_url(self) -> str:
        return reverse('cart_decrement', kwargs={
            'pk': self.id
        })
