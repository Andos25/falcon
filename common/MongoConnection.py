#!/usr/bin/env python
# coding=utf-8

import ConfigParser
import pymongo

class MongoConnection():
    def __init__(self):
        config = ConfigParser.SafeConfigParser()
        config.read("settings.ini")
        self.conn = pymongo.Connection(config.get("mongodb", "host"), int(config.get("mongodb", "port")))

    def getConn(self):
        return self.conn

    def getdbname(self, dbname):
        try:
            return self.conn[dbname]
        except:
            print "open database failed!"

if __name__ == '__main__':
    mc = MongoConnection()
    conn = mc.getConn()
