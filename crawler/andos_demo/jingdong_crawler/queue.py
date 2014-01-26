#!/usr/bin/python
# -*- coding: utf-8 -*-

#create by Andos he
#h.chujienados@gmail.com

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SocketServer import ThreadingMixIn 
class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):pass
class Queue:
    def __init__ (self):
        self.queue = list()
        self.length = 0
        print self.length

    def Input(self, argument):
        self.queue.append(argument)
        self.length += 1
        print self.length

    def Output(self):
        print self.length
        argument = self.queue[0]
        self.queue = self.queue[1:]
        self.length -= 1
        return argument

if __name__ == '__main__':
    server_object = Queue()
    server = ThreadXMLRPCServer(("localhost", 2310), allow_none = True)
    server.register_instance(server_object)
    server.serve_forever()
