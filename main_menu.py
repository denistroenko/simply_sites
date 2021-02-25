def load_menu(menu, site):
    # Наполнить меню ссылками на существующие страницы, если в атрибутах этих
    # страниц указано, что они должны быть в главном меню
    pages = site.get_pages_list_as_objects()
    for page in pages:
        if page.in_main_menu():
            menu.add(page.get_url(),
                    page.get_name_in_menu(),
                    )
            print(page.get_name_in_menu())
    # Добавить ссылки на внешние источники
    menu.add('http://yandex.ru', 'YANDEX')
