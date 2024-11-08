menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


class DataMixin:
    title_page = None
    extra_context = {}
    #для extra_context
    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu

# для get_context_data
    def get_mixin_context(self, context, **kwargs):
        print(kwargs)
        context['menu'] = menu
        context['cat_selected'] = None
        #объединяеям два словаря
        context.update(kwargs)
        return context
