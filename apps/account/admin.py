from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import *


@admin.register(ShopUser)
class ShopUserAdmin(UserAdmin):
    form = ShopUserChangeForm
    add_form = ShopUserCreationForm
    model = ShopUser
    list_display = ['phone', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['phone']

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    ordering = ['phone']