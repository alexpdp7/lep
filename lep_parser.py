import urllib

import pyquery
from importlib.resources import path


def get_front_page_articles():
    return _articles(_load_front_page())


def _load_front_page():
    return pyquery.PyQuery('https://elpais.com')


class Link:
    def __init__(self, py_query):
        self.py_query = py_query

    @property
    def is_article(self):
        return self.py_query.attr.href.count('/') == 8

    @property
    def path(self):
        return urllib.parse.urlparse(self.py_query.attr.href).path


class Article:
    def __init__(self, path, page_py_query):
        self.path = path
        self.page_py_query = page_py_query

    @property
    def _links(self):
        return [pyquery.PyQuery(link) for link in self.page_py_query('a[href*="{0}"]'.format(self.path))]

    @property
    def text(self):
        return ' '.join([link.text() for link in self._links]).strip() or '???'

    @property
    def section(self):
        parts = self.path.split('/')
        return '{0} - {1}'.format(parts[1], parts[5])

    @property
    def href(self):
        return 'https://elpais.com{0}'.format(self.path)


def _all_links(page):
    return [Link(pyquery.PyQuery(link)) for link in page('a[href^="https://elpais.com/"]')]

def _article_links(page):
    return [link for link in _all_links(page) if link.is_article]

def _deduped_paths(page):
    return list(set([link.path for link in _article_links(page)]))

def _articles(page):
    return [Article(path, page) for path in _deduped_paths(page)]
