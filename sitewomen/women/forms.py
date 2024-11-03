from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Husband


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code, params={"value": value})

class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, min_length=5, label="Заголовок", #валидаторы для проверки на браузере
                            widget=forms.TextInput(attrs={'class': 'form-input'}),
                            # validators=[
                            #     RussianValidator(), #т.к. некторых валиадров может не сущесовать, мы можем создавать свой (для многоразовго использования в коде) или
                            #     # если этот валиадор будет использвоаен один раз, то пищшется метод def clean
                            # ],
                            error_messages={#валидаторы для проверки на сервере
                                'min_length': 'Слишком короткий заголовок', #валидаторы для проверки на сервере
                                'required': 'Без заголовка - никак',
                            }) #здесь как раз используется widget тобы создать класс для него и регулировать стили, т.к. в шаблоне у всех классы одинаковые

    slug = forms.SlugField(max_length=255, label="URL", validators=[#валидаторы для проверки на сервере
        MinLengthValidator(5, message="Минимум 5 символов"), #валидаторы для проверки на сервере
        MaxLengthValidator(100, message="Максимум 100 символов"),
    ])

    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label="Контент")
    is_published = forms.BooleanField(required=False, label="Статус", initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категории", empty_label="Категория не выбрана")
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, label="Муж", empty_label="Не замужем")

    #для одногоразовго использования валидатора пищшется данный метод
    def clean_title(self):
        title = self.cleaned_data['title']
        ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError("Должны быть только русские символы, дефис и пробел.")

        return title