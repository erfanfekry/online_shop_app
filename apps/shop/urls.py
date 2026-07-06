from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'shop'

urlpatterns = [
    path('products/', views.product_list, name='product-list'),
    path('products/<slug:category_slug>', views.product_list, name='products-by-category'),
    path('products/sort/<str:sort_type>', views.product_list, name='product-list-by-sort'),
    path('products/<int:product_id>/<slug:product_slug>', views.product_detail, name='product-detail'),
    path('posts/search/', views.search_view, name='search'),
]