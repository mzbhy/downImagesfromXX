# -*- coding:utf-8 -*-
'''
爬取某1024社区达盖尔旗帜的图片
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

## 代理服务器设置
proxies = {
        'http': 'http://127.0.0.1:8087',
        'https': 'http://127.0.0.1:8087',
}

proxy_handler = urllib2.ProxyHandler(proxies)
null_proxy_handler = urllib2.ProxyHandler({})

opener = urllib2.build_opener(proxy_handler)
urllib2.install_opener(opener)

def gethtml(url):
    req = urllib2.Request(url, headers = headers)
    try:
        response = urllib2.urlopen(url,timeout = 20)
       # html = response.read().decode('gb2312','ignore')
       # return html
    except urllib2.URLError, e:
        print e.reason
        return ""
    else:
        try:
            html = response.read().decode('gb2312','ignore')
        except urllib2.URLError, e:
            print e.reason
            return ""
        else:
            return html

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
        title = h.get_text().replace('?', u'？')

        if os.path.exists(title):   # 当前已经有了这个帖子了
            print u'%s 已经下载过了，此次跳过' % (title)
            continue

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
    if titles == []:
        return
    idx = 0

    count = 0;
    for link in links:
        title = titles[idx]
        idx = idx + 1

        print u'开始第 %d 个帖子' % (idx)
        print u'帖子的题目是 %s' % title

        if count >= 2:
            break
        count = count + 1
        imglinks = []
        jumpurl = prefix + link

        html = gethtml(jumpurl)
        soup = BeautifulSoup(html)

        inputs = soup.find('body').find('div', class_ = "tpc_content").find_all('input',recursive=True)
        for inp in inputs:
            imglink = inp.get('src')
            print imglink
            imglinks.append(imglink)

        mkdirname = title.replace('?', u'？')

        if os.path.exists(mkdirname):    # 以前处理过了
            continue

        os.mkdir(mkdirname)

        print u'开始下载图片，帖子题目是 %s' %mkdirname
        for imglink in imglinks:
            try:
                img = urllib2.urlopen(imglink).read()
            except urllib2.URLError, e:
                print e.reason
            else:
                print u'图片 %s 处理完了' %imglink
                with open(mkdirname+'/'+ imglink[-20:],'wb') as code:
                    code.write(img)
        print u'第 %d 个帖子下载完了' % (idx)


start = 1
end = 2

for page in range(start, end + 1):
    print u'开始第 %d 页' % (page)

    html = getpage(page)

    if html:
        titles, links = findtiezi_link(getpage(page))
        getimgs(titles, links)
    print u'第 %d 页下载完了' % (page)

print 'Done'

