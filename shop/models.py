from django.db import models
from django.urls import reverse
import users.models as users_models
from utils import format
import uuid


STAR = '<span class="material-symbols-outlined icon">star</span>'
STAR_ACTIVE = '<span class="material-symbols-outlined icon icon--blue">star</span>'


def product_default_properties():
    return {
        "specifications": {},
        "images": []
    }


class Product(models.Model):
    name = models.CharField(max_length=256)
    price = models.FloatField()
    category = models.ForeignKey('shop.Category', on_delete=models.CASCADE)
    brand = models.ForeignKey('shop.Brand', on_delete=models.CASCADE)
    favorite = models.ManyToManyField(
        users_models.Profile, related_name='favorite_products', blank=True)
    compare = models.ManyToManyField(
        users_models.Profile, related_name='compare_products', blank=True)
    description = models.TextField(null=True, blank=True)
    properties = models.JSONField(default=product_default_properties)

    def first_image(self) -> str:
        return self.images()[0]

    def get_middle_rating_as_html(self) -> str:
        count = self.reviews.count()
        count_html = f'<span class="text-primary ms-2">({count})</span>'
        if not self.reviews.all():
            return STAR * 5 + count_html
        middle = sum(review.rating for review in self.reviews.all()) // count
        print(middle, count, count - middle)
        return STAR_ACTIVE * middle + STAR * (5 - middle) + count_html

    def after_first_image(self) -> list[str]:
        return self.images()[1:]

    def images(self) -> list[str]:
        return self.properties['images']

    def specifications(self) -> dict[str, str] | None:
        return self.properties['specifications']

    def specifications_as_span_list(self) -> list[str]:
        specifications = dict(list(self.specifications().items())[:6])

        return map(
            lambda name: f'<span class="specification-name">{name}: </span><span class="specification-value">{specifications[name]}</span>',
            specifications)

    def specifications_first_part_as_trs(self) -> list[str]:
        specifications = self.specifications()
        return map(
            lambda key: f'<tr><td>{key}</td><td>{specifications[key]}</td></tr>',
            list(specifications.keys())[:len(specifications) // 2]
        )

    def specifications_second_part_as_trs(self) -> list[str]:
        specifications = self.specifications()
        return map(
            lambda key: f'<tr><td>{key}</td><td>{specifications[key]}</td></tr>',
            list(specifications.keys())[len(specifications) // 2:]
        )

    def to_favorite_url(self) -> str:
        return reverse('to_favorite', kwargs={'pk': self.id})

    def to_compare_url(self) -> str:
        return reverse('to_compare', kwargs={'pk': self.id})

    def to_cart_url(self) -> str:
        return reverse('to_cart', kwargs={'pk': self.id})

    def get_price(self) -> str:
        return format.format_price(self.price)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("product", kwargs={"pk": self.id})

    def bread_crumps(self) -> str:
        return self.category.bread_crumps()

    def get_compare_delete_url(self):
        return reverse('compare_delete', kwargs={'pk': self.id})


class Category(models.Model):
    name = models.CharField(max_length=256)
    parent = models.ForeignKey(
        'shop.Category', on_delete=models.CASCADE, null=True, blank=True)

    def bread_crumps(self):
        divider = '<span class="bread-crumps__divider">/</span>'
        html = '<a class="link bread-crumps__link" href="/">Главная</a>'
        html += divider
        html += f'<a class="link bread-crumps__link" href="{self.get_absolute_url()}">{self}</a>'
        return html

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={
            'pk': self.id
        })


class Brand(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    sender = models.ForeignKey(users_models.Profile, on_delete=models.CASCADE,
                               related_name='product_reviews', null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    rating = models.IntegerField(choices=zip(range(1, 6), range(1, 6)))
    review_text = models.TextField()
    post_date = models.DateField(auto_now=True, null=True, blank=True)

    def rating_as_html(self) -> str:
        return STAR_ACTIVE * self.rating + STAR * (5 - self.rating)

    def __str__(self) -> str:
        return super().__str__()


class CartProduct(models.Model):
    profile = models.ForeignKey(
        users_models.Profile, on_delete=models.CASCADE, related_name='cart_products'
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

    def get_delete_url(self) -> str:
        return reverse('cart_delete', kwargs={
            'pk': self.id
        })

    def get_price(self) -> str:
        return format.format_price(self.product.price * self.count)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(
        users_models.Profile, on_delete=models.CASCADE, related_name='orders'
    )
    products_info = models.JSONField()
    order_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    is_accept = models.BooleanField(default=False)
    cart_items_price = models.FloatField(default=0)
    delivery_price = models.FloatField(default=0)
    def get_absolute_url(self):
        return reverse('order', kwargs={
            'pk': self.id
        })
    
    def get_accept_url(self):
        return reverse('order_accept', kwargs={
            'pk': self.id
        })
    
    @property
    def total_price(self):
        return format.format_price(float(self.cart_items_price + self.delivery_price))
    
    @property
    def delivery_price_formatted(self):
        return format.format_price(self.delivery_price)
    
    @property
    def products_with_count(self):
        return [(Product.objects.get(id=product_info['product']), product_info['count']) for product_info in self.products_info]
    
    def __str__(self):
        return str(self.order_date.year + self.order_date.hour + self.order_date.second)
    