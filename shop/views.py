from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, DetailView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from . import models, forms
from email.mime.text import MIMEText
import smtplib, ssl
from utils import products


class IndexView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        phone_category = models.Category.objects.filter(
            name='Смартфоны и планшеты').first()
        phone_list = models.Product.objects.filter(category=phone_category)
        return render(request, 'index.html', {
            'phone_list': phone_list,
            'category_list': models.Category.objects.all()
        })


class ProductView(View):
    def get(self, request: HttpRequest, pk: int):
        return render(request, 'product.html', {
            'product': get_object_or_404(models.Product, id=pk),
            'review_form': forms.ReviewForm({
                'rating': 0,
                'review_text': ''
            })
        })

    def post(self, request: HttpRequest, pk: int):
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.sender = request.user.profile
            review.product = get_object_or_404(models.Product, id=pk)
            review.save()
        return redirect('product', pk=pk)


class CategoryView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        category = get_object_or_404(models.Category, id=pk)
        category_product_list = models.Product.objects.filter(
            category=category)
        min_price_product, max_price_product = products.get_minmax_products(category_product_list)
        price_min, price_max = int(request.GET.get(
            'price_min', min_price_product.price)), int(request.GET.get('price_max', max_price_product.price))
        def filter_products(product):
            specifications = product.specifications()
            if price_min <= int(product.price) <= price_max:
                for key in request.GET: 
                    if key.startswith('price'):
                        continue
                    if key not in specifications.values():
                        return False
            else:
                return False
            return True
        print(products.get_values_specifications(category_product_list, request.GET))
        return render(request, 'category.html', {
            'price_min': price_min,
            'price_max': price_max,
            'category': category,
            'category_product_list': filter(filter_products, category_product_list),
            'values_specifications': products.get_values_specifications(category_product_list, request.GET)
        })


def message_and_count(message: str, count: int, total_count: int | None = None) -> JsonResponse:
    return JsonResponse({
        'message': message,
        'count': count,
        'totalCount': total_count or count
    })


def to_compare(request: HttpRequest, pk: int) -> HttpResponse:
    if request.user.is_anonymous:
        return message_and_count('Вы должный зарегистрироваться', 0)

    product = get_object_or_404(models.Product, id=pk)
    if product.compare.contains(request.user.profile):
        product.compare.remove(request.user.profile)
        return message_and_count('Успешно удалено из сравнение.', 0, request.user.profile.get_compare_items_count())
    else:
        if request.user.profile.compare_products.count() >= 4:
            return message_and_count('Максимальное количество продуктов в сравнений.', 0, request.user.profile.get_compare_items_count())
        product.compare.add(request.user.profile)
    return message_and_count('Успешно добавлено в сравнение.', request.user.profile.get_compare_items_count())


def to_cart(request: HttpRequest, pk: int) -> JsonResponse:
    if request.user.is_anonymous:
        return message_and_count('Вы должный зарегистрироваться', 0)

    product = get_object_or_404(models.Product, id=pk)
    try:
        cart_product = models.CartProduct.objects.get(
            profile=request.user.profile, product=product)
        return message_and_count('Этот продукт уже есть в корзине.', cart_product.count, request.user.profile.get_cart_items_count())
    except ObjectDoesNotExist:
        cart_product = models.CartProduct(
            profile=request.user.profile, product=product, count=1)
        cart_product.save()
        return message_and_count('Успешно добавлено в корзину.', cart_product.count, request.user.profile.get_cart_items_count())


def to_favorities(request: HttpRequest, pk: int) -> JsonResponse:
    if request.user.is_anonymous:
        return message_and_count('Вы должный зарегистрироваться', 0)

    product = get_object_or_404(models.Product, id=pk)

    if product.favorite.contains(request.user.profile):
        product.favorite.remove(request.user.profile)
        return message_and_count('Успешно удален с избранных.', 0, request.user.profile.get_favorite_items_count())

    product.favorite.add(request.user.profile)
    return message_and_count('Успешно добавлен в избранное.', 1, request.user.profile.get_favorite_items_count())


