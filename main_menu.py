def load_pages(menu, site):
    # Наполнить меню ссылками на существующие страницы, если в атрибутах этих
    # страниц указано, что они должны быть в главном меню
    pages = site.get_pages_list()
    menu_id = menu.get_id()
    for page in pages:
        if page.get_id_menu() == menu_id:
            menu.add(page.get_url(),
                    page.get_name_in_menu(),
                    )
            print(page.get_name_in_menu())

def load_system_pages(menu: object):
    # Добавить ссылки на внешние источники
    menu.add('http://yandex.ru', 'YANDEX')

    # Добавить ссылки на спец.страницы
    menu.add('/_seo_test', 'SEO test')
