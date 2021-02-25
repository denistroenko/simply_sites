def load_pages(site):
    from os import uname
    from socket import gethostname
    from classes import Content

    site.add_page(name='Главная',
                  url='/',
                  name_in_menu='home',
                  name_in_content='Welcome to home page!',
                  layout={'sidebar_left':True, 'sidebar_right':True},
                  content_place='home.html',
                  seo_data={'title':'Главная страница в SEO data',
                            'description': 'Описание стр в SEO data',
                            'keywords': 'ключевые слова в SEO data',
                            'seo_name':'SEO-NAME! Welcome to Home!'},
                  in_main_menu=True,
                  access_level=3,
                  )

    site.add_page(name='О программе...',
                  url='/about_program',
                  layout={'sidebar_left':True},
                  content_place='home.html',
                  in_main_menu=True,
                  access_level=3,
                  )

    info = '{}<br>{}'.format(uname(), gethostname())
    site.add_page(name='SYSInfo',
                  url='/sysinfo',
                  content_place='none',
                  content=info,
                  in_main_menu=True,
                  )
