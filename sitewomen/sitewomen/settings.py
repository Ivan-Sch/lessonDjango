"""
Django settings for sitewomen project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ywt^i-jce1cq%5q4s^p0130-h9x9vdmvmge-vf8g+htkga+=71'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']
INTERNAL_IPS = ['127.0.0.1'] #для оптимизации используют dj debug-tooolbar
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions', #для Установка улучшенной пакета django-extensions
    'women.apps.WomenConfig',
    "users.apps.UsersConfig", #для приложения авторизации
    'debug_toolbar', #для оптимизации используют dj debug-tooolbar
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',#для приложения авторизации уже было
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',#для приложения авторизации уже было
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware', #для оптимизации используют dj debug-tooolbar
]

ROOT_URLCONF = 'sitewomen.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'users.context_processors.get_women_context', #для шаблонного контекстного процессора
                # ,context_processors.py -  get_women_context фу-я
            ],
        },
    },
]

WSGI_APPLICATION = 'sitewomen.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
#нестандартный путь
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

#URL-маршрут к изображению будет иметь этот префикс media
MEDIA_URL = '/media/'
#общий путь сохранения файлов
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#задает URL-адрес, на который следует перенаправлять пользователя после успешной авторизации;
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'users:login'
# LOGIN_URL – определяет URL-адрес, на который следует перенаправить
# неавторизованного пользователя при попытке посетить закрытую страницу сайта;
# LOGOUT_REDIRECT_URL – задает URL-адрес, на который перенаправляется пользователь после выхода.

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', #стандартная проверка по username and password
    'users.authentication.EmailAuthBackend', #ссылка на бэкенд аунтификацию (своя логика проверки по E-mail)

]
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"# вместо инструкций для восставноления пароля будет приходить в консоль
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"  #почтовый SMTP-бэкенд. Можно убрать параметр EMAIL_BACKEND, или прописать его со значением:


EMAIL_HOST = "smtp.yandex.ru" #Это адрес SMTP-сервера, предоставляемого Яндексом. Он используется для отправки электронной почты с помощью SMTP-протокола.
EMAIL_PORT = 465 #Это порт, который используется для подключения к SMTP-серверу. Порт 465 часто используется для защищенных соединений с использованием SSL.
EMAIL_HOST_USER = "serbakovv79@yandex.ru" #Это адрес электронной почты, который будет использоваться как имя пользователя при аутентификации на SMTP-сервере.
# В данном случае это ваш адрес Яндекс.
EMAIL_HOST_PASSWORD =  "" #Это пароль для учетной записи электронной почты Яндекс, который будет использоваться для аутентификации при отправке электронных писем.
EMAIL_USE_SSL = True #Это параметр, указывающий, что в соединении с SMTP-сервером следует использовать SSL (Secure Sockets Layer) для шифрования данных.
# Это повышает безопасность при передаче данных.


DEFAULT_FROM_EMAIL = EMAIL_HOST_USER #  - Значение по умолчанию для отправителя электронных писем. Здесь оно устанавливается равным EMAIL_HOST_USER,
# так что все письма будут выглядеть так, как будто они отправлены с этого адреса.

SERVER_EMAIL = EMAIL_HOST_USER #Это адрес электронной почты, который будет использоваться для сообщений об ошибках, отправляемых с вашего приложения.
# Обычно это адрес, с которого отправляются уведомления о проблемах, связанных с работой приложения.

EMAIL_ADMIN = EMAIL_HOST_USER  #Этот параметр, как правило, указывает адрес электронной почты администратора, который будет получать уведомления об ошибках,
#если они возникают в приложении.

AUTH_USER_MODEL = 'users.User' #при замене существующей модели User на свою собственную, нам в файле settings.py необходимо еще переопределить параметр AUTH_USER_MODEL,
#который по умолчанию принимает значение 'auth.User'.

DEFAULT_USER_IMAGE = MEDIA_URL + 'users/default.png'