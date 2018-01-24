#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'
import threading
import requests
import argparse
import os
from bs4 import BeautifulSoup

'''
    批量检测目标是否属于Web应用
    用法：
        python curl.py -K title -T 3 -F file.txt
        python curl.py -K status -F file.txt
        python curl.py -F file.txt

'''


targetList = [
"127.0.0.1:8080"

]


key = "title"
timeout = 3
resultDic = {}
threadList = []
threadNum = 10

def _curl(protocol,target):
    dic = {}
    dic['host'] = target.split(':')[0]
    url = protocol + "://" +target
    try:
        result = requests.get(url, timeout=int(timeout),verify=False)
        soup = BeautifulSoup(result.text)
        dic['target'] = url
        dic['status'] = str(result.status_code)
        dic['flag'] = True
        dic['host'] = target
        if soup.title == None or soup.title.string ==None or soup.title.string =='':
            dic['title'] = "None Title"
        else:
            dic['title'] = soup.title.string
        
    except:
        dic['title'] = "Curl Failed"
        dic['status'] = "0"
        dic['target'] = target
        dic['host'] = target
        dic['flag'] = False
  
    try:
        result1 = requests.options(url+"/testbyah", timeout=int(timeout))
        dic['head_allow'] = result1.headers['Allow']
    except:
        dic['head_allow'] = "Curl Failed"

        
    return dic

def curl(threadId):
    for i in xrange(threadId,len(targetList),threadNum):
        dic = _curl('http',targetList[i])
        if dic['flag'] == False:
            dic = _curl('https', targetList[i])
        if not resultDic.has_key(dic.get(key)):
            resultDic[dic.get(key)] = []
        resultDic[dic.get(key)].append(dic)


def scan():
    print "Run start: Total " + str(len(targetList)) + " request!"
    for threadId in xrange(0,threadNum):
        t = threading.Thread(target=curl,args=(threadId,))
        t.start()
        threadList.append(t)
    for num in xrange(0,threadNum):
        threadList[num].join()
    print "\r\nRun over !"

def printlog():
    for key in resultDic:
        print "["+key+"]"
        for result in resultDic[key]:
            print result['target'] + "  - " + result['status'] + "  - " + result['head_allow']
        print "\r\n"

def argSet(parser):
    parser.add_argument("-K", "--key", type=str, help="The order key e.g. titile、status、host", default="title")
    parser.add_argument("-T", "--timeout", type=str, help="Timeout", default="3")
    parser.add_argument("-F", "--file",type=str, help="Load ip dictionary e.g. 192.168.1.2:8080", default=None)
    return parser


def handle(args):
    key = args.key
    timeout = args.timeout
    file = args.file
    if key not in ['titile','status','host','head_allow']:
        key = 'title'

    if file != None:
        if os.path.isfile(file):
            with open(file, 'r') as f:
                for line in f.readlines():
                    myline = line.strip('\r').strip('\n')
                    targetList.append(myline)
        else:
            print "The path is not exist!"
    scan()
    printlog()

if __name__=='__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser = argSet(parser)
    args = parser.parse_args()
    handle(args)




