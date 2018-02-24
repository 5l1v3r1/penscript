#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import argparse
import os
import re


'''
    处理nmap扫描结果
    用法：
        python nmap-deal.py -F test.txt -V -O res.txt
        python nmap-deal.py -F test.txt -X -O res.tx

    test.txt 是 Nmap scan report for至Nmap done为止的内容。

'''

'''
resLit = [{
       "host": "127.0.0.1",
        "info" : [{
            "port" : "22",
            "server" : "unknown",
            "status" : "open",
            "other" : "tcp",
            }],
    }]
'''


def printlog(resLit,out,verbose):
    res = ""
    if verbose :
        for resDic in resLit:
            for result in resDic['info']:
                text = "%s:%s   %s   %s\r\n" %(resDic['host'],result['port'],result['status'],result['server'])
                print text,
                res+=text
    else:
        for resDic in resLit:
            for result in resDic['info']:
                if result['status'] == 'open':
                    text = "%s:%s\r\n" %(resDic['host'],result['port'])
                    print text,
                    res+=text 
                    
            
    if out != None:
        with open(out,'wb') as f:
            f.write(res);
       


def deal(filename,xml):
    resLit = []
    host = ""
    if not xml:
        flag = False
        infoLit = []
        with open(filename, 'r') as f:
            for line in f.readlines():
                text =  line.strip('\r').strip('\n')
                if "Nmap scan report for" in text or  'Nmap done' in text:
                    lit =  re.findall(r'(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|[0-9])(?:\.(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|[0-9])){3}',text)
                    if len(lit)>0  :
                        if flag or 'Nmap done'  in text :
                            resDic = {"host":host,"info":infoLit}
                            resLit.append(resDic)
                        infoLit = []
                        host =  lit[0]
                        flag = True
                        print host
                    else:
                        resDic = {"host":host,"info":infoLit}
                        resLit.append(resDic)
                else:
                    lit =  re.findall(r'(?:^(?:\d)+)(?:/)(?:[\s\S]*)',text)
                    if len(lit)>0:
                        lit = re.split(r'\s+|\/',lit[0])
                        infoDic = {"port":lit[0],"other":lit[1],"status":lit[2],"server":lit[3],"version":"Unknown_Version" if len(lit)< 4 else lit[3]}
                        infoLit.append(infoDic)
    else:
        import xml.etree.ElementTree as ET
        tree = ET.parse(filename)
        root = tree.getroot()
        for host in root.findall('host'):
            host_id = host.find('address').get('addr')
            infoLit = []
            for port in host.iter('port'):
                port_id = port.attrib.get('portid')
                port_protocol = port.attrib.get('protocol')
                port_state = port.find('state').attrib.get('state')
                port_service = port.find('service').attrib.get('name')
                infoDic = {"port":port_id,"status":port_state,"server":port_service,"other":port_protocol}
                infoLit.append(infoDic)
            resDic = {"host":host_id,"info":infoLit}
            resLit.append(resDic)
    return resLit


def argSet(parser):
    parser.add_argument("-F", "--filename",type=str, help="Load file e.g. a.txt", default=None,required=False)
    parser.add_argument("-X", "--xml",action='store_true',help="Load xml file", default=False)
    parser.add_argument("-O", "--out",type=str,help="output file", default=None)
    parser.add_argument("-V", "--verbose",action='store_true',help="verbose", default=False)
    return parser


def handle(args):
    xml = args.xml
    filename = args.filename
    out = args.out
    verbose = args.verbose
    if filename != None:
        if os.path.isfile(filename):
            print "Run start!"
            resLit = deal(filename,xml)
            printlog(resLit,out,verbose)
            print "Run over !"
        else:
            print "The path is not exist!"
     
if __name__=='__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser = argSet(parser)
    args = parser.parse_args()
    handle(args)




