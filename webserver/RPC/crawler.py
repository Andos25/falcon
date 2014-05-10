#!/usr/bin/env python
#coding=utf-8

import urllib2
import urllib
import re
from xmlrpclib import ServerProxy
import threading
import httplib
import login
import string  

pattern = re.compile('<a.*?\s+usercard=\\\\"id=(\d+)\\\\".*?W_f14 S_func1.*?>(.*?)<\\\/a>',re.S)

def get_homepage(username):
    pattern = re.compile(r'href=\\"(http:\\/\\/weibo.com\\/.*?)" title=')
    content = urllib2.urlopen("http://s.weibo.com/user/"+username+"&Refer=index").read()
    info = pattern.findall(content)[0]
    url = info.replace('\\', '');
    print url
    return url

def get_ids(url):
    uidpattern=re.compile("CONFIG\['oid'\]='(\d+)'",re.S)
    domainpattern=re.compile("CONFIG\['domain'\]='(\d+)'",re.S)
    content = urllib2.urlopen(url).read()
    uid =  uidpattern.findall(content)[0]
    domain = domainpattern.findall(content)[0]
    return uid,domain
def create_url(uid,domain):
    fans_page = "http://weibo.com/"+str(uid)+"/myfans?from=page_"+str(domain)+"&wvr=5.1&mod=headfans"
    follow_page = "http://weibo.com/"+str(uid)+"/myfollow?from=page_"+str(domain)+"&wvr=5.1&mod=headfollow"
    return fans_page,follow_page

def  get_info(url,n):
    info_list = list()
    name_list = list()
    content = urllib2.urlopen(url).read()
    info =  pattern.findall(content)
    n = n if(len(info)>n) else len(info)
    for i in range(0,n):
        tmp = {"id":list(info[i])[0],"name":list(info[i])[1]}
        name_list.append(list(info[i])[1])
        info_list.append(tmp)
    return info_list,name_list

def fans_crawler(username,n):
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>fans_crawler"
    fans_info_list = list()
    fans_name_list = list()
    FANS = list()
    url = get_homepage(username)
    uid,domain = get_ids(url)
    login.weiboLogin()                                    # login module must set here
    fans_page,follow_page = create_url(uid,domain)
    fans_info_list,fans_name_list = get_info(fans_page,n)
    # print fans_info_list
    # print fans_id_list
    for item in fans_info_list:
        tmp = {"name":item["name"]}
        new_fans_info = list()
        new_fans_name = list()
        new_follows_info = list()
        new_follows_name = list()
        uid_page = "http://weibo.com/u/"+str(item["id"])
        # print uid_page
        new_uid,new_domain = get_ids(uid_page)
        new_fans_page,new_follows_page = create_url(new_uid,new_domain)
        new_fans_info,new_fans_name = get_info(new_fans_page,n)
        new_follows_info,new_follows_name= get_info(new_follows_page,n)
        tmp["fans"] = new_fans_name
        tmp["follows"] = new_follows_name
        FANS.append(tmp)
    display(FANS)

def follows_crawler(username,n):
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>follows_crawler"
    follow_info_list = list()
    follow_name_list = list()
    FOLLOWES = list()
    url = get_homepage(username)
    uid,domain = get_ids(url)
    login.weiboLogin()                                    # login module must set here
    fans_page,follow_page = create_url(uid,domain)
    follow_info_list,follow_name_list = get_info(follow_page,n)
    for item in follow_info_list:
        tmp = {"name":item["name"]}
        new_fans_info = list()
        new_fans_name = list()
        new_follows_info = list()
        new_follows_name = list()

        uid_page = "http://weibo.com/u/"+str(item["id"])
        new_uid,new_domain = get_ids(uid_page)
        new_fans_page,new_follows_page = create_url(new_uid,new_domain)
        new_fans_info,new_fans_name = get_info(new_fans_page,n)
        new_follows_info,new_follows_name = get_info(new_follows_page,n)
        tmp["fans"] = new_fans_name
        tmp["follows"] = new_follows_name
        FOLLOWES.append(tmp)
    display(FOLLOWES)

def  display(object):
    for i in object:
        print i

class staff (threading.Thread):
    def __init__(self, threadID, username, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.username = username
        self.counter = counter

    def run(self):
        print "Starting " + self.name
        if self.threadID%2==1:
            fans_crawler(self.username,self.counter)
        else:
            follows_crawler(self.username,self.counter)
        print "Exiting " + self.name

if __name__ == '__main__':
    #the number 9 is the number of threads,can change it
    for i in range(1,3):
        thread = staff(i,"姚晨",4)
        thread.start()