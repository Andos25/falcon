#!/usr/bin/env python
#coding=utf-8

import sys
import random

def getFile():
	return open("/home/hadoop/kmeansdata/vector32w.txt", 'r')

#判断centerList中的每个向量与vectors中的每个向量是否正交，返回第一个正交的vector，若与vectors中的每个向量都不正交则返回“”
def isOrthogonal(centerList, vectors):#center:string; vectors:list
	widCol = []
	for i in range(0, len(centerList)):
		tmpcl = centerList[i].replace("{","").replace("}","").split(",")
		for j in range(0, len(tmpcl)):#widCol is a list of all centers' wordid
			widCol.append(tmpcl[j].split(":")[0])
	# print "widCol: ", widCol, '\n'
	for vector in vectors:
		orth = 1
		vector = "".join(vector.split("\t")[1].split())
		tmpList = vector.replace("{","").replace("}","").split(",")
		for p in range(0, len(tmpList)):
			# print "wordid: ", tmpList[p].split(":")[0], '\n'
			if tmpList[p].split(":")[0] in widCol:
				orth = 0
				break
		if orth:
			return vector
	return ""


def run():
	f = getFile()
	vectors = f.readlines()
	fstV = int(random.uniform(1, len(vectors)))
	centerList = list()
	centerList.append("".join(vectors[fstV-1].split("\t")[1].split()))
	flag = 1
	while flag:
		res = isOrthogonal(centerList, vectors)
		if res == "":
			flag = 0
		else:
			centerList.append(res)
	fw = open("/home/hadoop/kmeansdata/clustercenter32w.txt", 'w')
	for k in range(0, len(centerList)):
		fw.write(centerList[k])
	# print centerList, len(centerList)



if __name__ == '__main__':
	run()
		