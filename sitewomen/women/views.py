from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from .forms import AddPostForm
from .models import Women, Category, TagPost

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


def index(request):
    posts = Women.published.all().select_related('cat')
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'women/index.html', context=data)


def about(request):
    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu})


def show_post(request, post_slug):
    post = get_object_or_404(Women,
                             slug=post_slug)  # возвращает запись (объект) из таблицы БД (в данном случае по слагу равным...), если она есть, иначе генерируется исключение 404 - страница не найдена

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }

    return render(request, "women/post.html", data)


def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid(): #проверяет поля на корректность заполнения
            try:
                Women.objects.create(
                    **form.cleaned_data)  # поля названия формы должны совадать с полями модели, чтобы можно было их раскрыть при не связоной с моделью
                return redirect('home')  # после отпарвления данных выходим на главную страницу
            except Exception as e:
                print(e)
                form.add_error(None, 'Ошибка добавления поста')
    else:
        form = AddPostForm()
    data = {'menu': menu, 'title': 'Добавление статьи', 'form': form}

    return render(request, 'women/addpage.html', data)


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk).select_related('cat')

    data = {
        'title': f'Отображение по {category.name}',
        'menu': menu,
        'posts': posts,
        # пользовтельский менеджер - возвращает сразу отфильтрованный qwery_set по правилу в filter----- в данном случае выведуся все записи с паблишед = 1, но мы можем еще раз отфилтровать
        'cat_selected': category.pk,
    }
    return render(request, 'women/index.html', context=data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED)  # обращение к объектам (к постам) данного тэга

    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }

    return render(request, 'women/index.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
