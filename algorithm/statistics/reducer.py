#!/usr/bin/env python
#coding=utf-8

import sys
import pymongo

def get_collection(collectionname):
    mongo = pymongo.Connection("localhost", 27017)["weibo"]
    return mongo[collectionname]

def run():
    collection = get_collection("provinces")
    keylist = dict()
    provinceinfo = dict()
    for line in sys.stdin:
        try:
            key, value = line.rstrip().split('\t', 1)
            key = int(key)
            value = int(value)
        except:
            continue
        if keylist.has_key(key):
            keylist[key]["population"] += 1
            if(value == 0):
                keylist[key]['m'] += 1
            elif(value == 1):
                keylist[key]['f'] += 1
        else:
            tmp = dict()
            tmp["population"] = 1
            if(value == 0):
                tmp['m'] = 1
                tmp['f'] = 0
            elif(value == 1):
                tmp['m'] = 0
                tmp['f'] = 1
            else:
                tmp['m'] = 0
                tmp['f'] = 0       

            keylist[key] = tmp

    for province in collection.find():
        pro_id = province["id"] * 100
        count = 0
        count_m = 0
        count_f = 0
        for city in province["citys"]:
            code = pro_id+int(city["cid"])
            if not keylist.has_key(code):
                continue
            city["population"] = keylist[code]["population"]
            count += keylist[code]["population"]
            city["m"] = keylist[code]["m"]
            count_m += keylist[code]["m"]
            city["f"] = keylist[code]["f"]
            count_f += keylist[code]["f"]
        province["population"] = count
        province["m"] = count_m
        province["f"] = count_f
        collection.save(province)

if __name__ == '__main__':
    run()
