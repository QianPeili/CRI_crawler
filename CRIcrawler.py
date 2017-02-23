import re
import getopt
import sys
import os

from datetime import date, timedelta
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool
from urllib.request import ProxyHandler, build_opener, urljoin


def get_opt_value():
    """
    get opt value
    :return:
    """

    date_str = root_dir = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], '', ['help', 'date=', 'output='])
        for opt in opts:
            if 'date' in opt[0]:
                date_str = opt[1]
            elif 'output' in opt[0]:
                root_dir = opt[1]
    except getopt.GetoptError:
        exit(0)
    else:
        return date_str, root_dir


class Crawler(object):

    menu_url = 'http://newsradio.cri.cn/other/2014/jmd14.html'
    default_dir = "./"

    def __init__(self, date_str, root_dir):
        super(Crawler, self).__init__()
        if not date_str:
            date_str = self.default_date_str
        if not root_dir:
            root_dir = self.default_dir

        self.date_str = date_str
        self.directory = self.get_output_dir(root_dir)

        self.opener = self.get_opener()
        self.pattern = re.compile(r'(http:.*%s.*mp3)' % date)
        self.index = 1

        page = self.opener.open(self.menu_url).read()
        soup = BeautifulSoup(page, 'html.parser')
        self.soup = soup

    @property
    def default_date_str(self):
        yesterday = date.today() - timedelta(days=1)
        result = yesterday.strftime('%Y-%m-%d')
        return result

    def get_output_dir(self, root_dir):
        directory = os.path.join(root_dir, self.date_str + '/')

        # create new directory if directory not exists
        if os.path.exists(directory) is not True:
            os.mkdir(directory)
        return directory

    @staticmethod
    def get_opener():
        proxy_handler = ProxyHandler({})
        opener = build_opener(proxy_handler)
        return opener

    def start(self):
        div_tag = self.soup.find('div', {'class': 'box3'})
        a_tags = div_tag.findAll('a')
        href_list = map(lambda x: urljoin(self.menu_url, x['href']), a_tags)

        pool = Pool(8)
        pool.map(self.download_mp3, href_list)
        pool.close()

    def download_mp3(self, href):
        # some url are invalid
        try:
            sub_soup = BeautifulSoup(self.opener.open(href).read(), 'html.parser')
        except IOError:
            print(href + ' not found')
            return
        a_tag = sub_soup.find('div', {'class': 'rg'}).a
        pattern = re.compile('(http.*mp3)')
        source_uri = pattern.search(a_tag['href']).groups()[0]
        tmp_uri = urljoin(self.menu_url, source_uri)
        mp3_uri = re.sub('\d{4}-\d{2}-\d{2}', self.date_str, tmp_uri)
        title = re.sub('\d{4}-\d{2}-\d{2}', self.date_str, a_tag.text)
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
            print(uri + ' not exist.')
            return
        file_path = os.path.join(self.directory, '%s.mp3' % title)
        f = open(file_path, 'wb')
        f.write(d)
        f.close()
        print(uri + ' download successfully.')


def main():
    print('Download start...')
    date_str, output = get_opt_value()
    crawler = Crawler(date_str, output)
    crawler.start()
    print('Quest done!')

if __name__ == '__main__':
    main()
