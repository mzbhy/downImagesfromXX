# -*- coding:utf-8 -*-
'''
爬取草榴社区达盖尔旗帜的图片
需要 BeautifulSoup 库的支持
需要设置代理
'''
import urllib2
import urllib
from bs4 import BeautifulSoup
import os

addr = 'http://t66y.com/thread0806.php?fid=16&page='
prefix = 'http://t66y.com/'

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0'
          }

##
proxies = {
        'http': 'http://127.0.0.1:8087',
        'https': 'http://127.0.0.1:8087',
}

def gethtml(url):
    req = urllib2.Request(url, headers = headers)
    try:
        response = urllib.urlopen(url, proxies = proxies)
        html = response.read().decode('gb2312','ignore')
        return html
    except urllib2.URLError, e:
        print e.reason
    return ""

def getpage(page):
    # 当前地址页
    url = addr + str(page)
    return gethtml(url)

'''
获取当前页面下所有帖子的标题和链接
'''
def findtiezi_link(html):
    # 获取soup
    soup = BeautifulSoup(html)

    # 分析 HTML 结构
    bigpage = soup.find('body').find('div', style = "margin:3px auto").find('tbody', style = "table-layout:fixed;")

    tmp = bigpage.find_all('tr', class_ = 'tr2')

    mountain = tmp[-1]

    trs = mountain.find_next_siblings('tr',class_ = "tr3 t_one")
    links = []
    titles = []

    for tr in trs:
        td = tr.find('td', style="text-align:left;padding-left:8px")
        h = td.find('h3')
        title = h.get_text()
        a = h.find('a')
        link = a.get('href')

        links.append(link)
        titles.append(title)

        #print >> outfile, "%s %s" %(link.encode('utf-8'), title.encode('utf-8'))
    return titles, links

'''
获取当前link下的图片
'''
def getimgs(titles, links):
    idx = 0

    for link in links:
        print u'开始第 %d 个帖子' % (idx + 1)

        imglinks = []
        jumpurl = prefix + link

        html = gethtml(jumpurl)
        soup = BeautifulSoup(html)
        inputs = soup.find('body').find('div', class_ = "tpc_content").find_all('input')

        for inp in inputs:
            imglink = inp.get('src')
            print imglink
            imglinks.append(imglink)

        title = titles[idx]

        mkdirname = title.replace('?', u'？')

        if os.path.exists(mkdirname) == False:
            os.mkdir(mkdirname)
        idx = idx + 1          # title 加 1

        for imglink in imglinks:
            img = urllib2.urlopen(imglink).read()
            print imglink
            with open(mkdirname+'/'+ imglink[-20:],'wb') as code:
                            code.write(img)
        print u'第 %d 个帖子下载完了' % (idx + 1)

start = 1
end = 5

for page in range(start, end + 1):
    print u'开始第 %d 页' % (page)

    titles, links = findtiezi_link(getpage(page))
    getimgs(titles, links)
    print u'第 %d 页下载完了' % (page)

print 'Done'



