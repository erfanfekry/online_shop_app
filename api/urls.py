from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('users', views.UserViewSet)

app_name='api'
urlpatterns = [
    # path('products/', views.ProductListAPIView.as_view(), name='product-list-api'),
    # path('product/<pk>/', views.DetailListAPIView.as_view(), name='detail-list-api'),
    # path('users/', views.UserViewSet.as_view(), name='user-list-api'),
    # path('register/', views.UserRegisterAPIView.as_view(), name='user-register-api'),
    path('', include(router.urls)),
    path('orders/', views.OrderListAPIView.as_view(), name='orders_list_api'),
    path('orders/<pk>/', views.OrderRetrieveAPIView.as_view(), name='orders_detail_api'),



]
