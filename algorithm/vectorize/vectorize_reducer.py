#!/usr/bin/env python
#coding=utf-8

from pymongo import *
import sys
import json

def vectorizeReducer(inIp, inDbName, inCollectionName):
	
	inCon = Connection(inIp)
	inDb = inCon[inDbName]
	inCollection = inDb[inCollectionName]
	# outCon = Connection(outIp)
	# outDb = outCon[outDbName]
	# outCollection = outDb[outCollectionName]
	outCollection = Connection().weibo.test
	count = 0
	newline = list()
	res = dict()#针对一条微博blogId:[vector]
	for n in inCollection.find().sort('wordId', -1).limit(1):
		n = n['wordId']#向量长度
	for line in sys.stdin:#针对一条微博的一个单词
		newline = line.strip().split('\t') #blogId@word\ttf
		blogWord = newline[0].split('@')
		blogId = blogWord[0]
		word = eval('u"%s"'%blogWord[1])
		wordId = inCollection.find_one({"word": word})['wordId']#start from 0
		wordIdf = inCollection.find_one({"word": word})['idf']
		tf = newline[1]
		tfIdf = float(tf) * float(wordIdf)
		if res.has_key(blogId):
			res[blogId][wordId] = tfIdf
		else:
			res[blogId] = [0 for i in range(n+1)]
			res[blogId][wordId] = tfIdf
	for i in range(len(res)):
		print int(res.keys()[i]), res.values()[i]
		key = int(res.keys()[i])
		value = json.dumps(res.values()[i])
		outCollection.update({"_id": key}, {"$set": {"vector": value}}, upsert = True)


if __name__ == '__main__':
	inIp = 'localhost'
	inDbName = 'weibo'
	inCollectionName = 'idf_test'
	outIp = 'localhost'
	outDbName = 'weibo'
	outCollectionName = 'test'
	vectorizeReducer(inIp, inDbName, inCollectionName)