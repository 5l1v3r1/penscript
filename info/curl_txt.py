#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'
import threading
import requests
import argparse
import sys 
import os
import platform
import chardet
import Queue
import urllib
import time
#from openpyxl import Workbook
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
type=sys.getfilesystemencoding()
reload(sys)  
sys.setdefaultencoding('utf8')   
'''
    批量检测目标是否属于Web应用，并检测关键词，以及得到http请求方法
    Usage:
        python curl.py -T 3 -F file.txt
        python curl.py  -F file.txt
        python curl.py -F file.txt -V
        python curl.py -F file.txt -S admin,管理,后台 -N 100 -V 
    目标格式:
        http://www.baidu.com
        http://192.168.1.11
        http://192.168.1.22:80
        www.baidu.com
        127.0.0.1
'''

# targetList = []
# resultDic = {}
thread_list = []
search_list=[]
is_continue = True
resultList = {}
table_title_list = []
queue = Queue.Queue()
thread_count = 0 
file_lock = threading.Lock()
load_lock = threading.Lock()
codes = ['utf-8','gbk']
#book = Workbook()
#ws = book.active
#x = 1
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}
def curl_head(target,headers,timeout=3):
    try:
        requests.head(target, headers=headers, verify=False, timeout=timeout)
        return target
    except KeyboardInterrupt:
        is_continue = Flse
    except:
        pass
    return None

def get_base_url(url):
    protocol, s1 = urllib.splittype(url)
    host, s2 = urllib.splithost(s1)
    host, port = urllib.splitport(host)
    port = port if port != None else 443 if protocol == 'https' else 80
    base_url = protocol + "://" + host +":"+str(port)
    return base_url,host,port

'''
def to_excal(line):
    global x
    x = x + 1
    for key in line:
        if key not in table_title_list:
            table_title_list.append(key)
            ws.cell(row=1, column=len(table_title_list)).value = key
        try:
            # print line[key]
            if isinstance(line[key], int) or isinstance(line[key], str):
                ws.cell(row=x, column=table_title_list.index(key) + 1).value = line[key]
            elif isinstance(line[key], list):
                _ = ','.join(line[key])
                ws.cell(row=x, column=table_title_list.index(key) + 1).value = _.decode(type)
            elif isinstance(line[key], dict):
                ws.cell(row=x, column=table_title_list.index(key) + 1).value = str(line[key])
            else:
                ws.cell(row=x, column=table_title_list.index(key) + 1).value = line[key]
        except:
            print 'error code'
            ws.cell(row=x, column=table_title_list.index(key) + 1).value = "[Some error]"
'''
def curl(out,search_list,timeout=3):
    global is_continue
    while is_continue:
        load_lock.acquire()
        if  not is_continue or queue.qsize() < 1:
            load_lock.release()
            break
        i, target = queue.get()
        load_lock.release()
        dic = {}
        dic['id'] = str(i)
        dic['search'] = []
        dic['title'] = "[Curl Failed]"
        dic['status'] = "0"
        
        dic['flag'] = False
        dic['host'] = target.strip().split(':')[0].strip('https://').strip('http://')
        dic['target'] = target.strip()

        if  not is_continue:
            break
        if target.startswith('http://') or target.startswith('https://'):
            base_url,host,port = get_base_url(target)
            dic['host'] = host
            dic['port'] = port
            resultList[int(i)] = dic
        else:
            for pro in ['http://', "https://"]:
                url = curl_head(pro + target , headers)
                if url:
                    base_url,host,port = get_base_url(url)
                    dic['target'] = url
                    dic['host'] = host
                    dic['port'] = port
                    resultList[int(i)] = dic
                    break
                else:
                    port = 0
                    dic['port'] = port
                    resultList[int(i)] = dic
                    continue

        if  not is_continue:
            break
        try:
            title = None
            result = None
            result = requests.get(dic['target'], timeout=int(timeout),verify=False)
            content =  result.text
            dic['flag'] = True
            dic['status'] = str(result.status_code)
            soup = BeautifulSoup(result.text, "html5lib")
            title =  soup.title.string
            
            #print (result.encoding)
            title =  title.encode(result.encoding)
        except:
            #title = None
            content = None
            content = content.encode(result.encoding) if content !=None else ''.encode('utf-8')
        finally:
            if dic['status'] == 0:
                title = "[Curl Failed]".encode('utf-8')
            elif title == None or title =='':
                title = "[None Title]".encode('utf-8')

        if result and result.encoding!=None and result.encoding!='':
            codes.append(result.encoding)
        
        for j in range(0,len(codes)):
            try:
                dic['title'] = title.decode(codes[j]).strip().replace("\r", "").replace("\n", "")
                break
            except: 
                pass
            finally:
                if j+1 == len(codes):
                    content = ''
                    dic['title'] = '[Error Code]'

                    
        for searchkey in search_list:            
            try:
                if searchkey.decode(type) in dic['title'] or searchkey in content.encode(result.encoding):
                    dic['search'].append(searchkey)   
            except:
                pass
    

        # option 
        #try:
        #    result = requests.options(base_url+"/testbyah", timeout=int(timeout))
        #    dic['head_allow'] = result.headers['Allow']
        #except:
        #    dic['head_allow'] = "[Not Allow]"
        if is_continue:
            _search = ','.join(dic['search']).decode(type)
            file_lock.acquire()
            try:
            
                if len(search_list)>0:
                    pass
                    print "[%s]\t[%s]\t%s\t%s\t%s" %(str(i),dic['status'],dic['target'],dic['title'],_search)
                else:
                    pass
                    print "[%s]\t[%s]\t%s\t%s" %(str(i),dic['status'],dic['target'],dic['title'])
        #    if out:
        #        to_excal(dic)
            except Exception:
                pass
            file_lock.release()
            resultList[int(i)] = dic

    global thread_count 
    thread_count -= 1
    
    
    

