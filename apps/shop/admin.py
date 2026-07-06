from django.contrib import admin
from .models import *

class ImageInline(admin.TabularInline):
    model = Image
    extra = 0

class FeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'inventory', 'category', 'new_price', 'created']
    prepopulated_fields = {'slug':('name',)}
    search_fields = ['name', 'category__name', 'created']
    inlines = [ImageInline, FeatureInline]
