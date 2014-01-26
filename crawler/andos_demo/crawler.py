#!/usr/bin/env python
#coding=utf-8

import urllib2
import re
import time
from xmlrpclib import ServerProxy
import threading

class Crawler():
    """docstring for crawler"""
    def __init__(self):
        self.svr=ServerProxy("http://localhost:2310")
        self.pattern=re.compile('<a page-limited.*?>(\d+)<\/a>', re.S)
        while(self.getuserurl_db()):
            for i in range(1, self.get_limit_pagecount()):
                self.getfanscontent(i)
            break

    def getuserurl_db(self):
        #select a user's url which haven't be crawled, use a flag to sign a user
        #add code here:

        #Andos-demo: this code is just for demo, when you code your code ,delete this code
        self.url = "http://weibo.com/p/1003061266321801/follow"
        return True
        #if not find user which not crawled, return False
        #if xxxxx:return False

    def get_limit_pagecount(self):
        content = urllib2.urlopen(self.url).read()
        print content
        info = self.pattern.findall(content)[0]
        return int(info)

    def getfanscontent(self, pagecount):
        content = urllib2.urlopen(self.url+"?page="+str(pagecount)+"#place").read()
        self.svr.Input(content)
        
class Work(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        #add login code at here

    def run(self):
        crawler = Crawler()

if __name__ == '__main__':
    #the number 9 is the number of threads, you can change it
    for i in range(9):
        thread = Work()
        thread.start()
        print "create thread"+str(i)