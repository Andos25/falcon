#!/usr/bin/env python
#coding=utf8

'''''Author: Zheng Yi 
    Email: zhengyi.bupt@qq.com'''  
      
import re  
import json  
      
      
def sServerData(serverData):  
        "Search the server time & nonce from server data"  
          
        p = re.compile('\((.*)\)')  
        jsonData = p.search(serverData).group(1)  
        data = json.loads(jsonData)  
        serverTime = str(data['servertime'])  
        nonce = data['nonce']  
        print "Server time is:", serverTime  
        print "Nonce is:", nonce  
        return serverTime, nonce  
      
      
def sRedirectData(text):  
        p = re.compile('location\.replace\(\'(.*?)\'\)')  
        loginUrl = p.search(text).group(1)  
        return loginUrl  
      
      
def sUrl(htmlData):  
        iMainBegin = htmlData.find('<div class="feed_lists" node-type="feed_list">')  
        iMainEnd = htmlData.find('<div node-type="lazyload" class="W_loading">')  
        mainData = htmlData[iMainBegin:iMainEnd]  
        p = re.compile('href=\"(\/[a-zA-Z0-9\/\%]*?)\"')  
        #p = re.compile('href=\"(http:\/\/weibo.com\/[a-zA-Z]*?)\"')  
        semiUrlList = p.findall(mainData)  
        urlList = []  
        for url in semiUrlList:  
            urlList.append('http://weibo.com' + url)  
        return urlList  
