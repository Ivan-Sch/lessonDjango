from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
# расширить существующую модель User    НАДО ЕЩЕ ПРОПИСАТЬ AUTH_USER_MODEL = 'users.User' В settings.py
class User(AbstractUser):
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография")
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name="Дата рождения")
