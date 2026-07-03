from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from .cart import Cart
from shop.models import *

@require_POST
def add_to_cart(request, product_id):
    try:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product)
        item_count = len(cart)
        total_price = cart.get_total_price()

        response_data={
            'item_count': item_count,
            'total_price': total_price,
        }
    except:
        response_data = {'error': 'invalid request'}

    return JsonResponse(response_data)

def cart_detail(request):
    cart = request.session.get('cart')
    if cart:
        for pid, item in cart.items():
            product = get_object_or_404(Product, id=pid)
            new_price = product.new_price
            cart[pid]['price'] = new_price
            request.session['cart'] = cart
            request.session.modified = True
    cart = Cart(request)
    print('cart: ', cart.cart)
    return render(request, 'cart/cart_detail.html', {'mycart':cart})
#
def update_quantity(request):
    action = request.POST.get('action')
    item_id = request.POST.get('item-id')

    try:
        product = get_object_or_404(Product, id=item_id)
        cart = Cart(request)
        if action == 'add':
            cart.add(product)
        if action == 'decrease':
            cart.decrease(product)

        response_data = {
            'success': True,
            'total_price': cart.get_total_price(),
            'quantity': cart.cart[item_id]['quantity'],
            'total' : cart.cart[item_id]['price'] * cart.cart[item_id]['quantity'],
            'final_price': cart.get_final_price()
        }
        print('response data: ', response_data)
        return JsonResponse(response_data)
    except:
        return JsonResponse({'success': False, 'Error': 'item not found'})
    return None


def remove_from_cart(request):
    item_id = str(request.POST.get('item-id'))
    try:
        product = get_object_or_404(Product, id=item_id)
        cart=Cart(request)
        cart.remove(product)

        response_data = {
            'success': True,
            'item_count': len(cart),
            'total_price': cart.get_total_price(),
            'final_price': cart.get_final_price(),
        }
        print(response_data)
    except:
        response_data = {
            'success': False,
            'Error': 'Cannot remove item from cart.'}
    print(response_data)
    return JsonResponse(response_data)



    # def clear_cart(request):
#     cart =  request.session.get('cart')
#     if cart:
#         cart.clear()
#     cart = Cart(request)
#     item_count = len(cart)
#     total_price = cart.get_total_price()
#
#     response_data = {
#         'item_count': item_count,
#         'total_price': total_price,
#     }
#
#     return JsonResponse(response_data)

