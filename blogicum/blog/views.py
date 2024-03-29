from datetime import datetime

import pytz
from django.shortcuts import get_list_or_404, get_object_or_404, render

from blog.models import Category, Post
from blogicum.constants import const


def index(request):
    """Главная страница Блогикума."""
    template = 'blog/index.html'
    post_list = Post.objects.select_related(
        'location',
        'category',
        'author'
    ).filter(
        pub_date__lte=datetime.now(tz=pytz.timezone('Europe/Moscow')),
        is_published=True, category__is_published=True
    )[:const.PAGE_LIMIT]
    context = {
        'post_list': post_list
    }
    return render(request, template, context)


def post_detail(request, id):
    """Полный текст записи из ленты Блогикума."""
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.select_related(
            'location',
            'category',
            'author'
        ).filter(
            pub_date__lte=datetime.now(tz=pytz.timezone('Europe/Moscow')),
            is_published=True,
            category__is_published=True,
            pk=id
        )
    )
    context = {
        'post': post
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    """Список постов определенной категории."""
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug
    )
    post_list = get_list_or_404(
        Post.objects.select_related(
            'location',
            'category',
            'author'
        ).filter(
            category_id=category.id,
            is_published=True,
            pub_date__lte=datetime.now(tz=pytz.timezone('Europe/Moscow')),
            category__is_published=True
        )
    )
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template, context)
