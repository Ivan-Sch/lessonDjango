"""
URL configuration for sitewomen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from women import views
from women.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('women.urls')),   # include('users.urls'), говорит Django, что нужно импортировать маршруты
    # (URL-паттерны) из файла urls.py, который находится в приложении users.

    path('users/', include('users.urls', namespace="users")), #namespace нужен чтобы без конфликтов обращаться,
    # Таким образом, мы дополнительно изолируем приложение users от возможных конфликтов в именах маршрутов других приложений,
    # для этого в urls приложения пишут app_name = "users".

    path("__debug__/", include("debug_toolbar.urls")),
]

#чтобы в режиме теста отображлись изображения
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found

admin.site.site_header = "Панель администрирования" #для первоо заголовка название
admin.site.index_title = "Известные женщины мира" #для 2 заголовка
