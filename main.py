import urllib2
import re
from datetime import date, timedelta
from bs4 import BeautifulSoup
from urlparse import urljoin


proxy_handler = urllib2.ProxyHandler({})
opener = urllib2.build_opener(proxy_handler)
menu_url = 'http://newsradio.cri.cn/other/2014/jmd14.html'
page = opener.open(menu_url).read()
soup = BeautifulSoup(page)

yesterday = date.today() - timedelta(days=1)
date_str = yesterday.strftime(u'%Y-%m-%d')
directory = 'd:/cri/%s/' % date_str

index = 2
tr_tags = soup.findAll('tr', {'class': 'a03'})
p = re.compile(r'(http:.*%s.mp3)' % date_str)

for tr_tag in tr_tags:
    a_tag = tr_tag.findAll('td')[index].a
    href = urljoin(menu_url, a_tag['href'])
    sub_soup = BeautifulSoup(opener.open(href).read())
    a_list = sub_soup.findAll('a')

    
    for e in a_list:
        m = p.search(e['href'])
        if m:
            record_href = m.groups()[0]
            data = opener.open(record_href)
            break
    title = a_tag.text

broadcast_records = []


def download_mp3(tr_tag, pattern):
    a_tag = tr_tag.findAll('td')[index].a
    href = urljoin(menu_url, a_tag['href'])
    sub_soup = BeautifulSoup(opener.open(href).read())
    a_list = sub_soup.findAll('a')
    title = a_tag.text

    records_uris = find_mp3_uri(a_list)

