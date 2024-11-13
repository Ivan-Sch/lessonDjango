menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]


class DataMixin:
    paginate_by = 3 # пагинация для страниц со статьями
    title_page = None
    cat_selected = None
    extra_context = {}

    #ЕСЛИ extra_context есть там в классе представлени, то он не станвоится пустым,
    # в него просто добавляются, что прописано в __init__


    #для extra_context
    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page
        if self.cat_selected is not None:
            self.extra_context['cat_selected'] = self.cat_selected

        # if 'menu' not in self.extra_context:
        #     self.extra_context['menu'] = menu убрали т.к. прописали шаблонный контесный процессор или simple  тег

# для get_context_data
    def get_mixin_context(self, context, **kwargs):
        print(kwargs)
        # #ПО УМОЛЧАНИЮ
        # context['menu'] = menu
        #ПО УМОЛЧАНИЮ
        context['cat_selected'] = None
        print(context)
        #объединяеям два словаря
        context.update(kwargs)
        return context
