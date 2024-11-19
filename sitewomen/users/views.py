from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm


# def login_user(request):
#     if request.method == 'POST':
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             #делаем аунтификацию - сравниваем с БД с полями username и  password (красные) - ЭТО ОБЪЕКТ ЗАПИСИ ПОЛЬЗОВТАЕЛЯ
#             if user and user.is_active:
#                 login(request, user) # авторизация - создает запись в сессии, авторизуя текущего пользователя на сайте
#                 return HttpResponseRedirect(reverse('home'))
#     else:
#         form = LoginUserForm()
#     return render(request, 'users/login.html', {'form': form})

class LoginUser(LoginView):
    # Сам берет данные из БД, сам их проверяет- Django весь берет функционал на себя.
    # Но в формах которые мы делали сами, для добавления статьей,
    # там мы прописывали модель, если форма не связана с ней
    # form_class = AuthenticationForm #стандартный класс формы AuthenticationForm фреймворка Django
    form_class = LoginUserForm #можно свою форму, но надо форму наследовать от AuthenticationForm, а не от forms.Form
    template_name = 'users/login.html'
    extra_context = {'title': "Авторизация"}

    def get_success_url(self):
        return reverse_lazy('home') #Тот же самый эффект можно получить, определив константу в конфигируции LOGIN_REDIRECT_URL = 'home'

# def logout_user(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('users:login'))
# КЛАСС LogoutView мы прописали срауз в URLS



# Для регистрации пользов-я
# def register(request):
#     if request.method == "POST":
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)  # создание объекта без сохранения в БД
#             user.set_password(form.cleaned_data['password']) #ХЕШИРОВАНИЕ ПАРОЛЯ
#             user.save()
#             return render(request, 'users/register_done.html')
#     else:
#         form = RegisterUserForm()
#     return render(request, 'users/register.html', {'form': form})

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')

# Для изменения профиля
class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя"}
    user = model.objects.get(username='Ivan')
    print(user.first_name, user.last_name)

    def get_success_url(self):
        return reverse_lazy('users:profile')

#рофайл будет открываться только для текущего пользователя, либо сделано перенаправление на страницу авторизации для неавторизованных пользователей.
    def get_object(self, queryset=None):


        user = self.request.user
        print(f"User: {user}, First name: {user.first_name}, Last name: {user.last_name}")
        return self.request.user #сохраянет резульат в form в шаблоне можно использовать

#для отображения формы изменения пароля
class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
    extra_context = {'title': "Изменение пароля"}