# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import os

extractpicre = re.compile(r'(?<=<photo-url max-width="1280">).+?(?=</photo-url>)',flags=re.S)   #search for url of maxium size of a picture, which starts with '<photo-url max-width="1280">' and ends with '</photo-url>'
inputfile = open('blogname.txt','r')    #input file for reading blog names (subdomains). one per line

proxy = {'http':'http://127.0.0.1:8087'} #proxy setting for some reason

# invalid character when used in the filename
invalidchars = ['?','\\','/',':','*','<','>','|','\"']


def process_str(oristr):
    '''
    Clear invalid character in the string
    '''
    for invalidchar in invalidchars:
        oristr = oristr.replace(invalidchar, '_')
    return oristr

def downloadPicture(links, dirname):
    duplicateNum = 0
    choice = 'X'
    for link in links:
        surfix = link[-15:]
        imgname = dirname + '/' + process_str(surfix)
        print imgname
        if os.path.exists(imgname):
            print '[+] There is a image which has the same name with a previous one.'
            print '[+] Its name ', imgname
            if choice != 'Y' and choice != 'y' and choice != 'N' and choice != 'n':
                choice = raw_input('[+] Press {Y} to ignore the images, {N} to download them with different names\n')

            if choice == 'Y' or choice == 'y':
                continue
            elif choice == 'N' or choice == 'n':
                filename, expandname = os.path.splitext(imgname)
                imgname = filename+str(duplicateNum)+expandname
                duplicateNum += 1
            else:
                print '[+] Default: ignore it!'
        try:
            imgreq = urllib2.urlopen(link, timeout = 20)
            img = imgreq.read()
        except Exception, e:
            print e
        else:
            with open(imgname, 'wb') as writter:
                writter.write(img)
        print '[+] The link [%s] is done!' %link
    print '[+] Done!'



if __name__== '__main__':
    maxPicEachBlog = 200
    for blogname in inputfile:
        blogname = blogname.strip('\n')
        links = []
        baseurl = 'http://'+blogname.strip()+'.tumblr.com/api/read?type=photo&num=50&start='    #url to start with
        start = 0
        while True:
            url = baseurl + str(start)  #url to fetch
            print '[+]', url   #show fetching info
            pagecontent = urllib.urlopen(url,proxies = proxy).read()    #fetched content
            links = extractpicre.findall(pagecontent)    #find all picture urls fit the regex
            nPic = len(links)
            print '[+] Total number of pictures %d' % nPic
            if(nPic < 50):
                break;
            else:
                start += 50
            if start > 60:     # there are maybe many pictures! 
                break
        if not os.path.exists(blogname):
            os.mkdir(blogname)
            print '[+] Create directory ', blogname
        downloadPicture(links, blogname)
