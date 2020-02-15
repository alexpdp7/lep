from html import parser
import urllib


def get_front_page_articles():
    return _parse(_get_html())


def _get_html():
    return urllib.request.urlopen("https://elpais.com").read().decode('utf-8')


def _parse(content):
    parser = _HTMLParser()
    listener = _ArticleListener()
    parser.set_listener(lambda url, text: listener.listen(url, text))
    parser.feed(content)
    return listener.articles


class _ArticleListener:
    def __init__(self):
        self._articles = dict()

    def listen(self, url, text):
        texts = self._articles.get(url, [])
        texts.append(text)
        self._articles[url] = texts

    @property
    def articles(self):
        return [Article(url, texts) for url, texts in self._articles.items()]


class _HTMLParser(parser.HTMLParser):
    def set_listener(self, listener):
        self.listener = listener

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = dict(attrs)['href']
            if href.count('/') == 6 and 'redirector' not in href and href[0] == '/':
                self.current_article = href
            

    def handle_endtag(self, tag):
        self.current_article = None

    def handle_data(self, data):
        if hasattr(self, "current_article") and self.current_article:
            self.listener(self.current_article, data)


class Article:
    def __init__(self, url, texts):
        self.url = url
        self.text = " ".join(texts)
        _, section1, _, _, _, section2, _ = url.split("/")
        self.section = f"{section1} - {section2}"

    def __repr__(self):
        return repr(self.__dict__)
