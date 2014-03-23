#!/usr/bin/python
# -*- coding: utf-8 -*-

#create by Andos he
#h.chujienados@gmail.com

import urllib2
import re
import time
from xmlrpclib import ServerProxy
import threading

class Crawler:

    def __init__(self, begin_url, pageconunt, begincount):
        page = 0
        self.svr=ServerProxy("http://localhost:2310")
        self.url = begin_url
        while page < pageconunt:
            url = begin_url + '/' + str(begincount) + '.html'
            self.run(url)
            begincount += 1
            page += 1

    def run(self, url):
        self.svr.Input(url)
        print url
        try:
            webinfo = urllib2.urlopen(url).read()
            parttern_nextpage=re.compile("<a href='(.*?)'>下一页</a>")
            nextpage=parttern_nextpage.findall(webinfo)
            self.run('http://m.360buy.com'+nextpage[0])
        except:
            return

class Work(threading.Thread):
    def __init__(self, begin_url, pageconunt, begincount):
        self.begin_url = begin_url
        self.pageconunt = pageconunt
        self.begincount = begincount
        threading.Thread.__init__(self)
        
    def run(self):
        crawler = Crawler(self.begin_url, self.pageconunt, self.begincount)
        
if __name__ == '__main__':
    begin_url = 'http://m.360buy.com/comments'
    for i in range(9):
        thread = Work(begin_url, 100000, (i+1)*100000)
        thread.start()
        print "create thread"+str(i)