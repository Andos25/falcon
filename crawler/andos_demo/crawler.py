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

id =0
fansdic = None
class Crawler():
    """docstring for crawler"""
    def __init__(self):
        self.saveDir = "." +os.sep + "data"
        pid = '100306'
        pageNum = '1266321801'
        source_url = "http://weibo.com/p/1003061266321801"
        self.fansdic = dict()
        # self.fileName = saveDir + os.sep + pageNum + 'content.htm'  
        # self.uidlist = saveDir + os.sep + pageNum + 'uidlists.txt'
        # self.fanslist = saveDir + os.sep + pageNum + 'fanslists.txt'  
        self.svr=ServerProxy("http://localhost:2310")
        # self.pattern=re.compile(r'<a\s*class=\\"S_func1\\" href=(.*) target=\\"__blank\\">.*?<\/a>', re.S)
        # self.pattern=re.compile("href=\"(.+?)\"",re.S)
        self.pattern=re.compile("<a(.+?)>",re.S)

        # self.hrefpattern=re.compile('href=\\\\"\\\\/p\\\\/(\d+)')
        self.pidpattern=re.compile("CONFIG\['pid'\]='(\d+)'",re.S)
        self.hrefpattern=re.compile('href=.*?(usercard=.+)\\\\\"')
        self.listpattern=re.compile('<a.*?(\w+=\d+).*?>',re.S)
        self.fanspattern=re.compile('uid=\d+',re.S)

        while(source_url):
            self.get_limit_pagecount(source_url,pageNum)
                # self.getfanscontent(i)
            print 'get fans list,waiting...... '
            if self.getfanscontent(source_url,pageNum) is not None:
                print 'make fans list saved!'
            else:
                print 'faild to save the fans list!'

            # break

    def getuserfans_db(self,pagecount,fanslist):
        #select a user's url which haven't be crawled, use a flag to sign a user
        #add code here:
        #Andos-demo: this code is just for demo, when you code your code ,delete this code
        num =0
        for line in open(fanslist):
            matches = re.match('uid:(\d+)', line)
            fansid = matches.group(1)
            # print dict({pagecount:{'no':num,'uid':fansid,'used':0}})
            # self.fansdic = dict({pagecount:{'no':num,'uid':fansid,'used':0}}) #focus dict init style!!
            self.fansdic[num] = dict({'page':pagecount,'uid':fansid,'used':0})
            num = num+1
        return self.fansdic
        #if not find user which not crawled, return False
        #if xxxxx:return False
    def url_make(self):
        # print self.fansdic
        for key in self.fansdic:
            fans = self.fansdic[key]
            if fans['used']==0:
                url = 'http://weibo.com/u/'+str(fans['uid'])
                pageNum = fans['uid']
                print url
                fans['used']=1
                break
        return pageNum

    def get_limit_pagecount(self,url,pageNum):
        fileName = self.saveDir + os.sep + pageNum + 'content.html'
        uidlist = self.saveDir + os.sep + pageNum + 'uidlists.txt' 
        print fileName
        fOut = open(fileName, 'w')
        content = urllib2.urlopen(url).read()
        print content
        fOut.write(content)
        if content is not None:
            print str(url)+'content saved!'
            self.pid = self.pidpattern.findall(content)[0]
            print self.pid
            subinfo = self.pattern.findall(content)
            subinfo = ''.join(subinfo)
            hrefs = self.hrefpattern.findall(subinfo)
            # print hrefs
            print uidlist
            for href in hrefs:
                splits = href.split(' ')
                # print splits
                for split in splits:
                    matches = re.match('usercard=\\\\"(\w+=\d+)\\\\\"', split)
                    if matches is not None:
                        uid = matches.group(1)
                        tmp = re.compile('=')
                        uid = tmp.sub(':', uid)
                        fOut = open(uidlist, 'a')
                        fOut.write(uid+'\n')
                        print uid
            
            print str(url)+'content ids saved!'            
        return self.pid

    def get_fans_list(self,fanstext,pagecount,pageNum):
        # print fanstext
        fanslist = self.saveDir + os.sep + pageNum + 'fanslists.txt'  
        pre_fansid = 0
        fansre = self.listpattern.findall(fanstext)
        # print fanslist
        for fans in fansre:
            fans = fans.split(', ')
            for fan in fans:
                matches = re.match('uid=\d+',fan)
                if matches is not None:
                    fansid = matches.group()
                    tmp = re.compile('=')
                    fansid = tmp.sub(':', fansid)
                    if(fansid!=pre_fansid):
                        print fansid
                        fOut = open(fanslist,'a')
                        fOut.write(fansid+'\n')
                        pre_fansid = fansid

        self.getuserfans_db(pagecount,fanslist)
        return True

    def getfanscontent(self,url,pageNum):
        pagecount = 1
        fanstext = urllib2.urlopen("http://weibo.com/p/"+str(self.pid)+str(pageNum)+"/follow?relate=fans&page="+str(pagecount)+"#place").read()
        aa = "http://weibo.com/p/"+str(self.pid)+str(pageNum)+"/follow?relate=fans&page="+str(pagecount)+"#place"
        print aa
        while (fanstext):
            # print fanstext
            print '>>>>>>>>>>>>>>>>>>>fans on page '+str(pagecount)
            if (self.get_fans_list(fanstext,pagecount,pageNum)):
                pageNum = self.url_make()
                url = 'http://weibo.com/u/'+str(pageNum)
                while url:
                    self.get_limit_pagecount(url,pageNum)
                    pageNum = self.url_make()
                    url = 'http://weibo.com/u/'+str(pageNum)
                pagecount = pagecount+1
                content = urllib2.urlopen(url+"?page="+str(pagecount)+"#place").read()
            else:
                break
        return 1
        # self.svr.Input(content)
        
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