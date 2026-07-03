from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action
from .permissions import *

from .serializers import *


# class ProductListAPIView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#
# class DetailListAPIView(generics.RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# class UserAPIView(APIView):
#     authentication_classes = [BasicAuthentication]
#     # permission_classes = [IsAuthenticated]
#     # permission_classes = [AllowAny]
#     def get(self, request, *args, **kwargs):
#         users = ShopUser.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)
#
# class UserRegisterAPIView(generics.CreateAPIView):
#     permission_classes = [AllowAny]
#     queryset = ShopUser.objects.all()
#     serializer_class = UserRegisterSerializer

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(methods=['GET'], detail=False, url_path='get_discounted_products', url_name='get_discounted_products')
    def discounted_products(self, request):
        discount_param =request.query_params.get('discount', 0)
        try:
            int(discount_param)
        except:
            return Response('Invalid value for discount query parameter', status=400)

        products = self.queryset.filter(discount__gt=discount_param)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = ShopUser.objects.all()
    serializer_class = UserSerializer

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminKhorasani]

class OrderRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsBuyer]