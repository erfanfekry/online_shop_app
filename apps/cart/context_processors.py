from .cart import Cart
from apps.shop.models import Product
from django.shortcuts import get_object_or_404

def cart(request):
    return {'cart': Cart(request)}