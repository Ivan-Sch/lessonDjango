from django import template
from django.db.models import Count

import women.views as views
from women.models import Category, TagPost

register = template.Library()


# @register.simple_tag(name='getcats')
# def get_categories():
#     return views.cats_db


@register.inclusion_tag('women/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.annotate(total=Count("posts")).filter(total__gt=0)
    return {'cats': cats, 'cat_selected': cat_selected}   #связано это с index.html то что туда подается, то и БУДЕТ здесь передаваться--- cat_selected берется как раз из переданного в index.html---- потом все это (шаблонный тег show_categories)  мы запишем в base.html
# идет синхранизация со всеми шаблонами - потому что они связаны. index связан с base.html следоавтельно мы можем там прописать вот этот НОЫЙ тег show_categories, в который переданы данные через index т.е.
# index -> base -> list_categories.html (все они хранят данные поданные в index)


@register.inclusion_tag('women/list_tags.html')
def show_all_tags():
    return {"tags": TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)}