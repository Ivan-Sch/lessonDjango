from django.contrib.auth.views import LogoutView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy
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


    # Для формы ввода E-mail для восставнавления пароля
    path('password-reset/',
         PasswordResetView.as_view(
             template_name="users/password_reset_form.html",
             email_template_name="users/password_reset_email.html",
             success_url=reverse_lazy("users:password_reset_done")
         ),
         name='password_reset'),



    # Опевещение, что инструкции сброшены на E-mail
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
         name='password_reset_done'),
    #Для формы создания нового пароля, после того как юзер перешел по ссылке, ктр была на его Эл.Почте
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name="users/password_reset_confirm.html",
             success_url=reverse_lazy("users:password_reset_complete")
         ),
         name='password_reset_confirm'),


    #Опевещние, что успешно изменили пароль
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
         name='password_reset_complete'),

]