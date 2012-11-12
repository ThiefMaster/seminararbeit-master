# vim: fileencoding=utf8
import re
import urllib
from bs4 import BeautifulSoup
from datetime import datetime
from flask import Flask, render_template, request
from flask.ext.cache import Cache
from werkzeug.contrib.atom import AtomFeed
from werkzeug.routing import BaseConverter

# Initialize application
app = Flask(__name__)
app.config.from_pyfile('hskatom.cfg')
cache = Cache(app)

# Config vars
NEWS_URLS = app.config.setdefault('NEWS_URLS', {})
FEED_TITLE = app.config.setdefault('FEED_TITLE', 'Hochschule Karlsruhe - News')
NEWS_CACHE_DURATION = app.config.setdefault('NEWS_CACHE_DURATION', 3600)

# Url argument converter
class NewsKeyConverter(BaseConverter):
    """Matches a news key"""
    def __init__(self, map):
        BaseConverter.__init__(self, map)
        self.regex = '(?:%s)' % '|'.join([re.escape(x) for x in NEWS_URLS])
app.url_map.converters['newskey'] = NewsKeyConverter

# Utility functions
@cache.memoize(NEWS_CACHE_DURATION)
def retrieve_news(key):
    url = NEWS_URLS[key]
    app.logger.debug('Loading news from %s' % url)
    try:
        conn = urllib.urlopen(url)
    except IOError:
        return None
    bs = BeautifulSoup(conn.read(), 'lxml')
    conn.close()
    content = bs.find('div', id='content')
    if not content:
        return None
    blocks = content.find_all('div', 'csc-default')
    items = []
    for block in blocks:
        item = {}
        item['id'] = block['id']
        item['title'] = block.find('h4').text
        tmp = block.find('div', 'last')
        if not tmp:
            continue
        tmp = tmp.find('div', 'content')
        if not tmp:
            continue
        item['content'] = ''.join(map(unicode, tmp.contents))
        items.append(item)
    return items, datetime.utcnow()

# View functions
@app.route('/')
def index():
    return render_template('index.html', newskeys=NEWS_URLS.keys())

@app.route('/<newskey:key>.atom')
def atom(key):
    items, last_update = retrieve_news(key)
    url = NEWS_URLS[key]
    feed = AtomFeed(FEED_TITLE, feed_url=request.url, url=url,
        subtitle=key, updated=last_update)
    ts = datetime(1970, 1, 1)
    for item in items:
        item_url = '%s#%s' % (url, item['id'])
        feed.add(item['title'], item['content'], content_type='html', id=item_url,
            updated=ts, url=item_url)
    return feed.get_response()
