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
    # print url
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

def  get_info(url,username,n):
    info_list = list()
    pair_list = list()
    content = urllib2.urlopen(url).read()
    info =  pattern.findall(content)
    n = n if(len(info)>n) else len(info)
    for i in range(0,n):
        tmp = {"id":list(info[i])[0],"name":list(info[i])[1]}
        pair = username+"->"+list(info[i])[1]
        pair_list.append(pair)
        info_list.append(tmp)
    return info_list,pair_list

def  display(object):
    for i in object:
        print i

def crawler(username,n):
    # print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>fans_crawler"
    result = dir()
    fans_info_list = list()
    fans_pair_list = list()
    new_follows = list()
    follows_info_list = list()
    follow_pair_list = list()
    new_fans = list()
    url = get_homepage(username)
    uid,domain = get_ids(url)
    login.weiboLogin()                                    # login module must set here
    fans_page,follow_page = create_url(uid,domain)
    fans_info_list,fans_pair_list = get_info(fans_page,username,n)
    follows_info_list,follow_pair_list = get_info(follow_page,username,n)
    follow_pair_list.extend(fans_pair_list)
    for item in fans_info_list:
        new_fans_info = list()
        new_fans_pair = list()
        new_follows_info = list()
        new_follows_pair = list()
        uid_page = "http://weibo.com/u/"+str(item["id"])
        new_uid,new_domain = get_ids(uid_page)
        new_fans_page,new_follows_page = create_url(new_uid,new_domain)
        new_fans_info,new_fans_pair = get_info(new_fans_page,str(item["name"]),n)
        new_follows_info,new_follows_pair= get_info(new_follows_page,str(item["name"])  ,n)
        # fans_pair_list.extend(new_fans_pair)
        follow_pair_list.extend(new_fans_pair)
        # new_follows.extend(new_follows_pair)
        follow_pair_list.extend(new_follows_pair)
    for item in follows_info_list:
        new_fans_info = list()
        new_fans_pair = list()
        new_follows_info = list()
        new_follows_pair = list()
        uid_page = "http://weibo.com/u/"+str(item["id"])
        new_uid,new_domain = get_ids(uid_page)
        new_fans_page,new_follows_page = create_url(new_uid,new_domain)
        new_fans_info,new_fans_pair = get_info(new_fans_page,str(item["name"]),n)
        new_follows_info,new_follows_pair= get_info(new_follows_page,str(item["name"])  ,n)
        # follow_pair_list.extend(new_follows_pair)
        # new_fans.extend(new_fans_pair)
        follow_pair_list.extend(new_fans_pair)
        follow_pair_list.extend(new_follows_pair)
    # fans_pair_list.extend(new_fans)
    # follow_pair_list.extend(new_follows)
    # result = {"fans":fans_pair_list,"follows":follow_pair_list}
    result = {"relation":follow_pair_list}
    return result


# def follows_crawler(username,n):
#     # print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>follows_crawler"
#     follows_info_list = list()
#     follow_pair_list = list()
#     new_fans = list()
#     url = get_homepage(username)
#     uid,domain = get_ids(url)
#     login.weiboLogin()                                    # login module must set here
#     fans_page,follow_page = create_url(uid,domain)
#     follows_info_list,follow_pair_list = get_info(follow_page,username,n)
#     for item in follows_info_list:
#         new_fans_info = list()
#         new_fans_pair = list()
#         new_follows_info = list()
#         new_follows_pair = list()
#         uid_page = "http://weibo.com/u/"+str(item["id"])
#         new_uid,new_domain = get_ids(uid_page)
#         new_fans_page,new_follows_page = create_url(new_uid,new_domain)
#         new_fans_info,new_fans_pair = get_info(new_fans_page,str(item["name"]),n)
#         new_follows_info,new_follows_pair= get_info(new_follows_page,str(item["name"])  ,n)
#         follow_pair_list.extend(new_follows_pair)
#         new_fans.extend(new_fans_pair)
#         # display(new_fans)
#     return follow_pair_list,new_fans

# class staff (threading.Thread):
#     def __init__(self, threadID, username, counter):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.username = username
#         self.counter = counter

#     def run(self):
#         fans_pair_list = list()
#         new_follows = list()
#         follow_pair_list = list()
#         new_fans = list()
#         result = dir()
#         # print "Starting " + self.name
#         if self.threadID%2==1:
#             fans_pair_list,new_follows = fans_crawler(self.username,self.counter)
#         else:
#             follow_pair_list,new_fans = follows_crawler(self.username,self.counter)
#         # print "Exiting " + self.name
#         fans_pair_list = fans_pair_list.extend(new_fans)
#         follow_pair_list = follow_pair_list.extend(new_follows)
#         result = {"fans":fans_pair_list,"follows":follow_pair_list}
#         return result

if __name__ == '__main__':
    crawler("姚晨",4)
#     #the number 9 is the number of threads,can change it
#     for i in range(1,3):
#         thread = staff(i,"姚晨",4)
#         thread.start()
