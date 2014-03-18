#!/usr/bin/env python
#coding=utf-8

##idf
from pymongo import *
import json

def idf_mapper(ip, dbName, collectionName, sortBy, skip, limit):
    con = Connection(ip)
    db = con[dbName]
    collection = db[collectionName]
    tf = dict()
    for text in collection.find().sort(sortBy, 1).skip(skip).limit(limit):
        tf = json.loads(text['tf'])
        for i in range(len(tf)):
            if (tf.keys()[i].encode('utf-8') != ' '):
                print '%s\t%s' % (tf.keys()[i].encode('utf-8'), 1)

if __name__ == '__main__':
	ip = 'localhost'
	dbName = 'weibo'
	collectionName = 'test'
	sortBy = '_id'
	skip = 0
	limit = 5
	idf_mapper(ip, dbName, collectionName, sortBy, skip, limit)