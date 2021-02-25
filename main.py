import os
import socket
from flask import Flask, url_for
import baseapplib
from classes import Site, Page, Content, Menu
from pages import load_pages
from main_menu import load_menu


__version__ = '0.0.1'
SITE_NAME = 'Symply Site'

app = Flask(__name__)
site = Site()
menu = Menu('Main menu', 0)


def main():
    load_pages(site)
    load_menu(menu=menu, site=site)


def file_to_content(file_path):
    curent_path = baseapplib.get_script_dir()
    with open('{}{}'.format(curent_path, file_path,)) as file:
        content = file.read()
    return content


main()


@app.route('/')
def index():
    global site
    global menu
    return site.get_page(url='/', menu=menu)


@app.route('/<page_name>')
def page_name(page_name):
    global site
    global menu
    page_name = '/' + page_name
    return site.get_page(url=page_name, menu=menu)


if __name__ == '__main__':
    app.run(
        debug=True,
        host='192.168.88.1',
        port=80,
    )
