from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}

    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


# пользовтельский менеджер
class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):
    # Перечисляемое поле - для поля is_published //// IntegerChoices – для числовых наборов; TextChoices – для строковых наборов.
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, db_index=True, unique=True, validators=[
        MinLengthValidator(5),  # валидаторы для проверки на сервере
        MaxLengthValidator(100),
    ])
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None, blank=True, null=True,
                              verbose_name="Фото")  # поле для файлов
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT,
                                       verbose_name="Статус")  # меняется добавляется choices из-за добавления status'a ДАЛЕЕ позже замено на перебор в булевые згначения для админ панели, чтобы было видно нынешние показали этого поля и можно было выбирать
    cat = models.ForeignKey('Category',
                            on_delete=models.PROTECT,
                            related_name="posts",
                            verbose_name="Категории")  # вторичный ключ для таблицы Category// models.PROTECT - при удалении из первичной таблицы (Category),
    # удалятся все записи из вторичной (Women)
    tags = models.ManyToManyField('TagPost', blank=True, related_name="tags", verbose_name="Тэги")
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL, null=True, blank=True, related_name='wuman',
                                   verbose_name="Муж")
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True,
                               default=None) #для связки с БД пользователей, где get_user_model()-  мы обращаемся к модели User
    # с помощью функции get_user_model(). Это считается предпочтительной практикой для фреймворка Django.
    # ТАКЖЕ для этого в класс addpage добавялется функция для проверки формы, где мы добавялем автора к посту ЖЕНЩИНЫ Women

    objects = models.Manager()  # для сохранения стандартного мендежра, чтобы потом можно было обращаться через objects при создании пользовтаельского менеджера
    published = PublishedModel()  # пользовтельский менеджер - возвращает сразу отфильтрованный qwery_set по правилу в filter

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]
        verbose_name = 'Известные женщины'  # для название в ед.ч. таблицы в admin для самой модели
        verbose_name_plural = 'Известные женщины'  # для название во мн.ч. таблицы в admin для самой модели

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})  # для возврата url каждого экземпляра строки из БД

    # ф-я save автоматически включается при сохранени записи
    # функция чтобы автоматически заполнялся slug. Т.к. мы его запретили редактировать, т.е. он пустой при создании. Он сможет создаться один раз пустым, а
    # второй раз нет, т.к. у нас поле slug должно быть уникальным (unique=True)

    # def save(self, *args, **kwargs):
    #     # self.slug = slugify(self.title , allow_unicode=True) #вместо allow_unicode=True дял перевода толкьо для латиницы,
    #     # тогда можно прописать свою логику (функцию) дял перевода русских в англ
    #     self.slug = slugify(translit_to_eng(self.title))
    #     super().save(*args, **kwargs) #Но есть путь гораздо проще, но он применим только для админ-панели.
    #     # Уберем метод save() из модели Women, а в классе WomenAdmin пропишем следующий атрибут: prepopulated_fields = {"slug": ("title",)}

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    def __str__(self):
        return self.name


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    def __str__(self):
        return self.tag


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)

    def __str__(self):
        return self.name


# модель новой таблицы, в которой будут храниться ссылки на загруженные файл
class UploadFiles(models.Model):
    file = models.FileField(
        upload_to='uploads_model')  # upload_to – каталог, в который будет происходить загрузка файлов
