import pytest
from apps.account.models import ShopUser
from .views import *


# Test data were generated manually (case1: instead of using factory boy)
@pytest.fixture
def user(db):
    return ShopUser.objects.create_user(phone='123456789')

@pytest.fixture
def category(db, user):
        category1 =  Category.objects.create(name='Home Appliances', slug='home-appliances')
        category2 =  Category.objects.create(name='Shoes', slug='shoes')
        return list([category1, category2])

@pytest.fixture
def products(db, category):
    product1 = Product.objects.create(category=category[0], name= 'Unique Kettle', slug='unique-kettle' ,
                                      description='Full steel unique kettle', inventory=150,
                                      price=1500000, weight=750, discount=0)

    product2 = Product.objects.create(category=category[1], name='Adidas', slug='adidas',
                                      description='Samba Original', inventory=300,
                                      price=3000000, weight=600, discount=250000)
    return list([product1, product2])

def test_product_list_no_category(db, client, products):
    url = reverse('shop:product-list')
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.context['products']) == 2

def test_product_list_with_category(db, client, category, products):
    url = reverse('shop:products-by-category', kwargs={'category_slug':'home-appliances'})
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.context['products']) == 1
    assert response.context['products'][0].category == category[0]

def test_product_list_template_context_data(db, client, user, products):
    client.force_login(user)
    url = reverse('shop:product-list')
    response = client.get(url)

    assert 'products' in response.context
    assert len(response.context['products']) == 2

@pytest.mark.django_db
def test_detail_url_exists(client, user, products):
    client.force_login(user)
    url = reverse('shop:product-detail', kwargs={'product_id': products[0].id,'product_slug': products[0].slug})
    response = client.get(url)

    assert response.status_code == 200

def test_detail_url_does_not_exist(client, user, products):
    client.force_login(user)
    url = reverse('shop:product-detail', kwargs={'product_id': 999999,'product_slug': 'foo'})
    response = client.get(url)

    assert response.status_code == 404

def test_template_exists(db, client, user, products):
    client.force_login(user)
    url = reverse('shop:product-list')
    response = client.get(url)

    assert response.status_code == 200
    assert 'shop/product_list.html' in [t.name for t in response.templates]
    assert 'products' in response.context
    assert set(response.context['products']) == set(products)
