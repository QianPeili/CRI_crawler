import urllib2
import re
import getopt
import sys
import os
from datetime import date, timedelta
from bs4 import BeautifulSoup
from urlparse import urljoin
from multiprocessing.dummy import Pool


yesterday = date.today() - timedelta(days=1)
date_str = yesterday.strftime('%Y-%m-%d')
directory = 'd:\\cri\\%s\\' % date_str

try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['help', 'date=', 'output='])
    for opt in opts:
        if 'date' in opt[0]:
            date_str = opt[1]
        elif 'output' in opt[0]:
            directory = opt[1] + date_str + '\\'
except getopt.GetoptError:
    pass


class Crawler(object):

    def __init__(day, directory):
        super(Crawler, self).__init__()
        os.system('mkdir %s' % directory)

    def get_opener():
        pass

os.system('mkdir %s' % directory)
proxy_handler = urllib2.ProxyHandler({})
opener = urllib2.build_opener(proxy_handler)
menu_url = 'http://newsradio.cri.cn/other/2014/jmd14.html'
page = opener.open(menu_url).read()
soup = BeautifulSoup(page)

index = 2
tr_tags = soup.findAll('tr', {'class': 'a03'})
p = re.compile(r'(http:.*%s.*mp3)' % date_str)

def find_mp3_uri(l):
    for e in l:
        m = p.search(e['href'])
        if m:
            record_href = m.groups()[0]
            return record_href
    else:
        return None

def save_data_in_mp3(uri, title):
    file_path = os.path.join(directory, '%s.mp3' % title)
    f = open(file_path, 'wb')
    d = opener.open(uri)
    f.write(d.read())
    f.close()

def download_mp3(tr_tag):
    a_tag = tr_tag.findAll('td')[index].a
    href = urljoin(menu_url, a_tag['href'])
    sub_soup = BeautifulSoup(opener.open(href).read())
    a_list = sub_soup.findAll('a')
    title = '%s' % a_tag.text

    mp3_uri = find_mp3_uri(a_list)
    if mp3_uri:
        save_data_in_mp3(mp3_uri, title)


