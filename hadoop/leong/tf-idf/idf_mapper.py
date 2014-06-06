#!/usr/bin/env python
#coding=utf-8

##idf
from pymongo import *
import json

con = Connection()
db = con.weibo
collection = db.test
tf = dict()
for text in collection.find().limit(5):
	tf = json.loads(text['tf'])
	#print len(tf)
	# print tf
	for i in range(len(tf)):
		# print tf.keys()[i].encode('utf-8'), float(tf.values()[i])
		print '%s\t%s' % (tf.keys()[i].encode('utf-8'), 1)