#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'
import threading
import requests
import argparse
import os
import random
import re
from bs4 import BeautifulSoup

'''
    批量ip反查域名，域名查询备案信息
    ip 反查调用接口：aizhan、chinaz、114best
    域名ICP调用接口：aizhan、beianbeian、sobeian
'''

targetList = [
"111.198.162.44",
]

resultDic = {}
threadList = []
resultList = []

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }

def initdic(target,i):
    dic = {}
    dic['id'] = i
    dic['ip'] = target
    dic['chinaz'] = False
    dic['114best'] = False
    dic['aizhan'] = False
    dic['host'] = target
    dic['flag'] = False
    dic['domain'] = []
    dic['ICP']= []
    temptext =  re.search(r'(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|[0-9])(?:\.(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|[0-9])){3}',target)
    if temptext == None:
        dic['domain'].append(target)
        dic['flag'] = True
    return dic

def byaizhan(target,dic,timeout=3):
    for j in range(3):
        try:
            url = "https://dns.aizhan.com/" + target.strip(' ')+"/"
            result = requests.get(url, headers = headers, timeout=int(timeout))
            soup = BeautifulSoup(result.text)
            alist = soup.find_all("td", class_="domain")
            for i in xrange(1,len(alist)) :
                mydomain = alist[i].find("a").get_text()
                if mydomain not in dic['domain']:
                    dic['domain'].append(mydomain)     
            dic['aizhan'] = True
            dic['flag'] = True
            return dic
        except:
            pass
    print "[-] Error for (%s)%s by aizhan\r\n" %(dic['id'],target),
    return dic

def bychinaz(target,dic,timeout=3):
    for j in range(3):
        try:
            url = "http://s.tool.chinaz.com/same?s=" + target.strip(' ')
            result = requests.get(url, headers = headers, timeout=int(timeout))
            soup = BeautifulSoup(result.text)
            ul =  soup.find(id="ResultListWrap")
            for div in  soup.find_all("div", class_="w30-0 overhid"):
                mydomain = div.find("a").get_text()
                if mydomain not in dic['domain']:
                    dic['domain'].append(mydomain)
            dic['chinaz'] = True
            dic['flag'] = True
            return dic
        except:
            pass
    print "[-] Error for (%s)%s by chinaz\r\n" %(dic['id'],target),
    return dic

def by114best(target,dic,timeout=3):
    for j in range(3):
        try:
            url = "http://www.114best.com/ip/114.aspx?w=" + target.strip(' ')
            headers['X-Forwarded-For'] =  '.'.join([str(random.randint(0,255)),str(random.randint(0,255)),str(random.randint(0,255)),str(random.randint(0,255))])
            result = requests.get(url, headers = headers, timeout=int(timeout))
            soup = BeautifulSoup(result.text)
            div =  soup.find(id="rl")
            for span in div.find_all('span'):
                mydomain = span.get_text().replace(" ","").replace("\r","").replace("\n","")
                if mydomain not in dic['domain']:
                    dic['domain'].append(mydomain)
            dic['114best'] = True
            dic['flag'] = True
            return dic
        except:
            pass
    print "[-] Error for (%s)%s by 114best\r\n" %(dic['id'],target),
    return dic

def ICPsobeian(domain,dic,timeout=3):
    for j in range(3):
        flag = False
        try:
            ICPinfo = domain
            ICPTime = "None"
            # print domain
            url = "http://www.sobeian.com/search?key=" + domain.strip(' ')+"/"
            result = requests.get(url, headers = headers, timeout=int(timeout))
            soup = BeautifulSoup(result.text)
            for span in  soup.find_all("span", class_="list-group-item clearfix"):
                alist = span.find_all('a',href = re.compile('/icp/details/'))
                if domain in alist[2].get_text().split(' '):
                    ICPinfo += ":"+alist[1].get_text()
                    temp = re.search(r'\d{4}\-\d{2}\-\d{2}',span.get_text())
                    if temp !=None :
                        ICPTime = temp.group()
                    ICPinfo +=":"+ ICPTime
                    dic['ICP'].append(ICPinfo)
                    flag = True
                    break
            dic['flag'] = True
            return dic,flag
        except:
            pass
    print "[-] Error for ICP(%s)%s by sobeian\r\n" %(dic['id'],domain),
    return dic,flag


def ICPbyaizhan(domain,dic,timeout=3):
    for j in range(3):
        flag = False
        try:
            url = "https://icp.aizhan.com/" + domain.strip(' ')+"/"
            result = requests.get(url, headers = headers, timeout=int(timeout))
            soup = BeautifulSoup(result.text)
            div =  soup.find(id="icp-table")
            ICPinfo = domain
            if div !=None:
                for span in div.find_all('span'):
                    info = span.get_text()
                    if info !=None:
                        ICPinfo += ":"+info
            if ICPinfo !=domain and ICPinfo not in dic['ICP']:
                dic['ICP'].append(ICPinfo)
                flag = True
            dic['flag'] = True
            return dic,flag
        except:
            pass
    print "[-] Error for ICP(%s)%s by aizhan\r\n" %(dic['id'],domain),
    return dic,flag

def ICPbybeianbeian(domain,dic,timeout=3):
    for j in range(3):
        flag = False
        try:
            url = "http://www.beianbeian.com/search/" + domain.strip(' ')
            result = requests.get(url, headers = headers, timeout=int(timeout))
            soup = BeautifulSoup(result.text)
            info1 = info2 = None
            alist = soup.find_all('a',href = re.compile('/beianxinxi/'))
            if len(alist)>0:
                info1 = alist[0].get_text()
                div =  soup.find(id="pass_time")
                info2 = div.get_text()
            ICPinfo = domain
            if info1 !=None and info2!=None:
                ICPinfo += ":"+info1+":"+info2
            if ICPinfo != domain and ICPinfo not in dic['ICP']:
                dic['ICP'].append(ICPinfo)
                flag = True
            dic['flag'] = True
            return dic,flag
        except:
            pass
    print "[-] Error for ICP(%s)%s by beianbeian\r\n" %(dic['id'],domain),
    return dic,flag

