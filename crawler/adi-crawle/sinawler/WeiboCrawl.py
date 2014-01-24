#!/usr/bin/env python
#coding=utf8


'''''Author: Zheng Yi 
    Email: zhengyi.bupt@qq.com'''  
      
      
import urllib2 
import urllib 
import httplib
import cookielib  
import threading  
import os  
import WeiboEncode  
import WeiboSearch  
import TextAnalyze  
      
      
pagesContent = []           #html content of downloaded pages  
textContent = []            #main text content of downloaded pages  
triedUrl = []               #all tried urls, including failed and success  
toTryUrl = []               #urls to be try  
failedUrl = []              #urls that fails to download  

client_id = '1000570550' # app key
app_scret = 'aff4f0ce3b15153bb755042dccb3a922' # app secret
redirect_uri = 'http://www.data-god.com'
username = "h.chujieandos@gmail.com"
passwd = "antonidas25"
      
      
class WeiboLogin:            
    def __init__(self,uname,upasswd):
            client_id = '1000570550' # app key
            app_scret = 'aff4f0ce3b15153bb755042dccb3a922' # app secret
            redirect_uri = 'http://www.data-god.com'
            username = uname
            passwd = upasswd
    def Login(self, username, passwd):
            client_id = '1000570550'
            redirect_uri = 'http://www.data-god.com'
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
                return False
            print'Login sucess!'
            return True
                
               
    def GetServerTime(self):  
            "Get server time and nonce, which are used to encode the password"  
              
            print "Getting server time and nonce..."  
            serverData = urllib2.urlopen(self.serverUrl).read()  
            print serverData  
      
            try:  
                    serverTime, nonce = WeiboSearch.sServerData(serverData)  
                    return serverTime, nonce  
            except:  
                    print 'Get server time & nonce error!'  
                    return None  
      
      
    def EnableCookie(self, enableProxy):  
            "Enable cookie & proxy (if needed)."  
              
            cookiejar = cookielib.LWPCookieJar()  
            cookie_support = urllib2.HTTPCookieProcessor(cookiejar)  
      
            if enableProxy:  
                proxy_support = urllib2.ProxyHandler({'http':'http://xxxxx.pac'})  
                opener = urllib2.build_opener(proxy_support, cookie_support, urllib2.HTTPHandler)  
                print "Proxy enabled"  
            else:  
                opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
      
            urllib2.install_opener(opener)  
      
      
class WebCrawl:    
    def __init__(self, beginUrl, maxThreadNum = 10, maxDepth = 2, thLifetime = 10, saveDir = "." +os.sep + "CrawledPages"):  
            "Initialize the class WebCrawl"  
              
            toTryUrl.append(beginUrl)  
            self.maxThreadNum = maxThreadNum  
            self.saveDir = saveDir  
            self.maxDepth = maxDepth  
            self.thLifetime = thLifetime  
      
            self.triedPagesNum = 0  
            self.threadPool = []  
      
            if not os.path.exists(self.saveDir):  
                os.mkdir(self.saveDir)  
      
            self.logFile = open(self.saveDir + os.sep + 'log.txt','w')  
      
      
    def Crawl(self):  
            "Run this function to start the crawl process"  
              
            global toTryUrl  
      
            for depth in range(self.maxDepth):  
                print 'Searching depth ', depth, '...'  
                self.DownloadAll()  
                self.UpdateToTry()  
      
      
    def DownloadAll(self):  
            "Download all urls in current depth"  
              
            global toTryUrl  
            iDownloaded = 0  
              
            while iDownloaded < len(toTryUrl):  
                iThread = 0  
                while iThread < self.maxThreadNum and iDownloaded + iThread < len(toTryUrl):  
                    iCurrentUrl = iDownloaded + iThread  
                    pageNum = str(self.triedPagesNum)  
                    self.DownloadUrl(toTryUrl[iCurrentUrl], pageNum)  
      
                    self.triedPagesNum += 1  
                    iThread += 1  
                      
                iDownloaded += iThread  
                  
                for th in self.threadPool:  
                    th.join(self.thLifetime)  
                      
                self.threadPool = []  
                  
            toTryUrl = []  
      
          
    def DownloadUrl(self, url, pageNum):  
            "Download a single url and save"  
              
            cTh = CrawlThread(url, self.saveDir, pageNum, self.logFile)  
            self.threadPool.append(cTh)  
            cTh.start()  
      
      
    def UpdateToTry(self):  
            "Update toTryUrl based on textContent"  
              
            global toTryUrl  
            global triedUrl  
            global textContent  
              
            newUrlList = []  
      
            for textData in textContent:  
                newUrlList += WeiboSearch.sUrl(textData)  
              
            toTryUrl = list(set(newUrlList) - set(triedUrl))  
            pagesContent = []  
            textContent = []  
      
      
class CrawlThread(threading.Thread):  
      
    thLock = threading.Lock()  
      
    def __init__(self, url, saveDir, pageNum, logFile):    
            threading.Thread.__init__(self)  
            self.url = url  
            self.pageNum = pageNum  
            self.fileName = saveDir + os.sep + pageNum + '.htm'  
            self.textName = saveDir + os.sep + pageNum + '.txt'  
            self.logFile = logFile  
            self.logLine = 'File: ' + pageNum + '  Url: '+ url    
      
      
    def run(self):  
            "rewrite the run() function"  
              
            global failedUrl  
            global triedUrl  
            global pagesContent  
            global textContent  
      
            try:  
                htmlContent = urllib2.urlopen(self.url).read()              
                transText = TextAnalyze.textTransfer(htmlContent)  
                  
                fOut = open(self.fileName, 'w')  
                fOut.write(htmlContent)  
                fOut.close()  
                tOut = open(self.textName, 'w')  
                tOut.write(transText)  
                tOut.close()  
      
            except:  
                self.thLock.acquire()  
                triedUrl.append(self.url)  
                failedUrl.append(self.url)  
                sFailed = 'Failed!   ' + self.logLine  
                print sFailed  
                self.logFile.write(sFailed + '\n')  
                self.thLock.release()  
                return None  
              
            self.thLock.acquire()  
            pagesContent.append(htmlContent)  
            textContent.append(transText)  
            triedUrl.append(self.url)  
            sSuccess = 'Success!  ' + self.logLine  
            print sSuccess  
            self.logFile.write(sSuccess + '\n')  
            self.thLock.release()  
