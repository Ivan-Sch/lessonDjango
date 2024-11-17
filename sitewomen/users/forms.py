from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


    class Meta:
        model = get_user_model()  # получаем модель User с помощью стандартной функции get_user_model().
        #Это рекомендуемая практика на случай изменения модели. Тогда в программе ничего дополнительно
        # менять не придется.
        fields = ['username', 'password'] #отображать в форме поля username и password


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    # ДОП вылидация. ПРОИСХОДИТ ПРИ ПРОВВЕРКИ is_valid() в функ-ии представления,
    # автоматически вызываются при проверке корректности переданных данных
    # def clean_password2(self): #проверка равенства двух паролей
    #     cd = self.cleaned_data
    #     if cd['password'] != cd['password2']:
    #         raise forms.ValidationError("Пароли не совпадают!")
    #     return cd['password2']  УБРАЛИ ПОТОМУ ЧТО ИСПОЛЬЗУЕТСЯ НАСЛДЕОВАНИЕ ОТ UserCreationForm(автоматом проверяет), А если было от forms.ModelForm, то использовали.


    def clean_email(self): #проверка уникальности email в БД
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email
