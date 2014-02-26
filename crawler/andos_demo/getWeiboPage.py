#!/usr/bin/env python
#coding=utf-8

import urllib
import urllib2
import sys
import time
import Analysis

reload(sys)
sys.setdefaultencoding('utf-8')

class getWeiboPage:
	body = {
		# '__rnd':'',
		# '_k':'',
		# '_t':'0',
		# 'count':'50',
		# 'end_id':'',
		# 'max_id':'',
		# 'page':1,
		# 'pagebar':'',
		# 'pre_page':'0',
		# 'uid':''
			'domain':'100306',
			'pre_page':'1',
			'page':'1',
			'max_id':'',
			'end_id':'',
			'count'	:'15',
			'pagebar':'',
			'max_msign':'',
			'filtered_min_id':'',
			'pl_name':'Pl_Official_LeftProfileFeed__21',
			'id':'1003061266321801',
			'script_uri':'/p/1003061266321801/weibo',
			'feed_type':'0',
			'from':'page_100306',
			'wvr':'5',
			'mod':'headweibo',
			'__rnd':''
		}
   	charset = 'utf-8'

	def __init__(self):
		self.ajax_url = 'http://weibo.com/p/aj/mblog/mbloglist?'
		uid_list = []


	def get_msg(self,uname,uid,pid,page_num):
		print page_num
		for num in range(1,page_num):
			print num
			url = self.weibo_url(uid,pid)
			text = self.get_firstpage(url)
			# self.get_secondpage()
			# self.get_thirdpage()
			analy = Analysis.Analysis()
			analy.get_weibo_div(text,uname,uid)
			url = self.next_url(uid,pid,num)
			text = self.get_firstpage(url)
	def get_firstpage(self,url):
		# getWeiboPage.body['pre_page'] = getWeiboPage.body['page']-1
		# url = self.weibo_url(uid,pageid)
		print url
		req = urllib2.Request(url)
		result = urllib2.urlopen(req)
		text = result.read()
		# print text	
		# self.writefile('./result1',eval("u'''"+text+"'''"))
		return text
		
	def get_secondpage(self):
	#	getWeiboPage.body['end_id'] = '3679266073819194'
	#	getWeiboPage.body['max_id'] = '3487344294660278'
		getWeiboPage.body['pagebar'] = '0'
		getWeiboPage.body['pre_page'] = getWeiboPage.body['page']

		url = self.ajax_url +urllib.urlencode(getWeiboPage.body)
		print url
		req = urllib2.Request(url)
		result = urllib2.urlopen(req)
		text = result.read()
		text = text.encode("UTF-8")
		self.writefile('./text2',text)		
		# self.writefile('./result2',eval("u'''"+text+"'''"))
	def get_thirdpage(self):
		getWeiboPage.body['count'] = '15'
		getWeiboPage.body['pagebar'] = '1'
		getWeiboPage.body['pre_page'] = getWeiboPage.body['page']

		url = self.ajax_url +urllib.urlencode(getWeiboPage.body)
		print url
		req = urllib2.Request(url)
		result = urllib2.urlopen(req)
		text = result.read()
		text = text.encode("UTF-8")
		self.writefile('./text3',text)		
		# self.writefile('./result3',eval("u'''"+text+"'''"))
	def weibo_url(self,uid,pageid):
		url = 'http://weibo.com/p/' + pageid+uid + '/weibo?from=page_'+pageid+'&wvr=5&mod=headweibo'
		# http://weibo.com/p/1003061266321801/weibo?from=page_100306&wvr=5&mod=headweibo
		# http://weibo.com/p/1003061266321801/weibo?is_search=0&visible=0&is_tag=0&profile_ftype=1&page=1#feedtop
		return url
	def next_url(self,uid,pageid,pagecount):
		next_url = 'http://weibo.com/p/'+str(pageid)+str(uid)+'/weibo?is_search=0&visible=0&is_tag=0&profile_ftype=1&page='+str(pagecount)+'#feedtop'
		return next_url

	def weibo_ajax_url(self,uid,pageid,servertime):
		ajax_url = 'http://weibo.com/p/aj/mblog/mbloglist?'+urllib.urlencode(getWeiboPage.body)
		return ajax_url
	def get_uid(self,filename):
		fread = file(filename)
		for line in fread:
			getWeiboPage.uid_list.append(line)
			print line
			time.sleep(1)
	def writefile(self,filename,content):
		fw = open(filename,'a')
		fw.write(content)
		fw.close()