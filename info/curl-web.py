#!/usr/bin/env python
# -*- coding:utf-8 -*- 
__author__ = 'orleven'
import threading
import requests
import argparse
import os
import sys
import platform
from bs4 import BeautifulSoup
import chardet
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
type=sys.getfilesystemencoding()
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
        www.baidu.com
        192.168.1.11
        192.168.1.22:80
        192.168.1.22:80/admin

'''
#sysstr = platform.system() 
targetList = [

"134.96.253.30:2379",
"134.96.253.30:2380",
"134.96.253.30:6443",
"134.96.253.30:10250",
"134.96.253.30:10255",
"134.96.253.30:10256",
"134.96.253.30:30001",
"134.96.253.30:30002",
"134.96.253.30:30007",
"134.96.253.30:30101",
"134.96.253.30:30102",
"134.96.253.30:30105",
"134.96.253.30:30106",
"134.96.253.30:30201",
"134.96.253.30:30202",
"134.96.253.30:30301",
"134.96.253.30:30302",
"134.96.253.30:30309",
"134.96.253.30:30370",
"134.96.253.30:30501",
"134.96.253.30:30801",
"134.96.253.30:30803",
"134.96.253.30:30805",
"134.96.253.31:2379",
"134.96.253.31:2380",
"134.96.253.31:6443",
"134.96.253.31:10250",
"134.96.253.31:10255",
"134.96.253.31:10256",
"134.96.253.31:30001",
"134.96.253.31:30002",
"134.96.253.31:30007",
"134.96.253.31:30101",
"134.96.253.31:30102",
"134.96.253.31:30105",
"134.96.253.31:30106",
"134.96.253.31:30201",
"134.96.253.31:30202",
"134.96.253.31:30301",
"134.96.253.31:30302",
"134.96.253.31:30309",
"134.96.253.31:30370",
"134.96.253.31:30501",
"134.96.253.31:30801",
"134.96.253.31:30803",
"134.96.253.31:30805",
"134.96.253.32:2379",
"134.96.253.32:2380",
"134.96.253.32:6443",
"134.96.253.32:10250",
"134.96.253.32:10255",
"134.96.253.32:10256",
"134.96.253.32:30001",
"134.96.253.32:30002",
"134.96.253.32:30007",
"134.96.253.32:30101",
"134.96.253.32:30102",
"134.96.253.32:30105",
"134.96.253.32:30106",
"134.96.253.32:30201",
"134.96.253.32:30202",
"134.96.253.32:30301",
"134.96.253.32:30302",
"134.96.253.32:30309",
"134.96.253.32:30370",
"134.96.253.32:30501",
"134.96.253.32:30801",
"134.96.253.32:30803",
"134.96.253.32:30805",
"134.96.252.82:15005",
"134.96.252.84:2181",
"134.96.252.84:3888",
"134.96.252.84:6380",
"134.96.252.84:9300",
"134.96.252.84:10004",
"134.96.252.84:37225",
"134.96.252.84:40000",
"134.96.252.84:40001",
"134.96.252.84:56386",
"134.96.252.84:56388",
"134.96.252.85:80",
"134.96.252.85:88",
"134.96.252.85:464",
"134.96.252.85:749",
"134.96.252.85:3000",
"134.96.252.85:4245",
"134.96.252.85:6188",
"134.96.252.85:7337",
"134.96.252.85:7447",
"134.96.252.85:8019",
"134.96.252.85:8020",
"134.96.252.85:8033",
"134.96.252.85:8040",
"134.96.252.85:8042",
"134.96.252.85:8080",
"134.96.252.85:8088",
"134.96.252.85:8440",
"134.96.252.85:8441",
"134.96.252.85:8670",
"134.96.252.85:9000",
"134.96.252.85:9440",
"134.96.252.85:9441",
"134.96.252.85:10000",
"134.96.252.85:13562",
"134.96.252.85:20002",
"134.96.252.85:33939",
"134.96.252.85:35922",
"134.96.252.85:37856",
"134.96.252.85:38358",
"134.96.252.85:40000",
"134.96.252.85:40001",
"134.96.252.85:45454",
"134.96.252.85:50070",
"134.96.252.85:50111",
"134.96.252.85:56386",
"134.96.252.85:56388",
"134.96.252.85:60020",
"134.96.252.85:60200",
"134.96.252.85:61181",
"134.96.252.85:61310",
"134.96.252.86:88",
"134.96.252.86:754",
"134.96.252.86:1019",
"134.96.252.86:1022",
"134.96.252.86:3480",
"134.96.252.86:3481",
"134.96.252.86:8010",
"134.96.252.86:8480",
"134.96.252.86:8485",
"134.96.252.86:8670",
"134.96.252.86:9000",
"134.96.252.86:9001",
"134.96.252.86:16020",
"134.96.252.86:16030",
"134.96.252.86:20000",
"134.96.252.86:20001",
"134.96.252.87:1019",
"134.96.252.87:1022",
"134.96.252.87:2181",
"134.96.252.87:3480",
"134.96.252.87:3888",
"134.96.252.87:8010",
"134.96.252.87:8019",
"134.96.252.87:8020",
"134.96.252.87:8188",
"134.96.252.87:8670",
"134.96.252.87:9000",
"134.96.252.87:9001",
"134.96.252.87:9083",
"134.96.252.87:10200",
"134.96.252.87:16020",
"134.96.252.87:16030",
"134.96.252.87:20000",
"134.96.252.87:41796",
"134.96.252.87:50070",
"134.96.252.87:50090",
"134.96.252.88:8670",
"134.96.252.88:9200",
"134.96.252.88:9300",
"134.96.252.89:8670",
"134.96.252.89:9000",
"134.96.252.89:9200",
"134.96.252.89:9300",
"134.96.252.90:9200",
"134.96.252.90:9300",
"134.96.252.91:9639",
"134.96.252.91:10909",
"134.96.252.91:10911",
"134.96.252.91:10912",
"134.96.252.91:11911",
"134.96.252.91:15005",
"134.96.252.92:10909",
"134.96.252.92:10911",
"134.96.252.92:10912",
"134.96.252.92:11911",
"134.96.252.92:15005",
"134.96.252.93:80",
"134.96.252.93:2188",
"134.96.252.93:6066",
"134.96.252.93:8000",
"134.96.252.93:8086",
"134.96.252.93:8807",
"134.96.252.93:9014",
"134.96.252.93:9017",
"134.96.252.93:13189",
"134.96.252.93:53096",
"134.96.252.94:3690",
"134.96.252.94:6786",
"134.96.252.94:8009",
"134.96.252.94:8080",
"134.96.252.94:9876",
"134.96.252.95:2182",
"134.96.252.95:2183",
"134.96.252.95:3307",
"134.96.252.95:6786",
"134.96.252.95:8196",
"134.96.252.95:9876",
"134.96.252.95:13182",
"134.96.252.95:13183",
"134.96.252.95:37200",
"134.96.252.95:37744",
"134.96.252.96:2182",
"134.96.252.96:2183",
"134.96.252.96:6379",
"134.96.252.96:8001",
"134.96.252.96:8009",
"134.96.252.96:8080",
"134.96.252.96:8980",
"134.96.252.96:8981",
"134.96.252.96:8982",
"134.96.252.96:8983",
"134.96.252.96:8990",
"134.96.252.96:8991",
"134.96.252.96:8992",
"134.96.252.96:8993",
"134.96.252.96:8994",
"134.96.252.96:9200",
"134.96.252.96:12182",
"134.96.252.96:13182",
"134.96.252.96:13183",
"134.96.252.96:34421",
"134.96.252.96:42669",
"134.96.252.97:2182",
"134.96.252.97:2183",
"134.96.252.97:8807",
"134.96.252.97:8972",
"134.96.252.97:9014",
"134.96.252.97:9017",
"134.96.252.97:12183",
"134.96.252.97:13182",
"134.96.252.97:13183",
"134.96.252.97:37219",
"134.96.252.97:50992",
"134.96.252.102:111",
"134.96.252.102:2182",
"134.96.252.102:2183",
"134.96.252.102:3307",
"134.96.252.102:3502",
"134.96.252.102:8001",
"134.96.252.102:8080",
"134.96.252.102:8090",
"134.96.252.102:8196",
"134.96.252.102:8719",
"134.96.252.102:8720",
"134.96.252.102:8721",
"134.96.252.102:8866",
"134.96.252.102:13182",
"134.96.252.102:13183",
"134.96.252.102:36689",
"134.96.252.102:54497",
"134.96.252.102:56386",
"134.96.252.102:56388",
"134.96.252.103:3307",
"134.96.252.103:8280",
"134.96.252.103:8866",
"134.96.252.104:3307",
"134.96.252.104:8866",
"134.96.252.104:9005",
"134.96.252.104:9006",
"134.96.252.104:10000",
"134.96.252.104:10001",
"134.96.252.105:3307",
"134.96.252.105:9005",
"134.96.252.105:9006",
"134.96.252.105:10000",
"134.96.252.105:10001",
"134.96.252.106:8080",
"134.96.252.106:8090",
"134.96.252.106:56386",
"134.96.252.106:56388",
"134.96.252.107:2181",
"134.96.252.107:2888",
"134.96.252.107:3888",
"134.96.252.107:8030",
"134.96.252.107:8031",
"134.96.252.107:8032",
"134.96.252.107:8033",
"134.96.252.107:8088",
"134.96.252.107:8480",
"134.96.252.107:8485",
"134.96.252.107:8670",
"134.96.252.107:16000",
"134.96.252.107:16010",
"134.96.252.107:51510",
"134.96.252.108:2181",
"134.96.252.108:3888",
"134.96.252.108:8480",
"134.96.252.108:8485",
"134.96.252.108:8670",
"134.96.252.108:10020",
"134.96.252.108:10033",
"134.96.252.108:16000",
"134.96.252.108:16010",
"134.96.252.108:19888",
"134.96.252.108:60736",
"134.96.253.12:3307",
"134.96.253.12:6379",
"134.96.253.12:8001",
"134.96.253.12:8196",
"134.96.253.12:8972",
"134.96.253.12:8980",
"134.96.253.12:8981",
"134.96.253.12:8982",
"134.96.253.12:8983",
"134.96.253.12:8990",
"134.96.253.12:8991",
"134.96.253.12:8992",
"134.96.253.12:8993",
"134.96.253.12:8994",
"134.96.252.93:80",
"134.96.252.93:2188",
"134.96.252.93:6066",
"134.96.252.93:8000",
"134.96.252.93:8086",
"134.96.252.93:8807",
"134.96.252.93:9014",
"134.96.252.93:9017",
"134.96.252.93:13189",
"134.96.252.93:53096",]
resultDic = {}
threadList = []
resultList = []

def _curl(protocol,target,i,timeout=3,searchList=[]):
    dic = {}
    dic['id'] = str(i) 
    dic['host'] = target.split(':')[0]
    dic['search'] = []
    url = protocol + "://" +target.strip(' ')
    try:
        result = requests.get(url, timeout=int(timeout),verify=False)
        soup = BeautifulSoup(result.text)
        dic['target'] = url
        dic['status'] = str(result.status_code)
        dic['flag'] = True
        dic['host'] = target
        mytitle =  soup.title.string
        content =  result.text
        #print content.encode(result.encoding).decode('utf-8').encode(type)
        #print mytitle.encode(result.encoding).decode('utf-8').encode(type)
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
    url = protocol + "://" +target.strip(' ')
    try:
        result1 = requests.options(url+"/testbyah", timeout=int(timeout))
        dic['head_allow'] = result1.headers['Allow']
    except:
        dic['head_allow'] = "Not Allow"
    return dic

def curl(threadId,timeout,threadNum,verbose,searchList):
    for i in xrange(threadId,len(targetList),threadNum):
        dic = _curl('http',targetList[i],i,timeout,searchList)
        if not dic['flag'] :
            dic = _curl('https',targetList[i],i,timeout,searchList)
        resultList.append(dic)
        #if verbose and  dic['status'] !="0" :
        if True:
            if chardet.detect(dic['title'])['encoding'].lower()=='utf-8':    
                title = dic['title'].decode('utf-8').encode(type)
            else:
                title =  dic['title']
            try:
                print "[%s] %s - %s - %s - %s\r\n" % (dic['id'],dic['target'],dic['status'],title,','.join(dic['search'])),
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
                if chardet.detect(value['title'])['encoding'].lower()=='utf-8':    
                    title = value['title'].decode('utf-8').encode(type)
                else:
                    title =  value['title']
                if temp != value[key] and key != 'id' :
                    try:
                        f.write("\r\n["+title+"]\r\n")
                    except:
                        f.write("\r\n[Title Code Error]\r\n")
                try:
                    f.write("[%s] [%s] %s - %s - %s - %s\r\n" % (value['id'],value['status'],value['target'],value['head_allow'],title,','.join(value['search'])))
                except:                
                    f.write("[%s] [%s] %s - %s - %s - %s\r\n" % (value['id'],value['status'],value['target'],value['head_allow'],"[Title Code Error]",','.join(value['search'])))
                temp = value[key]
        print "[.] Save result into "+ out + "!"
    else:
        for value in resList:
            if chardet.detect(value['title'])['encoding'].lower()=='utf-8':    
                title = value['title'].decode('utf-8').encode(type)
            else:
                title =  value['title']
            if temp != value[key] and key != 'id' :
                try:
                    print "\r\n["+title+"]"
                except:
                    print "\r\n[Title Code Error]"
            try:
                print "[%s] [%s] %s - %s - %s - %s\r\n" % (value['id'],value['status'],value['target'],value['head_allow'],title,','.join(value['search'])),
            except :
                print "[%s] [%s] %s - %s  - %s - %s\r\n" % (value['id'],value['status'],value['target'],value['head_allow'],"[Title Code Error]",','.join(value['search'])),
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





