__version__ = '0.0.1'


import os
import socket
from flask import Flask, url_for
import baseapplib
from classes import Site, Page, Content, Menu
import pages
import main_menu
import sub_menu


SITE_NAME = 'Symply Site'

app = Flask(__name__)
site = Site()
menu = Menu('Main menu', 1)


def main():
    pages.load_pages(site=site)
    main_menu.load_pages(menu=menu, site=site)
    main_menu.load_system_pages(menu=menu)


def file_to_content(file_path):
    curent_path = baseapplib.get_script_dir()
    with open('{}{}'.format(curent_path, file_path,)) as file:
        content = file.read()
    return content


main()


@app.route('/')
def index():
    submenu=Menu('Sub Menu', 2)
    return site.get_page(url='/', menu=menu, submenu=submenu)


@app.route('/<page_url>')
def page_name(page_url):
    page_url= '/' + page_url
    page = site.get_page_by_url(page_url)
    submenu = Menu('Sub menu', 2)
    sub_menu.load_menu(menu=submenu, site=site, page=page)
    return site.get_page(url=page_url, menu=menu, submenu=submenu)


@app.route('/_seo_test')
def seo_test():
    content = '<h1> SEO test </h1>'
    for page in site.get_pages_list():
        seo_data = page.get_seo_data()

        title_len = len(seo_data['title'])
        if title_len <= 60:
            len_color = 'green'
        elif title_len <= 70:
            len_color = 'orange'
        else:
            len_color= 'red'

        title_len_analyze = f'<span style="color: {len_color};">'
        title_len_analyze += str(title_len)
        title_len_analyze += '</span>'

        content += '<h3><a href="{}">{}</a> (len: {})</h2> '.format(
                page.get_url(),
                seo_data['title'],
                title_len_analyze,
                )

        content += '<span style="color: gray;">[id:{}]</span> {}'.format(
                page.get_id(), page.get_url())

        content += '<h3>{}</h3>'.format(seo_data['seo_name'])

        if seo_data['description']:
            content += '<i>{}</i><br>'.format(seo_data['description'])
        else:
            content += '<span style="color: orange;"<i>Нет description</i>'
            content += '</span><br>'

        if seo_data['keywords']:
            content += '{}<br>'.format(seo_data['keywords'])
        else:
            content += '<span style="color: gray;"<i>Нет keywords</i>'
            content += '</span><br>'

        content += '<br>'
    page_seo_test = Page('-1',
                         'SEO test',
                         '/_seo_test',
                         content=content,
                         content_place='none',
                         )
    submenu=Menu('Sub menu', 2)
    return page_seo_test.get_page(menu=menu, submenu=submenu)


if __name__ == '__main__':
    app.run(
        debug=True,
        host='192.168.88.1',
        port=80,
    )
