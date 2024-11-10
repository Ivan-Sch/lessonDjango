from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from .forms import AddPostForm, UploadFileForm
from .models import Women, Category, TagPost, UploadFiles
from .utils import DataMixin

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


# def index(request):
#     posts = Women.published.all().select_related('cat')
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#     return render(request, 'women/index.html', context=data)

# ЗАМЕНА index представления:
# class WomenHome(TemplateView):
#     template_name = 'women/index.html'
#     # extra_context = {  # для стаического пути на момент прихода страница
#     #     'title': 'Главная страница',
#     #     'menu': menu,
#     #     'posts': Women.published.all().select_related('cat'),
#     #     'cat_selected': 0,
#     # }
#     #
#     # можно передавать и статические и динамические данные обработки: Если теперь попробовать поменять значения cat_id
#     # в GET-запросе, то будем видеть подсветку различных разделов. Правда, само
#     # содержимое будет оставаться прежним, т.к. мы этот функционал здесь
#     # не прописывали. Я лишь хотел показать отличия между методом get_context_data() и атрибутом extra_context.
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Главная страница'
#         context['menu'] = menu
#         context['posts'] = Women.published.all().select_related('cat')
#         context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
#         return context


# ЗАМЕНА index на класс от ListView - связка с таблицей БД
class WomenHome(DataMixin, ListView):
    # model = Women #указыватся модель из которой будут браться записи, но тогда будут все данные из этой модели (черновики тоже),
    # но нам надо паблишды, используеься метод   def get_queryset(self)

    # Шаблон для данного представления берется по правилу:
    # <имя приложения>/<имя модели>_list.html ----- women/women_list.html
    template_name = 'women/index.html'  # но у нас другой шаблон, поэтому явно указываем

    # Для отображения данных которые передается в шаблон (В нем используется posts), ListView формирует сам {% for p in object_list %}, вместо {% for p in posts %} как было до этого
    context_object_name = 'posts'  # хранит в перменной 'posts' возвращенный get_queryset(self), как в ф-ии data = {'posts': posts} - это тот же'posts', а также хранит данные через model = Women
    title_page = 'Главная страница'
    cat_selected = 0
    # который передается в шаблон ТАКЖЕ ЭТО object_list

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница' 
    #     context['menu'] = menu
    #     context['cat_selected'] = 0
    #     return context
    #

    # ДЛЯ DataMixin
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     return self.get_mixin_context(super().get_context_data(**kwargs),
    #                                   title='Главная страница',
    #                                   cat_selected=0,
    #                                   )

    def get_queryset(self):
        return Women.published.all().select_related('cat')


# функция для сохранения файла
def handle_uploaded_file(f):
    with open(f"uploads/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def about(request):
    # if request.method == "POST":
    #     form = UploadFileForm(request.POST, request.FILES)  # т.к. работает с фалйми то ипшется второй аргумент
    #     if form.is_valid():
    #         # # ДЛЯ НЕ СВЯЗАННОЙ ФОРМЫ С МОДЕЛЬЮ (2 способа)
    #         # 1 способ когда не згаржуем в БД
    #         # handle_uploaded_file(request.FILES['file'])  # для сохранения файла на сервер c не связанной таблицей
    #         # # "files", потому что в форме у нас поле files, если бы было без формы, то смотрели бы на about.html name="file_upload">
    #
    #         # 2 способ когда загружем в БД
    #         fp = UploadFiles(file=form.cleaned_data[
    #             'file'])  # UploadFiles - модель. СОХРАНЕНИЕ бдует в upload_to – каталог т .к. указалив самой модели,
    #         # если мы хотим загружать в общую папку то в конфигирации MEDIA_ROOT = BASE_DIR / 'media'
    #         fp.save()
    #
    # else:
    #     form = UploadFileForm()
    contact_list = Women.published.all()
    paginator = Paginator(contact_list, 3)  # делаем пигинацию из 3 страниц (разбивка) из списка contact_list
    print(request.GET)
    page_number = request.GET.get('page')
    # page_number= paginator.page(page_number) #можно так

    page_obj = paginator.get_page(page_number)  # получаем объект текущей страницы по номеру
    # page_obj = page_number.object_list #можно так

    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu, 'page_obj': page_obj})


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


# замена show_post на КЛАСС для отдельного поста
class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'  # DetailView ищет записи в модели по pk or slug указанный в URL, но у нашего URL slug другой - таким образом мы определяем, который в urls
    context_object_name = 'post'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     print(context)
    #     context['title'] = context['post']
    #     context['menu'] = menu
    #     return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context,
                                      title=context['post']
                                      )

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[
            self.slug_url_kwarg])  # если бы не было self.slug_url_kwarg, то можно было бы указать как в URl слаг 'post_slug'


