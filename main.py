import urllib2
from bs4 import BeautifulSoup
from datetime import date

proxy_handler = urllib2.ProxyHandler({})
opener = urllib2.build_opener(proxy_handler)
menu_url = 'http://newsradio.cri.cn/other/2014/jmd14.html'
page = opener.open(menu_url).read()
soup = BeautifulSoup(page)

index = 2
tr_tags = soup.findAll('tr', {'class': 'a03'})
result = []
prefix = 1
for tr_tag in tr_tags:
    a = tr_tag.findAll('td')[index].a
    href = a['href']
    title = str(prefix) + a.text
    result.append({'href': href, 'title': title})




