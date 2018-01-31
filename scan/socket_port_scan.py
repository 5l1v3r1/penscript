# -*- coding: UTF-8 -*-
__author__ = 'orleven'

import socket
import argparse
import re
import threading
import sys

threadList = []

# banList 
banList=['proxy,welcome to my world!']
def anlyze_host(target_host):
    try:
        pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}') 
        match = pattern.match(target_host)
        if match:
            return match.group()
        else:
            try:
                target_host = socket.gethostbyname(target_host) 
                return target_host
            except Exception as err:
                print '[-] Address error: ',err,'\r\n',
                exit(0)
    except Exception as err:
        print '[-] Error-1: ',sys.exc_info()[0],err,'\r\n',
        exit(0)
                    

def anlyze_port(target_port):

    try:
        pattern = re.compile(r'(\d+)-(\d+)')   
        match = pattern.match(target_port)
        if match:
            start_port = int(match.group(1))
            end_port = int(match.group(2))
            return [x for x in range(start_port,end_port + 1)]
        else:
            return [int(x) for x in target_port.split(',')]
    except Exception as err:
        print '[-] Error-2: ',sys.exc_info()[0],err ,'\r\n',
        exit(0)

def _scanner(target_host,target_port):

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect((target_host,target_port))
        s.sendall(b'GET / HTTP/1.1\r\n\r\n')
        message = s.recv(100)
        global banList 
        if message and message not in banList:
            print '[+] %s:%s open\r\n'% (target_host,target_port),
            # print '%s\r\n' % message.decode('utf-8'),
        # print('[+]%s:%s open\r\n' % (target_host,target_port)) 
           
    except socket.timeout:
        pass
        # print '[-] %s:%s close\r\n'  % (target_host,target_port),
  
    except Exception as err:
        pass
        # print '[-] Error-3: ',sys.exc_info()[0],err,'\r\n',
        # print '[-] %s:%s error\r\n' % (target_host,target_port),

def scanner(threadId,threadNum,target_host,target_port):
    for i in xrange(threadId,len(target_port),threadNum):
      _scanner(target_host,target_port[i])
        
def main():

   parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
   parser.add_argument("-T", "--target", type=str, help="Target ip", default=None)
   parser.add_argument("-P", "--port", type=str, help="Target port e.g. 1-100 or 21,53,80", default=None)
   parser.add_argument("-N", "--threadNum", type=str, help="Thread num e.g. 100", default=100)
   args = parser.parse_args()


   if args.target == None or args.port == None:
      exit(0)
   else:
      threadNum = int(args.threadNum)
      target_host = args.target
      target_port = args.port

   target_host = anlyze_host(target_host)
   target_port = anlyze_port(target_port)


   print "[.] Run start: Total scan " + str(len(target_port)) + " port!"
   for threadId in xrange(0,threadNum):
      t = threading.Thread(target=scanner,args=(threadId,threadNum,target_host,target_port))
      t.start()
      threadList.append(t)
   for num in xrange(0,threadNum):
      threadList[num].join()
   print "[+] Run over !"

      
if __name__ == '__main__':
   main()
