#!/usr/bin/env python
#coding=utf8

import urllib2

def getfanslist(uid, page):
    url = "http://weibo.com/p/"+str(uid)+"/follow?relate=fans&page="+str(page)
    html = urllib2.urlopen(url).read()
    print html

if __name__ == "__main__":
    getfanslist(1005051266321801, 1)
