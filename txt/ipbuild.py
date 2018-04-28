#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import argparse
import re  
import struct

'''
    根据ip段生成ip
    python ipbuild.py -S 192.168.1.1 -E 192.168.1.255
    python ipbuild.py -P 192.168.1.1/24 -O ip_all.txt
''' 

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


def build(out,start,end = None):
    if out != None:
        with open(out,'wb') as f:
            if start != None:
                if end !=None:
                    for num in range(ip2num(start),ip2num(end)+1):
                        f.write(num2ip(num)+"\r\n")
                else:
                    tmp = start.split('/')
                    ch = CIDRHelper()  
                    start,end = ch.Parse(tmp[0],int(tmp[1]))
                    for num in range(ip2num(start),ip2num(end)+1):
                        f.write(num2ip(num)+"\r\n")
    else:
        if start != None:
            if end !=None:
                for num in range(ip2num(start),ip2num(end)+1):
                    print num2ip(num)
            else:
                tmp = start.split('/')
                ch = CIDRHelper()  
                start,end = ch.Parse(tmp[0],int(tmp[1]))
                for num in range(ip2num(start),ip2num(end)+1):
                    print num2ip(num)

def argSet(parser):
    parser.add_argument("-S", "--start",type=str, help="start IP", default=None)
    parser.add_argument("-E", "--end",type=str,help="end IP", default=None)
    parser.add_argument("-O", "--out",type=str,help="output file", default=None)
    parser.add_argument("-P", "--part",type=str, help="ip range e.g. 192.168.0.0/16", default=None)
    return parser


def handle(args):
    start = args.start
    end = args.end
    part = args.part
    out = args.out
    print "[.] Run start!"
    if start != None and end!=None:
        build(out,start,end)
    if part !=None:
        build(out,part)
    print "[.] Run over !"

     
if __name__=='__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser = argSet(parser)
    args = parser.parse_args()
    handle(args)
