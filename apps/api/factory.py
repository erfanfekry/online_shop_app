import factory
from apps.account.models import ShopUser
from apps.shop.models import *
from apps.order.models import *


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShopUser
    phone = factory.Faker('numerify', text='091########') #type: ignore

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    name = factory.Faker('word')
    slug = factory.Faker('word')

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    category = factory.SubFactory(CategoryFactory)
    name = factory.Faker('word')
    slug = factory.Faker('word')
    description = factory.Faker('sentence')
    inventory = factory.Faker('random_int', min=1, max=200)
    price = factory.Faker('random_int', min=10**4, max=10**7)
    weight = factory.Faker('random_int', min=1000, max=50000)
    discount = factory.Faker('random_int', min=1000, max=500000)

class OrderFactory():
    class Meta:
        model = Order
    buyer = factory.SubFactory(UserFactory)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('first_name')
    phone = factory.Faker('numerify', text='091########') #type: ignore
    address = factory.Faker('address')
    postal_code = factory.Faker('postal_code')
    province = factory.Faker('province')
    city =  factory.Faker('city')

