from django.db import models
from django.urls import reverse


# пользовтельский менеджер
class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=1)


class Women(models.Model):
    # Перечисляемое поле - для поля is_published //// IntegerChoices – для числовых наборов; TextChoices – для строковых наборов.
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices,
                                       default=Status.DRAFT)  # меняется добавляется choices из -за добавления status'a
    cat = models.ForeignKey('Category',
                            on_delete=models.PROTECT)  # вторичный ключ для таблицы Category// models.PROTECT - при удалении из первичной таблицы (Category), удалятся все записи из вторичной (Women)

    objects = models.Manager()  # для сохранения стандартного мендежра, чтобы потом можно было обращаться через objects
    published = PublishedModel()  # пользовтельский менеджер - возвращает сразу отфильтрованный qwery_set по правилу в filter

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})  # для возврата url каждого экземпляра строки из БД

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    def __str__(self):
        return self.name
