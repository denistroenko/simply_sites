def load_menu(menu, site, page):
    childs_id = site.get_page_childs_by_id(page.get_id())
    for id in childs_id:
        pg = site.get_page_by_id(id)
        url = pg.get_url()
        name_in_menu = pg.get_name_in_menu()
        menu.add(link=url, caption=name_in_menu)