# def addpage(request):
#     if request.method == 'POST':
#         print(request.POST)
#         form = AddPostForm(request.POST, request.FILES) #т.к. идет работа сохранея файлов , то надо добавить request.FILES
#
#         if form.is_valid():  # проверяет поля на корректность заполнения
#             form.save()  # - для связанной формы с моделью можно напрямую сохрянть данные в БД
#             return redirect('home')
#             # для формы не связнной делается так:
#             # try:
#             #     Women.objects.create(
#             #         **form.cleaned_data)  # поля названия формы должны совадать с полями модели, чтобы можно было их раскрыть при не связоной с моделью
#             #     return redirect('home')  # после отпарвления данных выходим на главную страницу
#             # except Exception as e:
#             #     print(e)
#             #     form.add_error(None, 'Ошибка добавления поста')
#     else:
#         form = AddPostForm()
#     data = {'menu': menu, 'title': 'Добавление статьи', 'form': form}
#
#     return render(request, 'women/addpage.html', data)

# ЗАМЕНА addpage НА КЛАСС ПРЕДСТАВЛЕНИЯ
# class AddPage(View):
#     def get(self, request):
#         form = AddPostForm()
#         return render(request, 'women/addpage.html', {'menu': menu, 'title': 'Добавление статьи', 'form': form})
#
#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#
#         return render(request, 'women/addpage.html', {'menu': menu, 'title': 'Добавление статьи', 'form': form})

# ЗАМЕНА AddPage(View) на FormView

# class AddPage(FormView):
#     form_class = AddPostForm #указываеься имя формы
#     template_name = 'women/addpage.html'
#     success_url = reverse_lazy('home') # Для перенаправления после отправки формы. reverse(). Она пытается
#     # построить маршрут по имени 'home', но этот маршрут на момент формирования класса AddPage не определен.
#     # В таких ситуациях следует пользоваться другой аналогичной функцией reverse_lazy()
#     extra_context = {
#         'menu': menu,
#         'title': 'Добавление статьи',
#     }
#
#     # Для сохраения данных в БД Этот метод вызывается только после успешной проверки всех переданных данных
#     # формы. Параметр form – это ссылка на заполненную форму.
#     # Так как метод form_valid() вызывается после проверки данных, то в нем доступен словарь form.cleaned_data
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)

# ЗАМЕНА AddPage(FormView) на CreateView
class AddPage(DataMixin, CreateView):  # обращение к форме в html через form
    form_class = AddPostForm  # он берет сам автоматически , если прописывать модель
    # model = Women
    # fields = '__all__' #или данные ['title', 'slug', 'content', 'is_published', 'cat'] вводятся все поля которые обязательные в model

    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = "Добавление статьи"


# ДЛЯЯ ОБНОВЛЕНИЯ ДАННЫХ в БД
class UpdatePage(DataMixin, UpdateView):
    model = Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'


# ДЛЯ УДАЛЕНИЯ ДАННЫХ ИЗ БД
class DeletePage(DataMixin, DeleteView):
    model = Women
    template_name = 'women/deletepage.html'
    success_url = reverse_lazy('home')
    title_page = 'Удаление статьи'


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts = Women.published.filter(cat_id=category.pk).select_related('cat')
#
#     data = {
#         'title': f'Отображение по {category.name}',
#         'menu': menu,
#         'posts': posts,
#         # пользовтельский менеджер - возвращает сразу отфильтрованный qwery_set по правилу в filter----- в данном случае выведуся все записи с паблишед = 1, но мы можем еще раз отфилтровать
#         'cat_selected': category.pk,
#     }
#     return render(request, 'women/index.html', context=data)

# ЗАмена show_category на класс
class WomenCategory(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'  # хранит в перменной 'posts' возвращенный get_queryset(self), как в ф-ии data = {'posts': posts} - это тот же'posts',
    # который передается в шаблон ТАКЖЕ ЭТО object_list

    allow_empty = False  # если указать несуществующий слаг, то увидим пустую страницу, а нам бы хотелось увидеть ошибку 404 – страница не найдена.

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     cat = context['posts'][0].cat
    #     context['title'] = 'Категория - ' + cat.name
    #     context['menu'] = menu
    #     context['cat_selected'] = cat.id
    #
    #     return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected=cat.id)

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')  # cat_slug' -  bp URLs


# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#
#     posts = tag.tags.filter(is_published=Women.Status.PUBLISHED)  # обращение к объектам (к постам) данного тэга
#
#     data = {
#         'title': f'Тег: {tag.tag}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,
#     }
#
#     return render(request, 'women/index.html', context=data)

# ЗАМЕНА show_tag_postlist
class WomenTags(DataMixin, ListView):  # url 'tag/<slug:tag_slug>/'
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Тег - ' + self.kwargs['tag_slug']
    #     context['menu'] = menu
    #     context['cat_selected'] = None
    #     return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title='Тег - ' + self.kwargs['tag_slug'])


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