def _curl(target,i,timeout=3,mode="DI"):
    dic = initdic(target,i)
    if "D" in mode and dic['flag'] :
        dic = byaizhan(target,dic,timeout)
        dic = bychinaz(target,dic,timeout)
        dic = by114best(target,dic,timeout)
        if not dic['flag']:
            dic['domain'] = "Curl Failed"
    else:
        dic['domain'].append(target)
    if "I" in mode and len(dic['domain'])>0:
        for domain in dic['domain']:
            flag = False
            
            dic,myflag = ICPsobeian(domain,dic,timeout)
            flag |= myflag
            
            if not myflag :
                dic,myflag = ICPbyaizhan(domain,dic,timeout)
                flag |= myflag
            
            if not myflag :
                dic,myflag = ICPbybeianbeian(domain,dic,timeout)
                flag |= myflag
                
            if not flag:
                dic['ICP'].append(domain)
    return dic


def curl(threadId,timeout,threadNum,verbose,mode):
    for i in xrange(threadId,len(targetList),threadNum):
        dic = _curl(targetList[i],i,timeout,mode)
        resultList.append(dic)
        if verbose and  dic['flag'] :
            #print "[%s] %s - %s - %s \r\n" % (dic['id'],dic['ip'],dic['domain'],dic['ICP']),
            if "I" in mode:
                print "[%s] %5s - %s - " % (dic['id'],dic['flag'],dic['ip']),
                for myICP in dic['ICP']:
                    print "|"+myICP,
                print ""
            else:
                print "[%s] %5s - %s - %s" % (dic['id'],dic['flag'],dic['ip'],dic['domain'])

def scan(threadNum,timeout,verbose,mode):
    print "======================================================="
    print "[.] Start scan domain by ip: Total " + str(len(targetList)) + " ip!"
    for threadId in xrange(0,threadNum):
        t = threading.Thread(target=curl,args=(threadId,timeout,threadNum,verbose,mode,))
        t.start()
        threadList.append(t)
    for num in xrange(0,threadNum):
        threadList[num].join()
    print "\r\n[.] Run over domain by ip!"
    
    print "======================================================="
    print "[.] Sort list..."
    resList =  sorted(resultList,key = lambda e:e.__getitem__("id"))
    return resList

def printlog(resList,out,mode):
    print "======================================================="
    print "... These Info just for reference ..."
    print "[.] Start to output!"
    if out!=None:
        with open(out,'wb') as f :
            for value in resList:
                try:
                    if "I" in mode:
                        f.write("[%s] %5s - %s - " % (value['id'],value['flag'],value['ip']))
                        for myICP in value['ICP']:
                            f.write("|"+myICP)
                        f.write("\r\n")
                    else:
                        f.write("[%s] %5s - %s - %s - %s\r\n" % (value['id'],value['flag'],value['ip'],value['domain'],value['ICP']))
                except:
                    if "I" in mode:
                        f.write("[%s] %5s - %s - " % (value['id'],value['flag'],value['ip']))
                        for myICP in value['ICP']:
                            f.write("|"+myICP)
                        f.write("\r\n")
                    else:
                        f.write("[%s] %5s - %s - %s - %s\r\n" % (value['id'],value['flag'],value['ip'],value['domain'],value['ICP']))                
        print "[.] Save result into "+ out + "!"
    else:
        for value in resList:
            try:
                if "I" in mode:
                    print "[%s] %5s - %s - " % (value['id'],value['flag'],value['ip']),
                    for myICP in value['ICP']:
                        print "|"+myICP,
                    print ""
                else:
                    print "[%s] %5s - %s - %s" % (value['id'],value['flag'],value['ip'],value['domain'])
            except :
                if "I" in mode:
                    print "[%s] %5s - %s - " % (value['id'],value['flag'],value['ip']),
                    for myICP in value['ICP']:
                        print "|"+myICP,
                    print ""
                else:
                    print "[%s] %5s - %s - %s" % (value['id'],value['flag'],value['ip'],value['domain'])
    print "[.] End output!"
    print "======================================================="

def argSet(parser):
    parser.add_argument("-T", "--timeout", type=str, help="Timeout", default="10")
    parser.add_argument("-F", "--file",type=str, help="Load ip dictionary e.g. 192.168.1.2", default=None)
    parser.add_argument("-V", "--verbose",action='store_true',help="verbose", default=True)
    parser.add_argument("-O", "--out",type=str, help="output file e.g res.txt", default=None)
    parser.add_argument("-N", "--threadnum",type=int, help="Thread Num e.g. 2", default=2)
    parser.add_argument("-M", "--mode",type=str,help="mode e.g. DI/D/I", default="DI")
    #parser.add_argument("-M", "--mode",action='store_true',help="mode e.g. DI/D/I", default="DI")
    return parser


def handle(args):
    timeout = args.timeout
    filename = args.file
    out = args.out
    threadnum = args.threadnum
    verbose = args.verbose
    mode = args.mode
    if filename != None:
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                for line in f.readlines():
                    myline = line.strip('\n').strip('\r')
                    targetList.append(myline)
        else:
            print "[-] The path is not exist!"
    resList = scan(threadnum,timeout,verbose,mode)
    printlog(resList,out,mode)

if __name__=='__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser = argSet(parser)
    args = parser.parse_args()
    handle(args)


