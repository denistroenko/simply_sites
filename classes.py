class Site:
    def __init__(self):
        self.__pages = []  # List of the Page objects
        self.__id_counter = 0

    def add_page(self,
                 name: str,
                 url: str,
                 name_in_menu: str='',
                 name_in_content: str='',
                 layout: dict={},            # see set_layout for args dict
                 content_place: str='none',  # none/file_name.html
                 content='',
                 seo_data: dict={},          # see set_seo for args dict
                 access_level: int=3,
                 id_parent_page: int=0,      # id of parent page. 0 - root
                 id_menu=0,                  # page in menu (id). 0 - no menu
                 ):

        self.__id_counter += 1
        page = Page(id=self.__id_counter,
                    name=name,
                    url=url,
                    name_in_menu=name_in_menu,
                    name_in_content=name_in_content,
                    layout=layout,
                    content_place=content_place,
                    content=content,
                    seo_data=seo_data,
                    access_level=access_level,
                    id_menu=id_menu,
                    )
        self.__pages.append(page)

        if id_parent_page != 0:
            for pg in self.__pages:
                if pg.get_id() == id_parent_page:
                    pg.add_child_page_id(self.__id_counter)

    def get_page(self, url, menu: object):  # Generate HTML

        for page in self.__pages:
            if page.get_url() == url:
                return page.get_page(menu)
        return 'error 404!'

    def get_pages_list(self) -> list:  # return list of objects
        return self.__pages

    def get_page_childs(self, id):
        for pg in self.__pages:
            if pg.get_id() == id:
                return pg.get_child_id()
        return ['---']

    def get_page_id_by_name(self, name):
        for pg in self.__pages:
            if pg.get_name() == name:
                return pg.get_id()
        return -1  # -1 if NO page found


