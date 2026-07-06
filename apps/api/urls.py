from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('users', views.UserViewSet)

app_name='api'
urlpatterns = [
    path('', include(router.urls)),
    path('orders/', views.OrderListAPIView.as_view(), name='orders_list_api'),
    path('orders/<pk>/', views.OrderRetrieveAPIView.as_view(), name='orders_detail_api'),



]
