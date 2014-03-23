#!/usr/bin/env python
# coding=utf-8

import ConfigParser
import pymongo

class MongoConnection():
    def __init__(self):
        config = ConfigParser.SafeConfigParser()
        config.read("settings.ini")
        self.conn = pymongo.Connection(config.get("mongodb", "host"), int(config.get("mongodb", "port")))

    def get_connection(self):
        return self.conn

    def get_database(self, dbname):
        try:
            return self.conn[dbname]
        except:
            print "open database failed!"

    def get_collection(self, dbname, collection_name):
        try:
            return self.conn[dbname][collection_name]
        except:
            print "get collection failed!"

if __name__ == '__main__':
    mc = MongoConnection()
    conn = mc.get_connection()
