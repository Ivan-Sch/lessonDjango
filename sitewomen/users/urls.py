from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
app_name = "users" #т.к. используется namespace="users"
urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'), #МОЖНО СРАЗУ ПРОПИСАТЬ обравщение к встоенному классу
    # представления- без добавления своего и наследования от LogoutView
    # path('register/', views.register, name='register'),
    path('register/', views.RegisterUser.as_view(), name='register')
]