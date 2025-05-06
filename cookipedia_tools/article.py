from jinja2 import Environment, FileSystemLoader
import os
import requests
from bs4 import BeautifulSoup
from shirotsubaki.element import Element as Elm
from datetime import datetime


def get_title_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.title.string if soup.title else ''
        else:
            print(f'Error: {response.status_code}')
            return ''
    except Exception as e:
        print(f'Error: {str(e)}')
        return ''


def create_reference(url, today):
    print(url)
    datestr = today.strftime('%Y年%m月%d日')
    title = get_title_from_url(url)
    elm_a = Elm('a')
    elm_a.set_attr('class', 'asis')
    elm_a.set_attr('href', url)
    elm_li = Elm('li')
    if title != '':
        elm_li.append(title + '.')
    elm_li.append(elm_a)
    elm_li.append(f' ({datestr}参照).')
    return elm_li


def create_refereces(urls):
    elm_h2 = Elm('h2', '参考文献')
    today = datetime.today()
    elm_ol = Elm('ol')
    elm_ol.set_attr('class', 'ref')
    for url in urls:
        elm_ol.append(create_reference(url, today))
    return str(elm_h2) + '\n' + str(elm_ol)


class Article:
    def __init__(self, article_dir, func_open=None):
        self.env = Environment(loader=FileSystemLoader(article_dir))
        self.template = self.env.get_template('article_template.html')
        self.article_dir = article_dir
        self.func_open = func_open
    def create(self, filebody, title, references, description, long_title=False):
        out_file = os.path.join(self.article_dir, f'{filebody}.html')
        if os.path.isfile(out_file):
            print(f'Already exists: {out_file}')
            return
        data = {
            'long_title': ('long-title' if long_title else ''),
            'title': title,
            'description': description,
            'references': ('' if len(references) == 0 else create_refereces(references)),
        }
        with open(out_file, mode='w', encoding='utf8', newline='\n') as ofile:
            ofile.write(self.template.render(data))
        if self.func_open is not None:
            self.func_open(out_file)
