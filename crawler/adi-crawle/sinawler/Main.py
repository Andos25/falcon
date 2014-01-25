#!/usr/bin/env python
#coding=utf8
    
import WeiboCrawl  
   
if __name__ == '__main__':  
	beginUrl = 'http://weibo.com/yaochen'
	weiboLogin = WeiboCrawl.WeiboLogin('h.chujieandos@gmail.com','antonidas25')  
	if weiboLogin.Login('h.chujieandos@gmail.com','antonidas25') == True:  
		print "The WeiboLogin module works well!"  
      
	#start with my blog :)  
	webCrawl = WeiboCrawl.WebCrawl(beginUrl)  
	webCrawl.Crawl()  
	del webCrawl  
