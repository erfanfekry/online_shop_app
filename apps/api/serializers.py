from rest_framework import serializers

from apps.account.models import ShopUser
from apps.shop.models import *
from apps.order.models import *

class ProductFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ['name', 'value']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class ProductSerializer(serializers.ModelSerializer):
    features = ProductFeaturesSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'new_price', 'category', 'features']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopUser
        fields = ['id', 'first_name', 'last_name', 'phone', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = ShopUser(phone=validated_data['phone'],
                        first_name=validated_data['first_name'],
                        last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopUser
        fields = ['phone', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only':True}
        }
    def create(self, validated_data):
        user = ShopUser(phone=validated_data['phone'],
                        first_name=validated_data['first_name'],
                        last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
