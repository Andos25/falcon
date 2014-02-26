#!/usr/bin/env python 
#coding=utf-8

import urllib
import urllib2
import sys
import time
import os
import re
import pymongo
import random
import time
import string

reload(sys)
sys.setdefaultencoding('utf-8')

charset = 'utf-8'

class Analysis():
	"analysis weibo text and make store"
	def __init__(self):
		# self.divs_tyle = '<div.*?class=\\"WB_feed_type SW_fun S_line2 \\">'
		print 'start Analysis'
		self.divs_tyle = 'WB_feed_type SW_fun S_line2'
		self.saveDir = "." +os.sep + "data"
		self.divpattern = re.compile("<div(.+?)</div>",re.S)
		# self.text_pattern = re.compile("<em>(.+?)<\\\/em>",re.S)
		self.text_pattern = re.compile("<div.+?WB_text.+?>.{2}(.+?)<\\\/div>",re.S) # get time block 
		self.time_pattern = re.compile('(<a name=\d+.*?S_link2 WB_time.*?<\\\/a>)',re.S) # get date
		self.data_pattern = re.compile('date=\\\\"(\d+)',re.S)
		self.media_tpattern = re.compile('(<a class=\\\\"S_func2 WB_time\\\\".*?<\\\/a>)',re.S)
		self.format = '%Y-%m-%d %H:%M:%S'
		self.weiboc_pattern = re.compile('<strong.*?weibo.*?(\d+)<\\\/strong>',re.S)
		#<strong node-type=\"weibo\">7071<\/strong> 
		# <strong node-type="fans">63023964</strong>
		#   <div class=\"WB_text\" node-type=\"feed_list_content\" nick-name=\"姚晨\">\n
	def get_weibo_text(self,filename):
		# content = '<div class="WB_text" node-type="feed_list_reason"><em>【冬日里的正能量】天寒地冻，如果你遇到一个11岁没穿外套的小男孩，寒风中瑟瑟发抖，你会伸出援助之手吗？挪威的一个儿童慈善组织用隐藏的摄像机拍下了路人的反应，有人送上围巾、手套，甚至有人脱到只剩一件外衣，整个过程看得让人人心一暖。</em>'
		fread = open(filename,'r')
		content = fread.read()
		# print content
		contents = self.text_pattern.findall(content)
		for strip in contents:
			print strip

	# def make_weibo_store():
	def get_weibo_div(self,content,uid):  #uname zan shi bu jia  ,yi hou jia 
		# fread = open(filename,'r')
		# content = fread.read()
		# print content
		content = content.encode("utf-8")
		# print content
		contents = re.split(self.divs_tyle,content)
		for strip in contents:                                     #get each weibo html's info 
			texts = self.text_pattern.findall(strip)
			num = len(texts)
			while(num!=0):
				time = self.time_pattern.findall(strip)
				mtime = self.media_tpattern.findall(strip)
				if num == 1:
					own_weibo = texts[0]
					media_weibo = ''
				else:
					own_weibo = texts[0]
					media_weibo = texts[1] 
				# print own_weibo
				# print media_weibo
					# print text  #str(text).encode("utf-8")
				for t in time:
					date = self.data_pattern.findall(t)[0]
					# print date
				# if mtime is None:
				mdate = ''
				# else:
				for mt in mtime:
					mdate = self.data_pattern.findall(mt)[0]
				# print mdate 
				record = dict(own_weibo=own_weibo,media_weibo=media_weibo,media_time=mdate,weibo_time=date)
				store = Store()
				store.weibo_store(uid,own_weibo,media_weibo,mdate,date)
				print 'one page stored!'
				break
	def page_count(self,filename):  #uname zan shi bu jia  ,yi hou jia 
		fread = open(filename,'r')
		content = fread.read()
		content = content.encode("utf-8")
		count = self.weiboc_pattern.findall(content)
		for c in count:
			weibo_num = string.atoi(c)
			print weibo_num
			page_num = weibo_num/45+1
		print page_num 


class Store:
	"store weibo text into mongodb"
	def __init__(self):
		conn = pymongo.Connection("localhost",27017)
		print conn
		self.db = conn.sina
		if(self.db):
			print 'mongodb connected!'
	def weibo_store(self,uid,own_weibo,media_weibo,mdate,date):
		result = self.db.weibo.insert({'uid':uid,'weibo':{'own_weibo':own_weibo,'media_weibo':media_weibo,'media_time':mdate,'weibo_time':date}})  #name hui jia shang 
		if(result):
			print "a record stored!"
		else:
			print "store faild!"
if __name__=='__main__':
	filename = '/home/adiking/ustc_practice/falcon/crawler/andos_demo/data/1266321801content.html'
	ob = Analysis()
	# ob.get_weibo_text(filename)
	# ob.get_weibo_div(filename)
	# ss = Store()
	ob.page_count(filename)

		