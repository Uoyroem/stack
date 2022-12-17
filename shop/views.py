from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.views.generic import View, DetailView
from django.http import HttpRequest, HttpResponse
from . import models


class IndexView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        phone_category = models.Category.objects.filter(name='Смартфоны и планшеты').first()
        phone_list = models.Product.objects.filter(category=phone_category)
        return render(request, 'index.html', {
            'phone_list': phone_list
        })
    
    
class ProductDetailView(DetailView):
    model = models.Product
    

def to_compare(request: HttpRequest, id: int) -> HttpResponse:
    product = get_object_or_404(models.Product, id=id)
    if product.compare.contains(request.user.profile):
        product.compare.remove(request.user.profile)
    else:
        if request.user.profile.compare_products.count() >= 4:
            return HttpResponse('Максимальное количество продуктов в сравнений.')
        product.compare.add(request.user.profile)
    return HttpResponse('Добавлен')


def to_favorities(request: HttpRequest, id: int) -> HttpResponse:
    product = get_object_or_404(models.Product, id=id)
    
    if product.favorite.contains(request.user.profile):
        product.favorite.remove(request.user.profile)
    else:
        product.favorite.add(request.user.profile)
    return HttpResponse('Добавлен')
            
    
class SearchView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        query = request.GET['query']
        return render(request, 'search.html', {
            'query': query
        })
        

class CartView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        
        return render(request, 'cart.html')
    
    
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