#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'
import threading
import requests
import argparse
import sys 
import os
import platform
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#reload(sys)
#sys.setdefaultencoding('utf-8')
'''
    批量检测目标是否属于Web应用，并检测关键词，以及得到http请求方法
    Usage:
        python curl.py -K title -T 3 -F file.txt
        python curl.py -K status -F file.txt
        python curl.py -F file.txt -V
        python curl.py -F file.txt -S admin,管理,后台 -N 100 -V 
    目标格式:
        http://www.baidu.com
        http://192.168.1.11
        http://192.168.1.22:80
'''
#sysstr = platform.system() 
targetList = []
resultDic = {}
threadList = []
resultList = []
def _curl(target,i,timeout=3):
    dic = {}
    dic['id'] = str(i) 
    dic['host'] = target.split(':')[0].strip('https://').strip('http://')
    url = target.strip(' ')
    try:
        result = requests.get(url, timeout=int(timeout),verify=False)
        soup = BeautifulSoup(result.text)
        dic['target'] = url
        dic['status'] = str(result.status_code)
        dic['flag'] = True
        dic['host'] = target
        mytitle =  soup.title.string
        content =  result.text
        for searchkey in searchList:
            if searchkey in mytitle.encode(result.encoding).decode('utf-8').encode(type) or searchkey in content.encode(result.encoding).decode('utf-8').encode(type):
                # print searchkey,mytitle.encode(result.encoding).decode('utf-8').encode(type)
                dic['search'].append(searchkey)
        if mytitle == None or mytitle =='':
            dic['title'] = "None Title"
        else:
            dic['title'] =  mytitle.encode(result.encoding)
    except:
        dic['title'] = "Curl Failed"
        dic['status'] = "0"
        dic['target'] = target
        dic['host'] = target
        dic['flag'] = False
    url = target.strip(' ')
    try:
        result1 = requests.options(url+"/testbyah", timeout=int(timeout))
        dic['head_allow'] = result1.headers['Allow']
    except:
        dic['head_allow'] = "Not Allow"
    return dic

def curl(threadId,timeout,threadNum,verbose):
    for i in xrange(threadId,len(targetList),threadNum):
        dic = _curl(targetList[i],i,timeout)
        resultList.append(dic)
        if verbose and  dic['status'] !="0" :
            try:
                print "[%s] %s - %s - %s - %s\r\n" % (dic['id'],dic['target'],dic['status'],dic['title'].decode('utf-8').encode(type),','.join(dic['search'])),
            except:
                print "[%s] %s - %s - %s - %s\r\n" % (dic['id'],dic['target'],dic['status'],"Title Code Error",','.join(dic['search'])),
def scan(threadNum,timeout,verbose,searchList):
    print "[.] Run start: Total " + str(len(targetList)) + " request!"
    for threadId in xrange(0,threadNum):
        t = threading.Thread(target=curl,args=(threadId,timeout,threadNum,verbose,searchList,))
        t.start()
        threadList.append(t)
    for num in xrange(0,threadNum):
        threadList[num].join()
    print "\r\n[.] Run over!"

def printlog(key,out):
    print "=================== Order by " + key + " ======================="
    print "[.] Start to output!"
    resList =  sorted(resultList,key = lambda e:e.__getitem__(key))
    temp = "NoNasdon!asd32@NoneNone"
    if out!=None:
        with open(out,'wb') as f :
            for value in resList:
                if temp != value[key] and key != 'id' :
                    try:
                        f.write("\r\n["+value[key].decode('utf-8').encode(type)+"]\r\n")
                    except:
                        f.write("\r\n[Title Code Error]\r\n")
                try:
                    f.write("[%s] %s - %s - %s - %s\r\n" % (value['status'],value['target'],value['head_allow'],value['title'].decode('utf-8').encode(type),','.join(value['search'])))
                except:                
                    f.write("[%s] %s - %s - %s - %s\r\n" % (value['status'],value['target'],value['head_allow'],"[Title Code Error]",','.join(value['search'])))
                temp = value[key]
        print "[.] Save result into "+ out + "!"
    else:
        for value in resList:
            if temp != value[key] and key != 'id' :
                try:
                    print "\r\n["+value[key].decode('utf-8').encode(type)+"]"
                except:
                    print "\r\n[Title Code Error]"
            try:
                print "[%s] %s - %s - %s - %s\r\n" % (value['status'],value['target'],value['head_allow'],value['title'].decode('utf-8').encode(type),','.join(value['search'])),
            except :
                print "[%s] %s - %s  - %s - %s\r\n" % (value['status'],value['target'],value['head_allow'],"[Title Code Error]",','.join(value['search'])),
            temp = value[key]
    print "[.] End output!"
    print "======================================================="

def argSet(parser):
    parser.add_argument("-K", "--key", type=str, help="The order key e.g. title、status、host", default="id")
    parser.add_argument("-T", "--timeout", type=str, help="Timeout", default="3")
    parser.add_argument("-F", "--file",type=str, help="Load ip dictionary e.g. 192.168.1.2:8080", default=None)
    parser.add_argument("-V", "--verbose",action='store_true',help="verbose", default=False)
    parser.add_argument("-O", "--out",type=str, help="output file e.g res.txt", default=None)
    parser.add_argument("-S", "--search",type=str, help="search key in title or content,e.g. 管理,后台", default=None)
    parser.add_argument("-N", "--threadnum",type=int, help="Thread Num e.g. 10", default=10)
    return parser


def handle(args):
    key = args.key
    timeout = args.timeout
    filename = args.file
    out = args.out
    threadnum = args.threadnum
    verbose = args.verbose
    search = args.search
    searchList = []
    if search!=None:
        searchList=search.split(',')
    if key not in ['title','status','host','head_allow','id','search']:
        key = 'id'
    if filename != None:
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                for line in f.readlines():
                    myline = line.strip('\n').strip('\r')
                    targetList.append(myline)
        else:
            print "[-] The path is not exist!"
    scan(threadnum,timeout,verbose,searchList)
    printlog(key,out)

if __name__=='__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser = argSet(parser)
    args = parser.parse_args()
    handle(args)




