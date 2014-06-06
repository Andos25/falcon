#!/usr/bin/env python
#coding=utf8
      
import re  
import json
import logging 
import urllib2
import urllib 
from bs4 import BeautifulSoup

logger = logging.getLogger('bloglog')    
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
      
      
def sUrl(websize):  
        # iMainBegin = htmlData.find('<div class="WB_global_nav">')  
        # print iMainBegin
        # iMainEnd = htmlData.find('</div>')  
        # print iMainEnd
        # mainData = htmlData[iMainBegin:iMainEnd] 
        savefile = '/home/adiking/sinawler/savefile'

        urlre = re.compile(r'(http://[^/\\]+)', re.I)
        hrefre = re.compile(r'href="(.*?)"', re.I)
        # hrefre = re.compile(r'<a.* href=".*?<\/a>', re.I)
        blogre = re.compile(r'http://weibo.com/[\w]+[/\d]*', re.I)
        filterre = re.compile(r'.htm?|.xml|</p>|http://blog.sina.com.cn/[\w]+/[\w]+/', re.I)
        urlmatch = urlre.match(websize)
        if not urlmatch:
        #print '%s is not a correct url.'%websize
            logger.info('%s is not a correct url.'%websize)
        else:
            try:
                urllist = []
                fd = urllib2.urlopen(websize)
                content =fd.read()
                # print content
                #print '\nConnetion %s success...'%(websize)
                logger.info('Connetion %s success...'%(websize))
                hrefs = hrefre.findall(content)
                print hrefs

                for href in hrefs:
                    splits = href.split(' ')
                    if len(splits) != 1:
                        href = splits[1]
                    #get text of href tag
                    matches = re.match('href="(.*)"', href)
                    if matches is not None:
                        url = matches.group(1)
                        # print url
                        if blogre.match(url) is not None:
                            if filterre.findall(url):
                                pass
                            else:
                                urllist.append(url)
                saveFile(filterDuplicateData(urllist), savefile) 
                return urllist          
            except Exception, error:
                #print error
                    logger.info(error)

    # '''