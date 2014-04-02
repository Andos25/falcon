
import urllib
import urllib2
import sys
import time
import os
import re
import pymongo
import random
import time
from bson import ObjectId

reload(sys)
sys.setdefaultencoding('utf-8')

charset = 'utf-8'

class Store:
	"store weibo text into mongodb"
	def __init__(self):
		print "begin!"
		self.img_pattern = re.compile("<img\s*.*?>",re.S) # get time block
		self.last_pattern = re.compile("<\/\w+>\\\n",re.S)
		self.splite_pattern = re.compile("<\w+.*?>")
		conn = pymongo.Connection("localhost",27017)
		self.db = conn.falcon
		if(self.db):
			print 'mongodb connected!'

	def weibo_store(self,uname,uid,own_weibo,media_weibo,mdate,date):
		result = self.db.weibo.save({'uname':uname,'uid':uid,'weibo':{'own_weibo':own_weibo,'media_weibo':media_weibo,'media_time':mdate,'weibo_time':date}})  
		if(result):
			print "1 record stored!"
		else:
			print "store faild!"

	def fans_store(self,uname,uid,fansid,fansname):
		result = self.db.fans.save({'uname':uname,'uid':uid,'used':'0','fans':{'fansid':fansid,'fansname':fansname}})
		print result
		if(result):
			print "a fans stored!"
			return True
		else:
			print "fans store faild!"
			return False

	def million_record(self):
		result = self.db.ptext.find().limit(50)
		print result
		for r in result:
			print r
			# print r['fans']['fansname']
			self.db.ptext1.save({ "_id" :r["_id"], "favorited" : r["favorited"], "user_id" :r["user_id"] , "truncated" :r["truncated"] , "text" :r["text"], "created_at" :r["created_at"], "source" : r["source"] })

	def fans_mark(self,ob_id):
		result = self.db.fans.update({"_id":ObjectId(ob_id)},{"$set":{"used":'1'}})
		# result = self.db.fans.update({'_id':ob_id},{'$set':{'used':'1'}})
	def weibo_wash(self):

		result = self.db.fans.find()
		for r in result:
			# print r
			# text1 = r['weibo']['own_weibo']
			text2 = r['weibo']['media_weibo']
			# text = text1+text2
			uid = r['uid']
			uname = r['uname']
			# print text1
			# print text2
			# self.a_pattern.sub('',text)
			# self.img_pattern.sub('',text2)
			text = self.splite_pattern.split(text2)
			text = "".join(text)
			text.decode("utf-8")
			text.encode("utf-8")
			print text
			file_object = open('./test.txt', 'a')
			file_object.write(uid+'    '+uname+'      '+text+'\n')
			file_object.close( )



if __name__=='__main__':
	ob = Store()
	# ob.one_record()
	# ob.weibo_wash()
	ob.million_record()
