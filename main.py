import urllib2
import re
import getopt
import sys
import os
from datetime import date, timedelta
from bs4 import BeautifulSoup
from urlparse import urljoin
from multiprocessing.dummy import Pool


menu_url = 'http://newsradio.cri.cn/other/2014/jmd14.html'
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

    def __init__(self):
        super(Crawler, self).__init__()
        os.system('mkdir %s' % directory)
        self.opener = self.get_opener()
        self.pattern = re.compile(r'(http:.*%s.*mp3)' % date_str)
        self.index = 1

    def get_opener(self):
        proxy_handler = urllib2.ProxyHandler({})
        opener = urllib2.build_opener(proxy_handler)
        return opener

    def start(self):
        page = self.opener.open(menu_url).read()
        soup = BeautifulSoup(page)
        tr_tags = soup.findAll('tr', {'class': 'a03'})

        pool = Pool()
        try:
            map(self.download_mp3, tr_tags)
        except Exception:
            raise
        pool.close()

    def download_mp3(self, tr_tag):
        a_tag = tr_tag.findAll('td')[self.index].a
        href = urljoin(menu_url, a_tag['href'])
        sub_soup = BeautifulSoup(self.opener.open(href).read())
        a_list = sub_soup.findAll('a')
        title = '%s' % a_tag.text

        mp3_uri = self.find_mp3_uri(a_list)
        if mp3_uri:
            self.save_data_in_mp3(mp3_uri, title)

    def find_mp3_uri(self, l):
        for e in l:
            m = self.pattern.search(e['href'])
            if m:
                record_href = m.groups()[0]
                return record_href
        else:
            return None

    def save_data_in_mp3(self, uri, title):
        file_path = os.path.join(directory, '%s.mp3' % title)
        f = open(file_path, 'wb')
        d = self.opener.open(uri).read()
        f.write(d)
        f.close()    

if __name__ == '__main__':
    crawler = Crawler()
    crawler.start()
