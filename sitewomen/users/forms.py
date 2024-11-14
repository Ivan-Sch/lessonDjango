from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class LoginUserForm(AuthenticationForm):
        class Meta:
            model = get_user_model()  # получаем модель User с помощью стандартной функции get_user_model().
            #Это рекомендуемая практика на случай изменения модели. Тогда в программе ничего дополнительно
            # менять не придется.
            fields = ['username', 'password'] #отображать в форме поля username и password