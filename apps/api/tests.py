from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse, resolve
import pytest
from .factory import *



@pytest.fixture
def api_client():
    return APIClient()


def test_get_product_list_success(db, api_client):
    user = UserFactory.build()
    api_client.force_authenticate(user)
    products = ProductFactory.create_batch(3, name=['p1', 'p2', 'p3'])
    url = reverse('api:product-list')
    response = api_client.get(url)

    from apps.api.serializers import ProductSerializer
    assert response.status_code == status.HTTP_200_OK
    assert 'results' in response.data
    expected_data = ProductSerializer(products, many=True).data
    assert sorted(response.data['results'], key=lambda x:x['id']) == \
           sorted(expected_data, key=lambda x:x['id'])

def test_product_list_schema(db, api_client):
    user = UserFactory.build()
    api_client.force_authenticate(user)
    ProductFactory.create_batch(1)
    url = reverse('api:product-list')
    response = api_client.get(url)
    item = response.data['results'][0]

    assert isinstance(item['id'], int)
    assert isinstance(item['name'], str)
    assert isinstance(item['new_price'], int)

def test_get_product_list_empty(db, api_client):
    user = UserFactory.build()
    api_client.force_authenticate(user)
    url = reverse('api:product-list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['results'] == []

def test_product_list_filtering_and_signal(db, api_client):
    user = UserFactory.build()
    api_client.force_authenticate(user)
    ProductFactory.create_batch(1, name="Galaxy A51", price=1000, discount=200)
    ProductFactory.create_batch(1, name="Xiaomi Redmi 9")
    url = reverse('api:product-list')
    response = api_client.get(f'{url}?search="Galaxy A51"')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['name'] == 'Galaxy A51'
    assert response.data['results'][0]['new_price'] == 800