from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('product/<int:id>/detail', views.ProductDetailView.as_view(),  name='product_detail'),
    path('product/<int:id>/to-favorite', views.to_favorities,  name='to_favorite'),
    path('search', views.SearchView.as_view(), name='search'),
    path('cart', views.CartView.as_view(), name='cart'),
    path('favorities', views.FavoritiesView.as_view(), name='favorities'),
    path('compares', views.ComparesView.as_view(), name='compares')
]
