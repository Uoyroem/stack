from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import View, DetailView
from django.http import HttpRequest
from . import models


class IndexView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        phone_category = get_object_or_404(models.Category, name='Смартфоны и планшеты')
        phone_list = get_list_or_404(models.Product, category=phone_category)
        return render(request, 'index.html', {
            'phone_list': phone_list
        })
    
    
class ProductDetailView(DetailView):
    model = models.Product