def cart_increment(request: HttpRequest, pk: int) -> JsonResponse:
    try:
        cart_product = models.CartProduct.objects.get(id=pk)
        cart_product.count += 1
        cart_product.save()
    except ObjectDoesNotExist:
        ...
    finally:
        return message_and_count('', request.user.profile.get_cart_items_count())


def cart_decrement(request: HttpRequest, pk: int) -> JsonResponse:
    try:
        cart_product = models.CartProduct.objects.get(id=pk)
        cart_product.count -= 1
        if cart_product.count == 0:
            cart_product.delete()
        else:
            cart_product.save()
    except ObjectDoesNotExist:
        ...
    finally:
        return message_and_count('', request.user.profile.get_cart_items_count())


def cart_delete(request: HttpRequest, pk: int) -> JsonResponse:
    try:
        cart_product = models.CartProduct.objects.get(id=pk).delete()
    except ObjectDoesNotExist:
        ...
    finally:
        return message_and_count('', request.user.profile.get_cart_items_count())


def compare_delete(request: HttpRequest, pk: int) -> JsonResponse:
    if request.user.is_anonymous:
        return message_and_count('Вы должный зарегистрироваться', 0)
    try:
        request.user.profile.compare_products.remove(
            get_object_or_404(models.Product, id=pk))
    except ObjectDoesNotExist:
        ...
    finally:
        return message_and_count('', request.user.profile.get_compare_items_count())


class SearchView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        query = request.GET['query']
        return render(request, 'search.html', {
            'query': query,
            'product_list': models.Product.objects.filter(name__icontains=query)
        })


class CartView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        cart_list = None
        if request.user.is_authenticated:
            cart_list = request.user.profile.cart_products.all()
        return render(request, 'cart.html', {
            'cart_list': cart_list
        })


class ComparesView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        all_specifications = {}
        compare_list = None
        if request.user.is_authenticated:
            compare_list = request.user.profile.compare_products.all()
            general_specifications = set()
            for compare_product in compare_list:
                general_specifications.update(
                    compare_product.specifications().keys())

            for key in general_specifications:
                all_specifications[key] = []
                for compare_product in compare_list:
                    all_specifications[key].append(
                        compare_product.specifications().get(key))

        return render(request, 'compares.html', {
            'compare_list': compare_list,
            'all_specifications': all_specifications
        })


class FavoritiesView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        favorite_list = None
        if request.user.is_authenticated:
            favorite_list = request.user.profile.favorite_products.all()

        return render(request, 'favorities.html', {
            'favorite_list': favorite_list
        })


class NewOrderView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'new_order.html', {
            'cart_items_price': request.user.profile.get_cart_items_price_not_formatted()
        })
    
    def post(self, request: HttpRequest) -> HttpResponse:
        order = models.Order.objects.create(
            profile=request.user.profile,
            delivery_price=int(request.POST['delivery']),
            cart_items_price=request.user.profile.get_cart_items_price_not_formatted(),
            products_info=[model_to_dict(
                cart_product) for cart_product in request.user.profile.cart_products.all()]
        )
        for cart_product in request.user.profile.cart_products.all():
            cart_product.delete()
        print(request.get_host() + order.get_accept_url())
        sender = 'uoyroem.stack.info@gmail.com'
        context = ssl.create_default_context()
        link_to_accept = 'http://' + request.get_host() + order.get_accept_url()
        email_html = f"""
        <h2>Заказ № {order}</h2> 
        <p>Сумма заказа: {order.total_price}</p>
        <a href={link_to_accept}>Подтвердить заказ.</a>
        """
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(sender, 'tlghuscznmzebqwb')
            msg = MIMEText(email_html, 'html')
            msg['Subject'] = f'StackInfo: Подтвердите заказ № {order} на сумму {order.total_price}.'
            server.send_message(msg, sender, request.user.email)
        return redirect(order.get_absolute_url())
    

def order_accept(request: HttpRequest, pk: str) -> HttpResponse:
    order = get_object_or_404(models.Order, id=pk)
    order.is_accept = True   
    order.is_paid = True 
    order.save()
    return redirect(order.get_absolute_url())


class OrderView(DetailView):
    model = models.Order
    template_name = 'order.html'
    
