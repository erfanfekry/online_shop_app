from . import views
from django.urls import path

app_name = 'order'

urlpatterns = [
    path('make-order/', views.make_order, name='make-order'),
    path('request/', views.send_request, name='request'),
    path('verify/', views.verify, name='verify'),

]
