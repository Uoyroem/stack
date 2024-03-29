from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from utils import format


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self) -> str:
        return super().__str__()

    def my_review_products(self):
        return [product_review.product for product_review in self.product_reviews.all()]
    
    def get_products(self):
        return [cart_product.product for cart_product in self.cart_products.all()]

    def get_cart_items_count(self):
        return sum(cart_product.count for cart_product in self.cart_products.all())

    def get_compare_items_count(self):
        return self.compare_products.count()

    def get_favorite_items_count(self):
        return self.favorite_products.count()

    def get_cart_items_price_not_formatted(self):
        return sum(cart_product.product.price * cart_product.count for cart_product in self.cart_products.all())
    
    def get_cart_items_price(self):
        return format.format_price(self.get_cart_items_price_not_formatted())


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
