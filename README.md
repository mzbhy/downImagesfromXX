# downImagesfromXX

从某知名1024网站下载图片区图片

思路很简单，解析网页的HTML，找到图片的链接，然后去下载。

对HTML的解析用到了BeautifulSoup包。 

由于你懂的的原因，默认挂了代理。

目前存在的问题是对于部分标记有"先锋团"的帖子，只能下载到狮子Logo，还在解决之中。

Python新手，代码多有不规范之处。欢迎交流，如果您发现了其他 BUG或有相关想法，请和我联系。

## 2015年8月31日 更新
添加了Tumblr的批量下载脚本。在脚本所在文件夹下新建文档input.txt，将要下载的博客名输入，每行一个，
即可下载。

参考了知乎用户@exzhawk 的[博客](http://blog.exz.me/2014/write-a-python-script-to-export-1280-size-picture-urls-of-tumblrs/)
