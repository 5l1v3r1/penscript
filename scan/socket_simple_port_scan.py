# -*- coding: UTF-8 -*-
__author__ = 'orleven'

import socket
import argparse
import re
import threading
import sys


'''
    在nmap无法正常使用的情况下，使用socket爆破tcp端口
'''
threadList = []

class CIDRHelper:  
    def ipFormatChk(self, ip_str):  
        pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"  
        if re.match(pattern, ip_str):  
            return True  
        else:  
            return False  
  
    def masklenChk(self, masklen):  
        if masklen > 0 and masklen < 32:  
            return true  
        else:  
            return false  
  
    def Parse(self, ip, masklen):  
        if False == self.ipFormatChk(ip) :  
            return "0.0.0.1","0.0.0.0"
        ips = ip.split(".")  
        binip = 0  
        for id in ips:  
            binip = binip << 8  
            binip += int(id)  
        mask = (1 << 32) - 1 - ((1<<(32-masklen))-1)  
        a,b,c,d = struct.unpack('BBBB', struct.pack('>I',(binip & mask)))  
        start = ".".join([str(a),str(b),str(c),str(d)])  
        a,b,c,d = struct.unpack('BBBB', struct.pack('>I',(binip & mask)+(2<<(32-masklen-1)) - 1))  
        end = ".".join([str(a),str(b),str(c),str(d)])
        return start,end
  

def ip2num(ip):
    lp = [int(x) for x in ip.split('.')]
    return lp[0] << 24 | lp[1] << 16 | lp[2] << 8 | lp[3]

def num2ip(num):
    ip = ['', '', '', '']
    ip[3] = (num & 0xff)
    ip[2] = (num & 0xff00) >> 8
    ip[1] = (num & 0xff0000) >> 16
    ip[0] = (num & 0xff000000) >> 24
    return '%s.%s.%s.%s' % (ip[0], ip[1], ip[2], ip[3])


def build(start,end = None):
    hosts = []
    if start != None:
        if end !=None:
            for num in range(ip2num(start),ip2num(end)+1):
                hosts.append( num2ip(num))
        else:
            tmp = start.split('/')
            ch = CIDRHelper()  
            start,end = ch.Parse(tmp[0],int(tmp[1]))
            for num in range(ip2num(start),ip2num(end)+1):
                hosts.append( num2ip(num))
    return hosts

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
   #parser.add_argument("-T", "--target", type=str, help="Target ip", default=None)
   parser.add_argument("-P", "--port", type=str, help="Target port e.g. 1-100 or 21,53,80", default="80,21,23")
   parser.add_argument("-N", "--threadNum", type=str, help="Thread num e.g. 100", default=100)
   parser.add_argument("-S", "--start",type=str, help="start IP", default=None)
   parser.add_argument("-E", "--end",type=str,help="end IP", default=None)
   parser.add_argument("-O", "--out",type=str,help="output file", default=None)
   parser.add_argument("-PA", "--part",type=str, help="ip range e.g. 192.168.0.0/16", default=None)
   args = parser.parse_args()
   start = args.start
   end = args.end
   part = args.part

   target_host = []
   if start != None and end!=None:
       target_host = build(start,end)
   if part !=None:
       target_host = build(part)
   threadNum = int(args.threadNum)
   
   #target_host = args.target
   target_port = args.port
   for host in target_host:
       host = anlyze_host(host)
   
   target_port = anlyze_port(target_port)
   #if args.target == None or args.port == None:
   print "[.] Run start: Total scan " + str(len(target_host)*len(target_port)) + " port!"
   if target_host:
       


       
       for host in    target_host:
           for threadId in xrange(0,threadNum):
              t = threading.Thread(target=scanner,args=(threadId,threadNum,host,target_port))
              t.start()
              threadList.append(t)
           for num in xrange(0,threadNum):
              threadList[num].join()
   print "[.] Run over !"

      
if __name__ == '__main__':
   main()
