from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import View, DetailView
from django.http import HttpRequest, HttpResponse
from . import models


class IndexView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        # phone_category = get_object_or_404(models.Category, name='Смартфоны и планшеты')
        # phone_list = get_list_or_404(models.Product, category=phone_category)
        return render(request, 'index.html', {
            'phone_list': None
        })
    
    
class ProductDetailView(DetailView):
    model = models.Product
    
    
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
        return render(request, 'compares.html')
    

class FavoritiesView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'favorities.html')