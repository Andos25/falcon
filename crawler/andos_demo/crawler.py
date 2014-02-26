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
import login
import ast
import getWeiboPage
import Analysis
import string

id =0
pagecount = 1
fansdic = None
class Crawler():
    """docstring for crawler"""
    def __init__(self):
        self.saveDir = "." +os.sep + "data"
        uname = 'Kafka桑'
        pid = '100505'
        uid = '1766325471'
        source_url = "http://weibo.com/p/1003061266321801/weibo?is_search=0&visible=0&is_tag=0&profile_ftype=1&page=1#feedtop"
        self.fansdic = dict()
        # self.fileName = saveDir + os.sep + uid + 'content.htm'  
        # self.uidlist = saveDir + os.sep + uid + 'uidlists.txt'
        # self.fanslist = saveDir + os.sep + uid + 'fanslists.txt'  
        self.svr=ServerProxy("http://localhost:2310")
        self.pattern=re.compile("<a(.+?)>",re.S)

        # self.hrefpattern=re.compile('href=\\\\"\\\\/p\\\\/(\d+)')
        self.pidpattern=re.compile("CONFIG\['pid'\]='(\d+)'",re.S)
        self.stimepattern=re.compile("CONFIG\['servertime'\]='(\d+)'",re.S)
        self.hrefpattern=re.compile('href=.*?(usercard=.+)\\\\\"')
        self.listpattern=re.compile('(<li class=\\\\"clearfix S_line1\\\\".*?>)',re.S)
        self.fansid_pattern=re.compile('<li.*?uid=(\d+).*?>',re.S)
        self.fansname_pattern=re.compile('<li.*?\d+&fnick=(.*?)&.*?>',re.S)
        self.weiboc_pattern = re.compile('<strong.*?weibo.*?(\d+)<\\\/strong>',re.S)
        self.fansc_pattern = re.compile('<strong.*?fans.*?(\d+)<\\\/strong>',re.S)
       
        self.crawler(uname,uid)
        self.craw_fans(uname,pid,uid)

            # break

    def get_uncrawed_fans(self):    #cong db qu fans zhuanhuan cheng dic
        #select a user's url which haven't be crawled, use a flag to sign a user
        #add code here:
        #Andos-demo: this code is just for demo, when you code your code ,delete this code
        store = Analysis.Store()
        fans = store.get_uncrawed_fans()
        return fans


    def url_make(self):      #qu fans id
        # print self.fansdic
        for key in self.fansdic:
            fans = self.fansdic[key]
            if fans['used']==0:
                url = 'http://weibo.com/u/'+str(fans['uid'])
                uid = fans['uid']
                print url
                fans['used']=1
                break
        return uid
        # http://weibo.com/p/1003061266321801/weibo?from=page_100306&wvr=5&mod=headweibo

    def crawler(self,uname,uid):
        page_num = self.get_page_count(uid)
        # print page_num
        fileName = self.saveDir + os.sep + uid + 'content.html'
        uidlist = self.saveDir + os.sep + uid + 'uidlists.txt' 
        url = "http://weibo.com/u/"+str(uid)+"?source=webim"
        req = urllib2.Request(url)
        text = urllib2.urlopen(req).read()
        pid = self.pidpattern.findall(text)[0]
        print pid
        WBpage = getWeiboPage.getWeiboPage()
        content = WBpage.get_msg(uname,uid,pid,page_num)      
        return 1

    def get_page_count(self,uid):  
        url = "http://weibo.com/u/"+str(uid)+"?source=webim"
        print url
        req = urllib2.Request(url)
        result = urllib2.urlopen(req)
        content = result.read()
        content = content.encode("utf-8")
        count = self.weiboc_pattern.findall(content)
        for c in count:
            weibo_num = string.atoi(c)
            page_num = weibo_num/45+1
            print page_num
        return page_num

    def get_fans_store(self,uname,pid,uid):
        store = Analysis.Store()
        url = url = "http://weibo.com/u/"+str(uid)+"?source=webim"
        req = urllib2.Request(url)
        result = urllib2.urlopen(req).read()
        count = self.fansc_pattern.findall(result)
        for c in count:
            fans_num = string.atoi(c)
            page_num = fans_num/20+1
            print page_num
        for num in range(1,page_num):
            fans_url = "http://weibo.com/p/"+str(pid)+str(uid)+"/follow?relate=fans&page="+str(num)+"#place" 
            req = urllib2.Request(fans_url)
            content = urllib2.urlopen(req).read().encode("utf-8")
            fanslists = self.listpattern.findall(content)
            for li in fanslists:
                print li
                fansname = self.fansname_pattern.findall(li)[0]
                fansid = self.fansid_pattern.findall(li)[0]
                print fansname.encode("utf-8")
                print fansid
                store.fans_store(uname,uid,fansid,fansname)

        return True

    def craw_fans(self,uname,pid,uid):
        store = Analysis.Store()
        self.get_fans_store(uname,pid,uid)
        fans_info = store.get_uncrawed_fans()
        while (fans_info):
            uid = fans_info['fans']['fansid']
            print uid
            uname = fans_info['fans']['fansname']
            print uname
            ob_id = fans_info['_id']
            if(self.crawler(uname,uid)):
                store.fans_mark(ob_id)
            self.get_fans_store(uname,pid,uid)
            fans_info = self.get_uncrawed_fans()

        
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
            # content = urllib2.urlopen('http://weibo.com/p/1003061266321801/follow?relate=fans&page=1#place').read()
        except:
            print 'authorize error!'
            # return False
        print'authorize sucess!'
        # return True
        login.weiboLogin()

    def run(self):
        crawler = Crawler()



if __name__ == '__main__':
    #the number 9 is the number of threads, you can change it
    for i in range(1):
        thread = Work()
        thread.start()
        print "create thread"+str(i)