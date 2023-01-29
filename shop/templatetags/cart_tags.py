from django.core.exceptions import ObjectDoesNotExist
from django import template
from .. import models


register = template.Library()


@register.simple_tag
def cart_product_from_user(user, product):
    try:
        user.profile
    except AttributeError:
        return None
    
    try:
        cart_product = models.CartProduct.objects.get(
            profile=user.profile, product=product)
        return cart_product
    except ObjectDoesNotExist:
        return None
