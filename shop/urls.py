from django.urls import path, include
from . import views

product_urlpatterns = [
    path('detail', views.ProductDetailView.as_view(),  name='product_detail'),
    path('to-favorite', views.to_favorities,  name='to_favorite'),
    path('to-compare', views.to_compare, name='to_compare')
]

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('product/<int:pk>/', include(product_urlpatterns),  name='product'),
    path('search', views.SearchView.as_view(), name='search'),
    path('cart', views.CartView.as_view(), name='cart'),
    path('favorities', views.FavoritiesView.as_view(), name='favorities'),
    path('compares', views.ComparesView.as_view(), name='compares')
]
