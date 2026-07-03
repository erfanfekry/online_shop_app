from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from shop.models import *
from .sms_verification.sms_verification import SendSms


def post_paginator(request, posts):
    paginator = Paginator(posts, 2)
    current_page = request.GET.get('page', 1)

    try:
        posts = paginator.page(current_page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = []
    return posts, paginator


def product_list(request, category_slug=None, sort_type=None):

    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        category = categories.get(slug=category_slug)
        products = products.filter(category=category)
    if sort_type:
        for slug in Category.objects.values_list('slug'):
            if f'/products/{slug[0]}' in request.META.get('HTTP_REFERER', '/'):
                category = categories.get(slug=slug[0])
                products = products.filter(category=category)
        if sort_type == 'most_expensive':
            products = products.order_by('-price')
        elif sort_type == 'least_expensive':
            products = products.order_by('price')
        elif sort_type == 'oldest':
            products = products.order_by('created')
        elif sort_type == 'newest':
            products = products.order_by('-created')

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page', 1)

    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(paginator.num_pages)
    except EmptyPage:
        products = []

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'shop/product_list_ajax.html', {'products': products})
    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, product_id, product_slug):
    product = get_object_or_404(Product, id=product_id, slug=product_slug)
    category = product.category
    related_products = Product.objects.filter(category__name=category.name).exclude(id=product_id).all()[:5]

    print('related_products: ', related_products, '\n', 'category: ', category)
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'shop/product_detail.html', context)


@login_required
def search_view(request, pagination=True):
    paginator = None
    query = request.GET.get('query', '')
    if query != '':
        results1 = Product.objects.annotate(similarity=TrigramSimilarity('tags__name', query)).filter(
            similarity__gt=0.3)
        results2 = (Product.objects.annotate(similarity=TrigramSimilarity('description', query)).
                    filter(similarity__gt=0.1))
        posts = (results1 | results2).select_related('author').distinct()

        if pagination:
            posts, paginator = post_paginator(request, posts)
        context = {
            'query': query,
            'posts': posts,
            'paginator': paginator
        }
        return render(request, 'shop/product_list.html', context)
    else:
        return redirect(request.META.get('HTTP_REFERER'))

