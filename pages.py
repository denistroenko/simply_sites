def load_pages(site):
    from os import uname
    from socket import gethostname
    from classes import Content

    layout_full = {'header':True,
                   'footer':True,
                   'main_menu':True,
                   'slider':True,
                   'sidebar_left':True,
                   'sidebar_right':True,
                   'promo':True,
                   'holidays':True,
                  }


############################### PAGES #############################


    site.add_page(name='Главная',
                  url='/',
                  name_in_menu='home',
                  name_in_content='Welcome to home page!',
                  layout=layout_full,
                  content_place='home.html',
                  seo_data={'title':'Главная страница в SEO data',
                            'description': 'Описание стр в SEO data',
                            'keywords': 'ключевые слова в SEO data',
                            'seo_name':'SEO-NAME! Welcome to Home!'},
                  id_menu=1,
                  access_level=3,
                  )

    site.add_page(name='О программе...',
                  url='/about_program',
                  layout={'sidebar_left':True},
                  content_place='home.html',
                  id_menu=1,
                  access_level=3,
                  )

    site.add_page(name='subpage1',
                  url='/sub1',
                  name_in_menu='Имя в меню 1',
                  id_menu=0,
                  content_place='none',
                  content='Содержимое страницы (подстраницы) 1',
                  id_parent_page=site.get_page_id_by_name('О программе...'),
                  )

    site.add_page(name='subpage2',
                  url='/sub2',
                  id_menu=0,
                  name_in_menu='Имя в меню 2',
                  content_place='none',
                  content='Содержимое страницы (подстраницы) 2',
                  id_parent_page=site.get_page_id_by_name('О программе...'),
                  )

    site.add_page(name='subpage3',
                  url='/sub3',
                  id_menu=0,
                  name_in_menu='Имя в меню 3',
                  content_place='none',
                  content='Содержимое страницы (подстраницы) 3',
                  id_parent_page=site.get_page_id_by_name('О программе...'),
                  )

    id_list = site.get_page_childs(site.get_page_id_by_name('О программе...'))
    content = ''
    pages = site.get_pages_list()
    for pg in pages:
        if pg.get_id() in id_list:
            content += '<a href="' + pg.get_url() + '">' +\
                    pg.get_name_in_menu() + '</a><br>'
    site.add_page(name='subpages',
                  url='/subs',
                  id_menu=1,
                  content=content,
                  )

    info = '{}<br>{}'.format(uname(), gethostname())
    site.add_page(name='SYSInfo',
                  url='/sysinfo',
                  content_place='none',
                  content=info,
                  id_menu=1,
                  layout={'sidebar_left':False,
                         }
                  )
