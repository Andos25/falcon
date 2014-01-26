#!/usr/bin/python
# -*- coding: utf-8 -*-

#create by Andos he
#h.chujienados@gmail.com

from xmlrpclib import ServerProxy
import time
import urllib2
import re
import threading

class Analysis:
    def __init__(self):
        self.svr = ServerProxy("http://localhost:2310")
        self.lock = threading.Lock()

    def get_content(self):
        while True:
            try:
                content = self.svr.Output()
                self.content_analy(content)
            except:
                time.sleep(2)

    def content_analy(self, content):
        #use "re" to get useful content

    def saveinfo(self):
        #add save info code
        #save info to database

class Work(threading.Thread):

    def run(self):
        analysis = Analysis()
        analysis.get_content()

if __name__ == '__main__':
    for i in range(10):
        thread = Work()
        thread.start()
