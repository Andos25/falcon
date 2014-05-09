#!/usr/bin/env python
#coding=utf-8

from pymongo import *

def wordMark(ip, dbName, collectionName):
	con = Connection(ip)
	db = con[dbName]
	collection = db[collectionName]

	wordId = 0
	for text in collection.find():
		word = text['word']
		collection.update({"word": word}, {"$set": {"wordId":wordId}}, upsert = True)
		print word.encode('utf-8'), wordId
		wordId += 1



if __name__ == '__main__':
	wordMark('localhost', 'weibo', 'idf', )
