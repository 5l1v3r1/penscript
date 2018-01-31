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
"127.0.0.1:8080",


]


resultDic = {}
threadList = []
resultList = []

def _curl(protocol,target,i,timeout=3):
    dic = {}
    dic['id'] = str(i) 
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

def curl(threadId,timeout,threadNum):
    for i in xrange(threadId,len(targetList),threadNum):
        dic = _curl('http',targetList[i],i,timeout)
        resultList.append(dic)
        
def scan(threadNum,timeout):
    print "Run start: Total " + str(len(targetList)) + " request!"
    for threadId in xrange(0,threadNum):
        t = threading.Thread(target=curl,args=(threadId,timeout,threadNum,))
        t.start()
        threadList.append(t)
    for num in xrange(0,threadNum):
        threadList[num].join()
    print "\r\nRun over !"

def printlog(key,out):
    print "Start to output!"
    resList =  sorted(resultList,key = lambda e:e.__getitem__(key))
    temp = "NoNasdon!asd32@NoneNone"
    if out!=None:
        with open(out,'wb') as f :
            for value in resList:
                if temp != value[key] and key != 'id' :
                    try:
                        f.write( "\r\n["+value[key]+"]\r\n")
                    except:
                        f.write("\r\n[GBK Code Error]\r\n")
                f.write(value['target'] + "  - " + value['status'] + "  - " + value['head_allow']+'\r\n')
                temp = value[key]
        print "Save result into "+ out
    else:
        for value in resList:
            if temp != value[key] and key != 'id' :
                try:
                    print "\r\n["+value[key]+"]"
                except:
                    print "\r\n[GBK Code Error]"
            print value['target'] + "  - " + value['status'] + "  - " + value['head_allow']
            temp = value[key]
    print "\r\nEnd output!"

def argSet(parser):
    parser.add_argument("-K", "--key", type=str, help="The order key e.g. title、status、host", default="title")
    parser.add_argument("-T", "--timeout", type=str, help="Timeout", default="3")
    parser.add_argument("-F", "--file",type=str, help="Load ip dictionary e.g. 192.168.1.2:8080", default=None)
    parser.add_argument("-O", "--out",type=str, help="output file e.g res.txt", default=None)
    parser.add_argument("-N", "--threadnum",type=int, help="Thread Num e.g. 10", default=10)
    return parser


def handle(args):
    key = args.key
    timeout = args.timeout
    filename = args.file
    out = args.out
    threadnum = args.threadnum
    if key not in ['title','status','host','head_allow','id']:
        key = 'title'

    if filename != None:
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                for line in f.readlines():
                    myline = line.strip('\r').strip('\n')
                    targetList.append(myline)
        else:
            print "The path is not exist!"
    scan(threadnum,timeout)
    printlog(key,out)

if __name__=='__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser = argSet(parser)
    args = parser.parse_args()
    handle(args)




