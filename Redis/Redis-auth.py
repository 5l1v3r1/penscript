#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'


import redis
import ipaddr
import threading
import os
import sys
import socket
import time
import optparse

reload(sys)
sys.setdefaultencoding("utf8")
targetsList = []
threadNum = 10
threadList = []

def readdFile(filename):
    with open(filename, "r") as f:
        for line in f.readlines():
            address = line.strip().split(":")
            host = address[0]
            port = 6379
            if(len(address)>1):
                port = address[1]
            targetDic = {
                'host': host,
                'port': port,
            }
            targetsList.append(targetDic)


def exploit_redis(threadId):
    for i in xrange(threadId,len(targetsList),threadNum):
        try:
            r = redis.Redis(host=targetsList[i]['host'], port=targetsList[i]['port'])
            targetsList[i]['info'] = r.info()
            print "\r\n[+] " + targetsList[i]['host']+ ':' + targetsList[i]['port'] +  " exist auth vulner!",
        except:
            print "\r\n[-] " + targetsList[i]['host'] + ':' + targetsList[i]['port'],


def main():
    option = optparse.OptionParser()
    option.add_option('-f', dest='filename', default="targets.txt")
    option.add_option('-t', dest='host', default=None)
    option.add_option('-p', dest='port', default='6379')
    (options, args) = option.parse_args()

    if options.filename != None:
        if os.path.isfile(options.filename):
            readdFile(options.filename)
        else:
            print "\r\nThe path is not exist!",

    if not options.host == None:
        targetDic = {
            'host': options.host,
            'port': options.port,
            'info': "",
            'flag': False
        }
        targetsList.append(targetDic)

    print "Run start !"
    for threadId in xrange(0,threadNum):
        t = threading.Thread(target=exploit_redis,args=(threadId,))
        t.start()
        threadList.append(t)
    for num in xrange(0,threadNum):
        threadList[num].join()
    print "Run over !"


if __name__=='__main__':
    main()
