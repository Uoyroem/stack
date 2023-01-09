from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.http import HttpRequest, HttpResponse
from . import models, forms


class IndexView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        phone_category = models.Category.objects.filter(
            name='Смартфоны и планшеты').first()
        phone_list = models.Product.objects.filter(category=phone_category)
        return render(request, 'index.html', {
            'phone_list': phone_list
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


def to_compare(request: HttpRequest, pk: int) -> HttpResponse:
    product = get_object_or_404(models.Product, id=pk)
    if product.compare.contains(request.user.profile):
        product.compare.remove(request.user.profile)
        return HttpResponse('Успешно удалено из сравнение.')
    else:
        if request.user.profile.compare_products.count() >= 4:
            return HttpResponse('Максимальное количество продуктов в сравнений.')
        product.compare.add(request.user.profile)
    return HttpResponse('Успешно добавлено в сравнение.')


def to_cart(request: HttpRequest, pk: int) -> HttpResponse:
    product = get_object_or_404(models.Product, id=pk)
    cart_product = models.CartProduct(
        profile=request.user.profile, product=product, count=1)
    cart_product.save()
    return HttpResponse('Успешно добавлено в корзину.')


def to_favorities(request: HttpRequest, pk: int) -> HttpResponse:
    product = get_object_or_404(models.Product, id=pk)

    if product.favorite.contains(request.user.profile):
        product.favorite.remove(request.user.profile)
        return HttpResponse('Успешно удален с избранных.')

    product.favorite.add(request.user.profile)
    return HttpResponse('Успешно добавлен в избранное.')


def cart_increment(request: HttpRequest, pk: int) -> HttpResponse:
    cart_product = get_object_or_404(models.CartProduct, id=pk)
    cart_product.count += 1
    cart_product.save()
    return HttpResponse('')


def cart_decrement(request: HttpRequest, pk: int) -> HttpResponse:
    cart_product = get_object_or_404(models.CartProduct, id=pk)
    cart_product.count -= 1
    if cart_product.count == 0:
        cart_product.delete()
    else:
        cart_product.save()
    return HttpResponse('')


def cart_delete(request: HttpRequest, pk: int) -> HttpResponse:
    get_object_or_404(models.CartProduct, id=pk).delete()
    return HttpResponse('')


class SearchView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        query = request.GET['query']
        return render(request, 'search.html', {
            'query': query
        })


class CartView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:

        return render(request, 'cart.html', {
            'cart_list': request.user.profile.cart_products.all()
        })


class ComparesView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'compares.html', {
            'compare_list': request.user.profile.compare_products.all()
        })


class FavoritiesView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'favorities.html', {
            'favorite_list': request.user.profile.favorite_products.all()
        })