class Page:
    def __init__(self,
                 id: int,
                 name: str,
                 url: str,
                 name_in_menu: str='',
                 name_in_content: str='',
                 layout: dict={},            # see set_layout for args dict
                 content_place: str='none',  # none/file_name.html
                 content='',
                 seo_data: dict={},          # see set_seo for args dict
                 access_level: int=3,        # 0-admin,1-user,2-any user,3-any
                 id_menu=1,                  # page in menu (id). 0 - no menu
                 ):
        from flask import render_template

        self.__id = id
        self.__child_pages_id = []
        self.__name = name

        self.__name_in_menu = name               # Page name in menu
        if name_in_menu != '':
            self.__name_in_menu = name_in_menu

        self.__name_in_content = name           # Page name in content
        if name_in_content != '':
            self.__name_in_content = name_in_content


        # устанавливаем seo- свойства, если они переданы в словаре
        # Или умолчания
        if 'seo_name' in seo_data:
            self.__name_in_content = seo_data['seo_name']  # Page name changed
                                                           # by seo_data

        self.__title = name
        if 'title' in seo_data:
            if seo_data['title'] != '':
                self.__title = seo_data['title']
        self.__description = ''
        if 'description' in seo_data:
            self.__description = seo_data['description']
        self.__keywords= ''
        if 'keywords' in seo_data:
            self.__keywords = seo_data['keywords']


        self.__url = url
        self.__content_place = content_place

        self.__content = content

        self.__id_menu = id_menu
        self.__access_level = access_level

        self.set_layout(layout)

        # Templates
        self.__template_main = 'page.html'
        self.__template_header = 'header.html'
        self.__template_footer = 'footer.html'
        self.__template_main_menu = 'main_menu.html'
        self.__template_slider = 'slider.html'
        self.__template_sidebar_left = 'sidebar_left.html'
        self.__template_sidebar_right = 'sidebar_right.html'
        self.__template_promo = 'promo.html'
        self.__template_holidays = 'holidays.html'

        # Static
        self.__css = 'css/main.css'
        self.__css_system = 'css/system.css'
        self.__js = 'js/main.js'
        self.__js_system = 'js/system.js'

    def set_layout(self, layout: dict):
        ''' please dict:
            {'name':True/False}
            names:
            header
            footer
            main_menu
            sidebar_left
            sidebar_right
            promo
            holidays
        '''
        self.__show_header = True
        if 'header' in layout:
            self.__show_header = layout['header']

        self.__show_footer = True
        if 'footer' in layout:
            self.__show_footer = layout['footer']

        self.__show_main_menu = True
        if 'main_menu' in layout:
            self.__show_main_menu = layout['main_menu']

        self.__show_slider = False
        if 'slider' in layout:
            self.__show_slider = layout['slider']

        self.__show_sidebar_left = True
        if 'sidebar_left' in layout:
            self.__show_sidebar_left = layout['sidebar_left']

        self.__show_sidebar_right = False
        if 'sidebar_right' in layout:
            self.__show_sidebar_right = layout['sidebar_right']

        self.__show_promo = False
        if 'promo' in layout:
            self.__show_promo = layout['promo']

        self.__show_holidays = False
        if 'holidays' in layout:
            self.__show_holidays = layout['holidays']

    def add_child_page_id(self, id: int):
        self.__child_pages_id.append(id)

    def get_page(self, menu: object):
        from flask import render_template, url_for
        from main import file_to_content
        import baseapplib
        from datetime import datetime

        # В зависимости от типа контента (указано в свойстве), считать файл и
        # преобразовать его в контент с помощью глобальной функции, либо ничего
        # не делать вовсе
        if self.__content_place != 'none':
            file_name = self.__content_place
            content = Content(
                name=self.__name_in_content,
                content=file_to_content(url_for(
                        'static',
                        filename='html/{}'.format(file_name)))
                )
            self.__content = content.get_content()
        # else:
            # content = Content(
                    # name=self.__name,
                    # content=self.__content,
                    # ).get_content()
            # self.__content = content

        header = ''
        if self.__show_header:
            header = render_template(self.__template_header)

        footer = ''
        if self.__show_footer:
            copyright_year = datetime.now().year
            footer = render_template(self.__template_footer,
                                     copyright_year=copyright_year)
        main_menu = ''
        if self.__show_main_menu:
            main_menu = render_template(self.__template_main_menu,
                                        main_menu=menu.get_menu_list())
        slider = ''
        if self.__show_slider:
            slider = render_template(self.__template_slider)

        sidebar_left = ''
        if self.__show_sidebar_left:
            sidebar_left = render_template(self.__template_sidebar_left)

        sidebar_right = ''
        if self.__show_sidebar_right:
            sidebar_right = render_template(self.__template_sidebar_right)

        promo = ''
        if self.__show_promo:
            promo = render_template(self.__template_promo)

        holidays = ''
        if self.__show_holidays:
            holidays = render_template(self.__template_holidays)

        return render_template(
                self.__template_main,
                content=self.__content,
                title=self.__title,
                description=self.__description,
                keywords=self.__keywords,
                header=header,
                footer=footer,
                main_menu=main_menu,
                slider=slider,
                sidebar_left=sidebar_left,
                sidebar_right=sidebar_right,
                promo=promo,
                holidays=holidays,
                css=self.__css,
                css_system = self.__css_system,
                js=self.__js,
                js_system=self.__js_system,
                )

    def get_id(self):
        return self.__id

    def get_child_id(self):
        return self.__child_pages_id

    def get_id_menu(self):
        return self.__id_menu

    def get_url(self):
        return self.__url

    def get_name(self):
        return self.__name

    def get_name_in_menu(self):
        return self.__name_in_menu

    def get_name_in_content(self):
        return self.__name_in_content


class Content:
    def __init__(self,
                 name: str,
                 content: str,
                 ):

        self.__name = name
        self.__content = content
        self.__template = 'content.html'

    def get_content(self):
        from flask import render_template
        return render_template(
                self.__template,
                name=self.__name,
                content=self.__content,
                )


class Menu:
    def __init__(self, name, id):
        self.__menu = []
        self.__name = name
        self.__id = id

    def add(self, link, caption):
        self.__menu.append({'link':link, 'caption':caption})

    def get_id(self):
        return self.__id

    def get_menu_list(self):
        return self.__menu

