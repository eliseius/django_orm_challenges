"""
В этом задании вам предстоит работать с моделью поста в блоге. У него есть название, текст, имя автора, статус
(опубликован/не опубликован/забанен), дата создания, дата публикации, категория (одна из нескольких вариантов).

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими ноутбуками для облегчения тестирования
- реализовать у модели метод to_json, который будет преобразовывать объект книги в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""
from django.http import HttpRequest, HttpResponse, JsonResponse
from challenges.models import PostBlog

import datetime


def last_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть 3 последних опубликованных поста.
    """
    published_posts = PostBlog.objects.filter(status='pb')[:3]
    return HttpResponse([published_post.to_json() for published_post in published_posts])


def posts_search_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты, которые подходят под поисковый запрос.
    Сам запрос возьмите из get-параметра query.
    Подходящесть поста можете определять по вхождению запроса в название или текст поста, например.
    """
    posts_with_query = PostBlog.objects.filter(text_post__icontains=request.GET['query'])
    return HttpResponse([post.to_json() for post in posts_with_query])


def untagged_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты без категории, отсортируйте их по автору и дате создания.
    """
    posts_without_category = PostBlog.objects.filter(category__isnull=True).order_by('author_name', 'created_at')
    return HttpResponse([post.to_json() for post in posts_without_category])


def categories_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты все посты, категория которых принадлежит одной из указанных.
    Возьмите get-параметр categories, в нём разделённый запятой список выбранных категорий.
    """
    list_categories = request.GET['categories'].split(',')
    posts_categories = PostBlog.objects.filter(category__in=list_categories)
    return HttpResponse([post.to_json() for post in posts_categories])


def last_days_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть посты, опубликованные за последние last_days дней.
    Значение last_days возьмите из соответствующего get-параметра.
    """
    try:
        last_days = int(request.GET['last_days'])
    except (ValueError, KeyError):
        return HttpResponse(status=404)

    date_for_filter = datetime.datetime.now() - datetime.timedelta(days=last_days)
    posts = PostBlog.objects.filter(status='pb',publication_date__gte=date_for_filter)
    return HttpResponse([post.to_json() for post in posts])
