#!/usr/bin/env python
#coding=utf-8

import urllib2
import urllib
import re
import time
from xmlrpclib import ServerProxy
import threading
import httplib
import os

class Crawler():
    """docstring for crawler"""
    def __init__(self):
        saveDir = "." +os.sep + "data"
        self.url = "http://weibo.com/p/1003061266321801"
        self.pageNum = '1003061266321801' 
        self.fileName = saveDir + os.sep + self.pageNum + 'content.htm'  
        self.uidlist = saveDir + os.sep + self.pageNum + 'uidlists.txt'  
        self.svr=ServerProxy("http://localhost:2310")
        # self.pattern=re.compile(r'<a\s*class=\\"S_func1\\" href=(.*) target=\\"__blank\\">.*?<\/a>', re.S)
        # self.pattern=re.compile("href=\"(.+?)\"",re.S)
        self.pattern=re.compile("<a(.+?)>",re.S)
        # self.hrefpattern=re.compile('href=\\\\"\\\\/p\\\\/(\d+)')
        self.hrefpattern=re.compile('href=.*?(usercard=.+)\\\\\"')
        
        while(self.getuserurl_db()):
            for i in range(1, self.get_limit_pagecount()):
                self.getfanscontent(i)
            break

    def getuserurl_db(self):
        #select a user's url which haven't be crawled, use a flag to sign a user
        #add code here:

        #Andos-demo: this code is just for demo, when you code your code ,delete this code
        self.url = "http://weibo.com/yaochen"
        return True
        #if not find user which not crawled, return False
        #if xxxxx:return False

    def get_limit_pagecount(self):
        fOut = open(self.fileName, 'w')
        content = urllib2.urlopen(self.url).read()
        fOut.write(content)
        # print content
        subinfo = self.pattern.findall(content)
        subinfo = ''.join(subinfo)
        hrefs = self.hrefpattern.findall(subinfo)
        for href in hrefs:
            splits = href.split(' ')
            # print splits
            for split in splits:
                matches = re.match('usercard=\\\\\"(\w+=\d+)\\\\\"', split)
                if matches is not None:
                    uid = matches.group(1)
                    fOut = open(self.uidlist, 'a')
                    fOut.write(uid+'\n')
                    print uid

        return 1

    def getfanscontent(self, pagecount):
        content = urllib2.urlopen(self.url+"?page="+str(pagecount)+"#place").read()
        self.svr.Input(content)
        
class Work(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        #add login code at here
        client_id = '1000570550'
        redirect_uri = 'http://www.data-god.com'
        username = 'h.chujieandos@gmail.com'
        passwd = 'antonidas25'
        url = "https://api.weibo.com/oauth2/authorize?client_id="+client_id+"&redirect_uri="+redirect_uri+"&response_type=code"
        conn = httplib.HTTPSConnection("api.weibo.com")
        postdata = urllib.urlencode({'client_id':client_id,'redirect_uri':redirect_uri,'action':'submit','userId':username,'passwd':passwd})
        conn.request('POST','/oauth2/authorize',postdata,{'Referer':url, 'Content-Type': 'application/x-www-form-urlencoded'})
        res = conn.getresponse()
        page = res.read()
        code = res.msg['Location'].split("?")[1][5:]
        try:
            res.getheaders()
        except:
            print 'Login error!'
            # return False
        print'Login sucess!'
        # return True

    def run(self):
        crawler = Crawler()

if __name__ == '__main__':
    #the number 9 is the number of threads, you can change it
    for i in range(1):
        thread = Work()
        thread.start()
        print "create thread"+str(i)