#!/usr/bin/env python
#coding=utf-8

import zerorpc
import re
import urllib2
import crawler
import json
import pymongo

class CrawlerRPC(object):
    def __init__(self):
        self.pattern = re.compile(r"<br title='(.*?)'>");
        self.conn = pymongo.Connection("localhost",27017)
        self.db = self.conn.falcon

    def checkschedule(self):
        content = urllib2.urlopen("http://127.0.0.1:8088").read();
        info = self.pattern.findall(content);
        for i in info:
            if i != "100.0":
                return i
        return "-1"

    def weibocrawler(self,username,n=4):
        graphinfo = dict()
        format_str = ""
        result = crawler.crawler(username,n)
        for i in result["fans"]:
            format_str +=  i+"{ weight:1,name :""} \n"
            format_str += i.split('->')[0]+"{color:#ff0000}\n"+i.split('->')[1]+"{color:#00ffff}\n"
        for j in result["follows"]:
            format_str += "{ weight:1,name :""} \n"
            format_str += i.split('->')[0]+"{color:#ff0000}\n"+i.split('->')[1]+"{color:#00ffff}\n"
        format_str +="\n; endings\n"
        graphinfo['src'] = format_str
        data = {"graphinfo": graphinfo, "img_url": ""}    
        data = json.dumps(data)
        self.db.craw.insert({"name":username,"content":data})
        print "finished!"
        return data


if __name__ == '__main__':
    s = zerorpc.Server(CrawlerRPC())
    s.bind("tcp://0.0.0.0:4242")
    s.run()
    # a = CrawlerRPC()
    # a.weibocrawler('周迅')

