from apps.shop.models import Product
from copy import deepcopy
class Cart:
    def __init__(self,  request):
        self.session = request.session
        cart = request.session.get('cart')
        if not cart:
            cart = request.session['cart'] = {}
        self.cart = cart


    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'price': product.new_price, 'weight': product.weight}
        else:
            if product.inventory >= self.cart[product_id]['quantity']:
                self.cart[product_id]['quantity'] += 1
        self.save()

    def decrease(self, product):
        product_id = str(product.id)
        if self.cart[product_id]['quantity'] > 1:
            self.cart[product_id]['quantity'] -= 1
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def clear(self):
        del self.session['cart']
        self.save()

    def get_post_price(self):
        total_weight = sum(item['weight'] * item['quantity'] for item in self.cart.values())
        if total_weight < 1000:
            return 25000
        elif 1000 <= total_weight <= 5000:
            return 50000
        else:
            return 100000

    def get_total_price(self):
        total_price = sum(int(item['price']) * int(item['quantity']) for item in self.cart.values())
        return total_price

    def get_final_price(self):
        final_price = int(self.get_post_price()) + int(self.get_total_price())
        return final_price

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        product_dict = {str(product.id): product for product in products}
        for product_id, items in self.cart.items():
            product = product_dict.get(product_id)
            if product:
                quantity = int(items.get('quantity'))
                price = int(product.new_price)
                weight = int(items.get('weight'))
                yield {
                    'quantity': quantity,
                    'price': price,
                    'weight': weight,
                    'product': product,
                    'total': price * quantity
                }

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        self.session.modified = True
