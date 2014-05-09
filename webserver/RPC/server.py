#!/usr/bin/env python
#coding=utf-8

import zerorpc
import re
import urllib2
import crawler

class CrawlerRPC(object):
    def __init__(self):
        self.pattern = re.compile(r"<br title='(.*?)'>");

    def checkschedule(self):
        content = urllib2.urlopen("http://127.0.0.1:8088").read();
        info = self.pattern.findall(content);
        for i in info:
            if i != "100.0":
                return i
        return "-1"
    def weibocrawler(self,username,n):
        for i in range(1,3):
            thread = crawler.staff(i,username,n)
            thread.start()

if __name__ == '__main__':
    s = zerorpc.Server(CrawlerRPC())
    s.bind("tcp://0.0.0.0:4242")
    s.run()
    # a = CrawlerRPC()
    # a.weibocrawler('姚晨',4)

