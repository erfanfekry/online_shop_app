from django.db import models
from django.urls import reverse
from django_resized import ResizedImageField


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name='نام')
    slug = models.SlugField(max_length=250, unique=True)

    class Meta  :
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:products-by-category', kwargs={'category_slug': self.slug})


class ProductFeature(models.Model):
    features = models.ForeignKey('Product', related_name='features', on_delete=models.CASCADE, verbose_name='ویژگی ها')
    name = models.CharField(max_length=250, verbose_name='ویژگی')
    value = models.CharField(max_length=250, verbose_name='مقدار')

    def __str__(self):
        return self.name + ': ' + self.value

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='دسته بندی')
    name = models.CharField(max_length=250, verbose_name='نام')
    slug = models.SlugField(max_length=250, unique=True, verbose_name='اسلاگ')
    description = models.TextField(max_length=3000, verbose_name='توضیحات')
    inventory = models.PositiveIntegerField(default=0, verbose_name='موجودی')
    price = models.PositiveIntegerField(default=0, verbose_name='قیمت')
    weight = models.PositiveIntegerField(default=0, verbose_name='وزن')
    discount = models.PositiveIntegerField(default=0, verbose_name='تخفیف')
    new_price = models.PositiveIntegerField(default=0, verbose_name='قیمت پس از تخفیف')
    created = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='بروزرسانی')

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['id', 'slug']),
                   models.Index(fields=['name']),
                   models.Index(fields=['-created'])
                   ]
        verbose_name = 'محصول'
        verbose_name_plural = 'محصول ها'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product-detail', kwargs={'product_id': self.id, 'product_slug': self.slug})

class Image(models.Model):
    post = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=1000, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image_file = ResizedImageField(size=[800, 800], upload_to='product_images/%Y%m%d')

    def __str__(self):
        return self.title if self.title else 'None'

    class Meta:
        ordering = ['title']
        indexes = [models.Index(fields=['title'])]

    verbose_name = 'تصویر'
    verbose_name_plural = 'تصویر ها'






