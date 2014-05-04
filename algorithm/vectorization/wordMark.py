#!/usr/bin/env python
#coding=utf-8

import pymongo

def get_collection():
    mongo = pymongo.Connection("192.168.40.161", 27017)["weibo"]
    return mongo["idf"] 

def run():
	collection = get_collection()
	wordId = 0
	print collection.find().count()
	for text in collection.find():
		text["id"] = wordId
		collection.save(text)
		wordId += 1



if __name__ == '__main__':
	run()