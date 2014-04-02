#!//usr/bin/env python
#coding=utf-8

from pymongo import *

def vectorizeMapper(ip, dbName, collectionName):
	con = Connection(ip)
	db = con[dbName]
	collection = db[collectionName]
	tf = dict()
	# output = open("/home/hadoop/python/input", 'a')
	for blogText in collection.find():
		# print blogText['tf']
		tf = dict(eval(blogText['tf'].encode('utf-8')))
		blogId = blogText['_id']
		for i in range(len(tf)):
			if tf.keys()[i] != ' ':
				key = str(blogId) + '@' + tf.keys()[i] #tf.keys()[i] => word
				value = tf.values()[i]
				print '%s\t%s' % (key, value)
				# print type(tf.keys()[i].decode('utf-8')), tf.keys()[i].decode('utf-8').encode('gbk')
				# output.write(key + '\t' + str(value) + '\n')


if __name__ == '__main__':
	ip = 'localhost'
	dbName = 'weibo'
	collectionName = 'test'
	vectorizeMapper(ip, dbName, collectionName)