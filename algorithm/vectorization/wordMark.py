#!/usr/bin/env python
#coding=utf-8

import pymongo

def get_collection():
    mongo = pymongo.Connection("master", 27017)["weibo"]
    return mongo["idf"] 

def run():
	collection = get_collection()
	wordId = 0
	print collection.find().count()
	for text in collection.find():
		# text["id"] = wordId
		collection.update({"_id":text["_id"]}, {"$set":{"id": wordId}}, True)
		# collection.save(text)
		wordId += 1



if __name__ == '__main__':
	run()