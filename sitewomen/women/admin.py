from django.contrib import admin, messages
from .models import Women, Category


# admin.site.register(Women) #регистрация таблицы (модели)


# можно создать свой собсвенный фильтр, со своей собтсвенной логикой
class MarriedFilter(admin.SimpleListFilter):
    title = 'Статус женщин'
    parameter_name = 'status' #создается для написания ссылки в поискивке /?'status'='married'

    def lookups(self, request, model_admin): #создается для написания ссылки в поискивке /?'status'='married'
        return [
            ('married', 'Замужем'), #( Названия параметров, Названия пунктов в фильтре)
            ('single', 'Не замужем'),
        ]

    def queryset(self, request, queryset): #создается для свеого отбора
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)

@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_create', 'is_published', 'cat', 'brief_info')
    list_display_links = ('title',)
    list_editable = ('is_published',)
    ordering = ['-time_create', 'title']
    list_per_page = 5
    actions = ['set_published', "set_draft"] # прописывается для пользовталеского действия
    search_fields = ['title__startswith', 'cat__name'] # создается поиск по полю т.е. будет писатьсься фраза, часть слова, и будет находится в столбацах указанных
    list_filter = [MarriedFilter, 'cat__name', 'is_published'] #создается фильтр таблицы справа от таблицы, по каким-то параметрам, которыйе указаны
    # также тут указана ссылка на класс MarriedFilter- свой собвсвтенный фильтр, со своей логикой работы


   #создается пользовтаельское поле (стобец) в админ панели, которого нет в БД
    @admin.display(description="Краткое описание", ordering='content' ) #для названия стобца. Если бы его не было, то было бы название метода brief_info. Ordering, чтобы у поля была сортировка
    def brief_info(self, women: Women):
        return f"Описание {len(women.content)} символов."


    #Создание пользовательских действий/ На самом верху списка расположен в админ панели
    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей).") #для создания уведомления сверху о действие

    # Создание пользовательских действий для снятия с УВНЕДОМЛЕНИЕМ о снятии self.message_user (messages.WARNING)
    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей) сняты с публикации!", messages.WARNING) #для создания уведомления сверху о действие



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
