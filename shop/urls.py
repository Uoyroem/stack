from django.urls import path, include
from . import views

cart_urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('<int:pk>/increment', views.cart_increment, name='cart_increment'),
    path('<int:pk>/decrement', views.cart_decrement, name='cart_decrement')
]

product_urlpatterns = [
    path('detail', views.ProductDetailView.as_view(),  name='product_detail'),
    path('to-favorite', views.to_favorities,  name='to_favorite'),
    path('to-compare', views.to_compare, name='to_compare'),
    path('to-cart', views.to_cart, name='to_cart')
]

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('product/<int:pk>/', include(product_urlpatterns),  name='product'),
    path('search', views.SearchView.as_view(), name='search'),
    path('cart', include(cart_urlpatterns)),
    path('favorities', views.FavoritiesView.as_view(), name='favorities'),
    path('compares', views.ComparesView.as_view(), name='compares')
]
