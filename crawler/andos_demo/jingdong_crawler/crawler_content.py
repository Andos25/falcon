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
                url = self.svr.Output()
                print url
                webinfo = urllib2.urlopen(url).read()
                pattern = re.compile('<div class="eval">(.*?</div>.*?总结.*?</div>)',re.S)
                content = pattern.findall(webinfo)
                self.content_analy(content)
            except:
                time.sleep(2)

    def content_analy(self, content):
        for line in content:
            parttern = re.compile('<div class="u-score">评分：<span>(\d)分</span></div>')
            score = (parttern.findall(line))[0]
            if score == '4' or score == '5':  
                parttern1 = re.compile('(?<=<div class="u-merit"><strong>优点：</strong>).*(?=</div>)')
                merit = (parttern1.findall(line))[0]
                self.lock.acquire()
                self.saveinfo(merit, 'good')
                self.lock.release()
            
                parttern2 = re.compile('(?<=<div class="u-insi"><strong>不足：</strong>).*(?=</div>)')
                insipient = (parttern2.findall(line))[0]
                if insipient != '暂时还没发现缺点哦！' and insipient != '暂时还没有发现缺点哦！':
                    self.lock.acquire()
                    self.saveinfo(insipient, 'bad')
                    self.lock.release()

            if score =='1' or score =='0':  
                parttern3 = re.compile('(?<=<div class="u-summ"><strong>总结：</strong>).*(?=</div>)')
                summary = (parttern3.findall(line))[0]
                self.lock.acquire()
                self.saveinfo(summary, 'bad')
                self.lock.release()
                
                parttern4 = re.compile('(?<=<div class="u-insi"><strong>不足：</strong>).*(?=</div>)')
                insipient = (parttern4.findall(line))[0]
                insipient = insipient.encode('utf-8')
                if insipient != '暂时还没发现缺点哦！' and insipient != '暂时还没有发现缺点哦！':
                    self.lock.acquire()
                    self.saveinfo(insipient, 'bad')
                    self.lock.release()

    def saveinfo(self, info, info_type):
        try:
            if info_type == 'good':
                f = open('data/good.txt','a')
            elif info_type == 'bad':
                f = open('data/bad.txt','a')
            try:
                f.write('%s\n'%(info))
            except:
                trackback.print_exc()
            finally:
                f.close()                
            
        except IOException:
            print "Open File Failed!"

class Work(threading.Thread):

    def run(self):
        analysis = Analysis()
        analysis.get_content()

if __name__ == '__main__':
    for i in range(10):
        thread = Work()
        thread.start()
