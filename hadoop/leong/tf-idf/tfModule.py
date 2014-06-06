#!/usr/bin/env python
#coding=utf-8

##tf
import jieba
from pymongo import *
import os
import os.path
import json

def df(ip, dbName, collectionName, fieldName, sortBy, skip, limit):
	con = Connection(ip)
	#print con
	db = con[dbName]
	#print db
	collection = db[collectionName]
	#print collection
	for text in collection.find().sort(sortBy, 1).skip(skip).limit(limit):
		tId = text[sortBy]
		#print tId
		segOne = jieba.cut(text[fieldName], cut_all=False)
		count = 0.0
		df = list()
		wordslist = dict()
		for i in segOne:
			if wordslist.has_key(i):
				wordslist[i] += 1  #key: weibo text word ;value: how many times this word appears in this weibo text
			else:
				wordslist[i] = 1
			count += 1  #total words of each weibo text
		mongoInsert = dict()
		for i in range(len(wordslist)):
			df.append(wordslist.values()[i]/count)
			mongoInsert[wordslist.keys()[i].encode('utf-8')] = df[i]
		#print "mongoInsert: "
		mongoInsert = json.dumps(mongoInsert)
		# for j in range(len(mongoInsert)):
		# 	print "key: ", mongoInsert.keys()[j], "values: ", mongoInsert.values()[j]
		#print "##################################################################"
		collection.update({"_id":tId}, {"$set": {"tf":mongoInsert}}, upsert = True)
		targetFile = "/tmp/jieba.cache"
		if os.path.isfile(targetFile):
			os.remove(targetFile)

if __name__ == '__main__':
	numRec = 589942
	print "start"
	skip = 0
	limit = 1000
	for skip in range(550000, 590001, limit):
		df(ip = "localhost", dbName = "weibo", collectionName = "text", fieldName = "text", sortBy = "_id", skip = skip, limit = limit)
	print "Done"