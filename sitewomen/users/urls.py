from django.contrib.auth.views import LogoutView, PasswordChangeDoneView
from django.urls import path
from . import views
app_name = "users" #т.к. используется namespace="users"
urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'), #МОЖНО СРАЗУ ПРОПИСАТЬ обравщение к встоенному классу
    # представления- без добавления своего и наследования от LogoutView
    # path('register/', views.register, name='register'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    # Для изменения пароля
    path('password-change/', views.UserPasswordChange.as_view(), name='password_change'),
    # Для перенавпрления после успешного изменения
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"), name="password_change_done"),
    # Для password_change_done мы не создаем форму(не нужна) и не пишем класс предстлавения, т.к. сразу к нему обращаемся,
    # а чтобы указать свой шаблон, мы пишем в ф-ии as_view
]