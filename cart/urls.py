from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('cart-detail/', views.cart_detail, name='cart-detail'),
    path('update-quantity/', views.update_quantity, name='update-quantity'),
    path('remove/', views.remove_from_cart, name='remove-from-cart'),


]