# -*- coding: UTF-8 -*-
__author__ = 'orleven'

'''
   其他端口的未授权访问漏洞扫描，例如dubbo等，其他功能遇到在添加
'''

import socket
import argparse
import re
import threading
import sys

threadList = []
resultList = []
targetList = [

]
vulList = [
   {
      "vul":"Test",
      "key":"just for test!\r\n\r\n",
      "flag":"just for test!",
   },
   {
      "vul":"Dubbo access vul",
      "key":"ls\r\n\r\n",
      "flag":"com.alibaba.dubbo",
   }
]

def socketscan(target,i,timeout=5):
    dic = {}
    address = target.split(':')
    dic['id'] = str(i) 
    dic['host'] = host = address[0]
    dic['port'] = port = address[1]
    dic['vul'] = "Unknown"
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(int(timeout))
    try:
       s.connect((host,int(port)))
    except socket.timeout:
       pass
    except Exception as err:
       pass
    message = ""
    for vul in vulList:
       try:
           s.sendall(vul['key'])
           message = s.recv(1024)
           dic['message'] = message[0:100] + '\r\n'
           if vul['flag'] in message:
              dic['vul'] = vul['vul']
              return dic
       except socket.timeout:
           pass
       except Exception as err:
           pass
    return dic

def _scan(threadId,timeout,threadNum):
    for i in xrange(threadId,len(targetList),threadNum):
        dic = socketscan(targetList[i],i,timeout)
        resultList.append(dic)

def scan(threadNum,timeout):
    
    print "[.] Run start: Total " + str(len(targetList)) + " request!"
    for threadId in xrange(0,threadNum):
        t = threading.Thread(target=_scan,args=(threadId,timeout,threadNum,))
        t.start()
        threadList.append(t)
    for num in xrange(0,threadNum):
        threadList[num].join()
    print "[.] Run over !"

def printlog(key,out,verbose):
    print "[.] Start to output!"
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
                if verbose:
                   f.write(value['host']+ ":" + value['port']+'   -   ' +value['message'] + '\r\n')
                else:
                   f.write(value['host']+ ":" + value['port']+'\r\n')
                temp = value[key]
        print "[.] Save result into "+ out
    else:
        for value in resList:
            if temp != value[key] and key != 'id' :
                try:
                    print "\r\n["+value[key]+"]"
                except:
                    print "\r\n[GBK Code Error]"
            if verbose:
               print value['host'] + ":" + value['port'] +'   -   ' +value['message']
            else:
               print value['host'] + ":" + value['port']  
            temp = value[key]
    print "\r\n[.] End output!"

def argSet(parser):
    parser.add_argument("-T", "--timeout", type=str, help="Timeout", default="5")
    parser.add_argument("-V", "--verbose",action='store_true',help="verbose", default=False)
    parser.add_argument("-K", "--key", type=str, help="The order key e.g. vul、id、host", default="title")
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
    verbose = args.verbose
    if key not in ['vul','id','host']:
        key = 'vul'
    if filename != None:
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                for line in f.readlines():
                    myline = line.strip('\r').strip('\n')
                    targetList.append(myline)
        else:
            print "The path is not exist!"
    scan(threadnum,timeout)
    printlog(key,out,verbose)

if __name__=='__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser = argSet(parser)
    args = parser.parse_args()
    handle(args)

