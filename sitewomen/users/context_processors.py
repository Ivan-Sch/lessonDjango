from women.utils import menu

#Контекстные процессор для отображения меню на всех страницах. Т.е. мы можем спокойно обращаться к mainmenu,
# а следоватлеьгно к menu. ДЛЯ ЭТОГО В натройках конфигурации
# context_processors пропишем настрйоку для распозанования даннйо фун-ии
def get_women_context(request):
    return {'mainmenu': menu}