def scan(thread_num,timeout,search_list,out):
    global thread_count
    global is_continue
    print "[.] Run start: Total " + str(queue.qsize()) + " request!"
    for threadId in xrange(0,thread_num):
        t = threading.Thread(target=curl,args=(out,search_list,timeout,))
        t.start()
        thread_count += 1
    while True:
        try:
            time.sleep(0.01)
        except:
            is_continue = False
            continue
        if thread_count <= 0 or not is_continue :
            print "\r\n[.] Save file..."
            #book.save(out)
            save(out)
            print "\r\n[.] Run over!"
            break
    
        
            
            
    #for num in xrange(0,thread_num):
    #    thread_list[num].join()
    
def save(out):
    if out:

        sorted(resultList.keys())
        with open(out,'w+') as f:
            for i in resultList.keys():
                dic = resultList[i]
                #f.write("[%s]\t[%s]\t%s\t%s\r\n" %(str(i),dic['status'],dic['target'],dic['title']))
                try:
                    if len(search_list)>0:
                        pass
                        #f.write("[%s]\t[%s]\t%s\t%s\t%s\r\n" %(str(i),dic['status'],dic['target'],dic['title'],_search))
                    else:
                        pass
                        f.write("[%s]\t[%s]\t%s\t%s\r\n" %(str(i),dic['status'],dic['target'],dic['title']))
                except Exception:
                    print Exception
                    pass
        

def argSet(parser):
    # parser.add_argument("-K", "--key", type=str, help="The order key e.g. title、status、host", default="id")
    parser.add_argument("-T", "--timeout", type=str, help="Timeout", default="3")
    parser.add_argument("-F", "--file",type=str, help="Load ip dictionary e.g. 192.168.1.2:8080", default=None)
    # parser.add_argument("-V", "--verbose",action='store_true',help="verbose", default=False)
    parser.add_argument("-O", "--out",type=str, help="output file e.g res.txt", default="res.txt")
    parser.add_argument("-S", "--search",type=str, help="search key in title or content,e.g. 管理,后台", default=None)
    parser.add_argument("-N", "--threadnum",type=int, help="Thread Num e.g. 10", default=10)
    return parser
    
def handle(args):
    timeout = args.timeout
    filename = args.file
    out = args.out
    threadnum = args.threadnum
    search = args.search
    search_list = []
    
    if search!=None:
        search_list=search.split(',')
    z = 1
    #global queue
    if filename != None:
        if os.path.isfile(filename):
            with open(filename, 'rb') as f:
                for line in f.readlines():
                    myline = line.strip('\n').strip('\r')
                    queue.put([z,myline])
                    z += 1
            scan(threadnum,timeout,search_list,out)
        else:
            print "[-] The path is not exist!"
    

if __name__=='__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser = argSet(parser)
    args = parser.parse_args()
    handle(args)
