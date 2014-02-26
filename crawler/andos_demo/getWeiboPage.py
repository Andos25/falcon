#!/usr/bin/env python
#coding=utf-8

import urllib
import urllib2
import sys
import time
import Analysis
import login

reload(sys)
sys.setdefaultencoding('utf-8')

class getWeiboPage:
	body = {
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
		for num in range(1,page_num):
			print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>page"+str(num)
			url = self.next_url(uid,pid,num)
			text = self.get_firstpage(url)
			text2 = self.get_secondpage(pid,uid,num)
			text3 = self.get_thirdpage(pid,uid,num)
			text = text + text2 + text3
			# print text
			analy = Analysis.Analysis()
			analy.get_weibo_div(text,uname,uid)
			print '>>>>>>>>>>>>>>>>1 page stored!'
			url = self.next_url(uid,pid,num)
			text = self.get_firstpage(url)
	def get_firstpage(self,url):
		print url
		req = urllib2.Request(url)
		result = urllib2.urlopen(req)
		text = result.read()
		return text
		
	def get_secondpage(self,pid,uid,num):
		getWeiboPage.body['pagebar'] = 0
		getWeiboPage.body['pre_page'] = num
		getWeiboPage.body['page'] = num
		getWeiboPage.body['domain'] = pid
		getWeiboPage.body['id'] = str(pid)+str(uid)
		getWeiboPage.body['script_uri'] = '/p/'+str(pid)+str(uid)+'/weibo'
		getWeiboPage.body['from'] = 'page_'+str(pid)
		if (num>1):
			getWeiboPage.body['is_search'] = 0
			getWeiboPage.body['visible'] = 0
			getWeiboPage.body['is_tag'] = 0
			getWeiboPage.body['profile_ftype'] = 1
		# print getWeiboPage.body
		# getWeiboPage.body['pre_page'] = getWeiboPage.body['page']
		url = self.ajax_url +urllib.urlencode(getWeiboPage.body)
		# print url
		req = urllib2.Request(url)
		result = urllib2.urlopen(req)
		text = result.read()
		# text = text.encode("UTF-8")		
		# self.writefile('./result2',eval("u'''"+text+"'''"))
		# print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.AJAX 1"
		# print text
		return text
	def get_thirdpage(self,pid,uid,num):
		getWeiboPage.body['pagebar'] = 1
		# getWeiboPage.body['pre_page'] = getWeiboPage.body['page']
		getWeiboPage.body['pre_page'] = num
		getWeiboPage.body['page'] = num
		getWeiboPage.body['domain'] = pid
		getWeiboPage.body['id'] = str(pid)+str(uid)
		getWeiboPage.body['script_uri'] = '/p/'+str(pid)+str(uid)+'/weibo'
		getWeiboPage.body['from'] = 'page_'+str(pid)
		if (num>1):
			getWeiboPage.body['is_search'] = 0
			getWeiboPage.body['visible'] = 0
			getWeiboPage.body['is_tag'] = 0
			getWeiboPage.body['profile_ftype'] = 1		
		# print getWeiboPage.body
		url = self.ajax_url +urllib.urlencode(getWeiboPage.body)
		# print url
		req = urllib2.Request(url)
		result = urllib2.urlopen(req)
		text = result.read()
		# print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.AJAX 2"
		# print text
		# text = text.encode("UTF-8")		
		# self.writefile('./result3',eval("u'''"+text+"'''"))
		return text
	def weibo_url(self,uid,pid):
		url = 'http://weibo.com/p/' + str(pid)+str(uid) + '/weibo?from=page_'+str(pid)+'&wvr=5&mod=headweibo'
		return url
	def next_url(self,uid,pid,num):
		next_url = 'http://weibo.com/p/'+str(pid)+str(uid)+'/weibo?is_search=0&visible=0&is_tag=0&profile_ftype=1&page='+str(num)+'#feedtop'
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

# if __name__=='__main__':
# 	login.weiboLogin()
# 	ob = getWeiboPage()
# # 	# ob.get_weibo_text(filename)
# 	uname = 'Kafka桑'
# 	pid = '100505'
# 	uid = '1766325471'
# 	page_num =10
# 	ob.get_msg(uname,uid,pid,page_num)
# # 	# ss = Store()