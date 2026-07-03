from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'shop'

urlpatterns = [
    path('products/', views.product_list, name='product-list'),
    path('products/<slug:category_slug>', views.product_list, name='products-by-category'),
    path('products/sort/<str:sort_type>', views.product_list, name='product-list-by-sort'),
    path('products/<int:product_id>/<slug:product_slug>', views.product_detail, name='product-detail'),
    path('posts/search/', views.search_view, name='search'),

    # path('profile/', views.profile, name='profile'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
#     path('posts/comment/<int:post_id>', views.comment_view, name='comment'),
#     path('posts/edit/<int:post_id>', views.edit_post, name='edit-post'),
#     path('post/delete-post/<int:post_id>', views.delete_post, name='delete-post'),
]