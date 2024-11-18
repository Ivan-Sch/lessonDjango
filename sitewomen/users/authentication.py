from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

# Бэкенд аунтификация по е-маил и паролю
# authenticate() – непосредственно аутентификация по username и password; возвращается объект пользователя, либо None, если он не был найден;
# get_user() – получение объекта пользователя по идентификатору.
class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs): #username = ссылка на наш записанный E-mail
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None

    # Нужен чтобы был виден пользователь
    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None #Теперь, при вводе E-mail и пароля пользователь будет авторизован и отображен на панели главного меню.
            # Вот так в Django очень просто можно создавать свои собственные бэкенды авторизации пользователей на сайте.