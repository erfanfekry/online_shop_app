from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'account'
urlpatterns = [

    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('user-register/', views.user_register, name='user-register'),
    path('user-edit/', views.user_edit, name='user-edit'),
    path('change-password/', auth_views.PasswordChangeView.as_view(success_url='done'), name='password_change'),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(success_url='done'), name='password-reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password-reset-done'),
    path('password-reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(success_url='/password-reset/complete'), name='password-reset-confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password-reset-complete'),
    path('send-verification/', views.phone_verification, name='phone-verification'),
    path('code-confirm/', views.code_confirm, name='code-confirm'),
]