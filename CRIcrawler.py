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
root_dir = 'c:/cri/'
pattern = re.compile('(http.*mp3)')

try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['help', 'date=', 'output='])
    for opt in opts:
        if 'date' in opt[0]:
            date_str = opt[1]
        elif 'output' in opt[0]:
            root_dir = opt[1]
except getopt.GetoptError:
    exit(0)


directory = os.path.join(root_dir, date_str+'/')
# mkdir if directoty not exists
if os.path.exists(directory) is not True:
    os.mkdir(directory)


class Crawler(object):

    def __init__(self):
        super(Crawler, self).__init__()
        self.opener = self.get_opener()
        self.pattern = re.compile(r'(http:.*%s.*mp3)' % date_str)
        self.index = 1

    def get_opener(self):
        proxy_handler = urllib2.ProxyHandler({})
        opener = urllib2.build_opener(proxy_handler)
        return opener

    def start(self):
        page = self.opener.open(menu_url).read()
        soup = BeautifulSoup(page, 'html.parser')
        self.soup = soup
        div_tag = soup.find('div', {'class': 'box3'})
        a_tags = div_tag.findAll('a')
        hrefs = map(lambda x: urljoin(menu_url, x['href']), a_tags)

        pool = Pool(8)
        pool.map(self.download_mp3, hrefs)
        pool.close()

    def download_mp3(self, href):
        # some url are invalid
        try:
            sub_soup = BeautifulSoup(self.opener.open(href).read(), 'html.parser')
        except IOError:
            print href + ' not found'
            return
        a_tag = sub_soup.find('div', {'class': 'rg'}).a
        source_uri = pattern.search(a_tag['href']).groups()[0]
        tmp_uri = urljoin(menu_url, source_uri)
        mp3_uri = re.sub('\d{4}-\d{2}-\d{2}', date_str, tmp_uri)
        title = re.sub('\d{4}-\d{2}-\d{2}', date_str, a_tag.text)
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
        try:
            d = self.opener.open(uri).read()
        except IOError:
            print uri + ' not exist.'
            return
        file_path = os.path.join(directory, '%s.mp3' % title)
        f = open(file_path, 'wb')
        f.write(d)
        f.close()
        print uri + ' download successfully.'

def main():
    print 'Download start...'
    crawler = Crawler()
    crawler.start()
    print 'Quest done!'

if __name__ == '__main__':
    main()