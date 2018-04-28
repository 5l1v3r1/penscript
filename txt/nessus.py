#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'

import argparse
import os
import re
from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET
import HTMLParser  
'''
ip  port service vul version vul_zn

'''

# 不需要显示的漏洞
pulginidBanList = [
    '11936', # OS Identification
    '19506', # Nessus Scan Information
    '11219', # Nessus SYN scanner
    '10287', # Traceroute Information
    '22964', # Service Detection
    '54615', # Device Type
    '11933', # Do not scan printers
    '45590', # Common Platform Enumeration (CPE)
    '25220', # TCP/IP Timestamps Supported
    '10114', # ICMP Timestamp Request Remote Date Disclosure
    '10919', # Open Port Re-check
    '35716', # Ethernet Card Manufacturer Detection
    '66334', # Patch Report
    '44920', # Do not scan printers (AppSocket)
    '50350', # OS Identification Failed
    '24260', # HyperText Transfer Protocol (HTTP) Information
    '10107', # HTTP Server Type and Version
    '10884', # Network Time Protocol (NTP) Server Detection
    '10281', # Telnet Server Detection
    '10267', # SSH Server Type and Version Information
    '11154', # Unknown Service Detection: Banner Retrieval
    '10736', # DCE Services Enumeration
    '14274', # Nessus SNMP Scanner
    '10150', # Windows NetBIOS / SMB Remote Host Information Disclosure
    '10881', # SSH Protocol Versions Supported
    '11111', # RPC Services Enumeration
    '22073', # Oracle Database Detection
    '10658', # Oracle Database tnslsnr Service Remote Version Disclosure
    "24786", # Nessus Windows Scan Not Performed with Admin Privileges 
    "10397", # Microsoft Windows SMB LanMan Pipe Server Listing Disclosure 
    "10394", # Microsoft Windows SMB Log In Possible 
    "10785", # Microsoft Windows SMB NativeLanManager Remote System Information Disclosure 
    "26917", # Microsoft Windows SMB Registry : Nessus Cannot Access the Windows Registry 
    "11011", # Microsoft Windows SMB Service Detection 
    "100871", # Microsoft Windows SMB Versions Supported (remote check)  
    "106716", # Microsoft Windows SMB2 Dialects Supported (remote check)  
    "96982", # Server Message Block (SMB) Protocol Version 1 Enabled (uncredentialed check) 
    "10758", # VNC HTTP Server Detection 
    "19288", # VNC Server Security Type Detection 
    "65792", # VNC Server Unencrypted Communication Detection 
    "10342", # VNC Software Detection
    "11819", # TFTP Daemon Detection
    "10092", # FTP Server Detection
    "10940", # Windows Terminal Services Enabled
    "66173", # RDP Screenshot
    "43111", # HTTP Methods Allowed (per directory)
    "10052", # Daytime Service Detection
    "10884", # Network Time Protocol (NTP) Server Detection
    "57333", # NNTP Authentication Methods
    "52703", # vsftpd Detection
    "10719", # MySQL Server Detection
    "66293", #Unix Operating System on Extended Support
    "35296", # SNMP Protocol Version Detection  
    "34022", # SNMP Query Routing Information Disclosure  
    "10800", # SNMP Query System Information Disclosure  
    "10551", # SNMP Request Network Interfaces Enumeration  
    "40448", # SNMP Supported Protocols Detection  
    "10548", # Microsoft Windows LAN Manager SNMP LanMan Shares Disclosure  
    "10546", # Microsoft Windows LAN Manager SNMP LanMan Users Disclosure  
    "10263", # SMTP Server Detection
    "10021", # Identd Service Detection
    "11123", # Radmin (Remote Administrator) Port 4899 Detection
    "25201", # Talk Service (talkd, in.talk, ntalk) Detection
    "69482", # Microsoft SQL Server STARTTLS Support  
    "10144", # Microsoft SQL Server TCP/IP Listener Detection
    "10061", # Echo Service Detection
    "18164", # TCP Port 0 Open: Possible Backdoor
    "103869", # Open Network Video Interface Forum (ONVIF) Protocol Detection  
    "103865", # ONVIF Device Information  
    "103866", # ONVIF Device Services  
    "103868", # ONVIF Get Device User List  
    "104275", # ONVIF Stream URI
    "25701", # LDAP Crafted Search Request Server Information Disclosure    
    "20870", # LDAP Server Detection
    "35711", # Universal Plug and Play (UPnP) Protocol Detection
    "11389", # L2TP Network Server Detection
    "43815", # NetBIOS Multiple IP Address Enumeration
    "12218", # mDNS Detection (Remote Network)
    "10794", # Symantec pcAnywhere Detection (TCP)
]

# 资产梳理端口服务探测,功能暂未实现，目前只收录了None型漏洞
pulginidServiceDic = {
    "NetBIOS/SMB":["11011","10736","10150","26917","24786","10397","10394","10785","100871","106716","96982"],
    "HTTP":["10107","24260","43111"],
    "NTP":['10844'],
    "Telnet":["10281"],
    "SSH":["10881","10267"],
    "SNMP":['14274'],
    "RPC":['1111'],
    "Oracle DB":['22073','10658'],
    "VNC":["19288","65792","10342","10758"],
    "TFTP":["11819"],
    "FTP":["10092","52703"],
    "RDP":["10940","66173"],
    "Daytime":["10052"],
    "NTP":["10884","97861",],
    "NNTP":["57333"],
    "Mysql":["10719"],
    "Mssql":["69482","10144"],
    "SNMP":["35296","34022","10800","10551","40448","10548","10546"],
    "SMTP":["10263"],
    "Identd":["10021"],
    "Radmin":["11123"],
    "Talk":["25201"],
    "Echo":["10061"],
    "ONVIF":["103869","103865","103866","103868","104275"],
    "LDAP":["25701","20870"],
    "UPnP":["35711"],
    "L2TP":["11387"],
    "NetBIOS":["43815"],
    "mDNS":["12218"],
    "Symantec pcAnywhere":["10794"],
}


pulginidDic = {
    # Windows Easy
    "34477":{"risk":"【紧急】","vul":"MS08-067: Windows Crafted RPC 请求处理远程代码执行漏洞 ","description":"Windows Crafted RPC 请求处理远程代码执行漏洞 。","solution":"建议及时更新补丁或升级到最新版本。"},
    
    # Windows Diff
    "79638":{"risk":"【紧急】","vul":"MS14-066: Schannel远程代码执行漏洞 ","description":"Schannel远程代码执行漏洞 。","solution":"建议及时更新补丁或升级到最新版本。"},
    "35362":{"risk":"【紧急】","vul":"MS09-001: SMB远程代码执行漏洞 ","description":"SMB远程代码执行漏洞 。","solution":"建议及时更新补丁或升级到最新版本。"},
    "20008":{"risk":"【紧急】","vul":"MS05-051: MSDTC远程代码执行漏洞","description":"MSDTC远程代码执行漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "21334":{"risk":"【紧急】","vul":"MS06-018: Windows分布式事务处理协调器拒绝服务漏洞 ","description":"Windows分布式事务处理协调器拒绝服务漏洞 。","solution":"建议及时更新补丁或升级到最新版本。"},
    "11835":{"risk":"【紧急】","vul":"MS03-039: RPC 接口字符溢出漏洞 ","description":"RPC 接口字符溢出漏洞 。","solution":"建议及时更新补丁或升级到最新版本。"},
    "12054":{"risk":"【紧急】","vul":"MS04-007: ASN.1远程代码执行漏洞 ","description":"ASN.1远程代码执行漏洞 。","solution":"建议及时更新补丁或升级到最新版本。"},
    "12209":{"risk":"【紧急】","vul":"MS04-011: Windows安全更新漏洞","description":"Windows安全更新漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "22034":{"risk":"【高危】","vul":"MS06-035: Windows远程代码执行漏洞","description":"Windows远程代码执行漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "54585":{"risk":"【高危】","vul":"MS11-035: Wins远程代码执行漏洞","description":"Wins远程代码执行漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "58435":{"risk":"【高危】","vul":"MS12-020: RDP远程代码执行漏洞 ","description":"RDP远程代码执行漏洞 。","solution":"建议及时更新补丁或升级到最新版本。"},
    "90510":{"risk":"【中危】","vul":"MS16-047: SAM and LSAD 安全更新漏洞 ","description":"SAM and LSAD 安全更新漏洞 。","solution":"建议及时更新补丁或升级到最新版本。"},
    

    # Telnet
    "42263":{"risk":"【中危】","vul":"Telnet明文传输","description":"Telnet采用明文的方式进行数据传输，容易受到中间人攻击导致信息泄露等风险。","solution":"建议使用其他加密传输的协议代替，例如SSH等。"},

    # Apache
    "45004":{"risk":"【紧急】","vul":"Apache 2.2.x < 2.2.15 多个漏洞","description":"Apache 2.2.x < 2.2.15 存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "77531":{"risk":"【高危】","vul":"Apache 2.2.x < 2.2.23 多个漏洞","description":"Apache 2.2.x < 2.2.23 存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "101787":{"risk":"【高危】","vul":"Apache 2.2.x < 2.2.34 多个漏洞","description":"Apache 2.2.x < 2.2.34 存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},    
    "100995":{"risk":"【高危】","vul":"Apache 2.2.x < 2.2.33-dev / 2.4.x < 2.4.26 多个漏洞","description":"Apache 2.2.x < 2.2.33-dev / 2.4.x < 2.4.26 存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "33477":{"risk":"【中危】","vul":"Apache 2.2.x < 2.2.9 多个漏洞(DoS, XSS)","description":"Apache 2.2.x < 2.2.9 存在多个安全漏洞,例如DoS、 XSS。","solution":"建议及时更新补丁或升级到最新版本。"},
    "48205":{"risk":"【中危】","vul":"Apache 2.2.x < 2.2.16 多个漏洞","description":"Apache 2.2.x < 2.2.16 存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "50070":{"risk":"【中危】","vul":"Apache 2.2.x < 2.2.17 多个漏洞","description":"Apache 2.2.x < 2.2.17 存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "53896":{"risk":"【中危】","vul":"Apache 2.2.x < 2.2.18 APR apr_fnmatch DoS漏洞","description":"Apache 2.2.x < 2.2.18 APR apr_fnmatch DoS漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "56216":{"risk":"【中危】","vul":"Apache 2.2.x < 2.2.21 mod_proxy_ajp DoS漏洞","description":"Apache 2.2.x < 2.2.21 mod_proxy_ajp DoS漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "57791":{"risk":"【中危】","vul":"Apache 2.2.x < 2.2.22 多个漏洞","description":"Apache 2.2.x < 2.2.22 存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "62101":{"risk":"【中危】","vul":"Apache 2.2.x < 2.2.23 多个漏洞","description":"Apache 2.2.x < 2.2.23 存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "64912":{"risk":"【中危】","vul":"Apache 2.2.x < 2.2.24 多个XSSl漏洞","description":"Apache 2.2.x < 2.2.24 存在多个XSS漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "68915":{"risk":"【中危】","vul":"Apache 2.2.x < 2.2.25 多个漏洞","description":"Apache 2.2.x < 2.2.25 存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "73405":{"risk":"【中危】","vul":"Apache 2.2.x < 2.2.27 多个漏洞","description":"Apache 2.2.x < 2.2.27 存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},

    # PHP
    "76281":{"risk":"【紧急】","vul":"PHP 5.4.x < 5.4.30 多个漏洞","description":"PHP 5.4.x < 5.4.30 多个漏洞  ","solution":"建议及时更新补丁或升级到最新版本。"},
    "83033":{"risk":"【紧急】","vul":"PHP 5.4.x < 5.4.40 多个漏洞","description":"PHP 5.4.x < 5.4.40 多个漏洞  ","solution":"建议及时更新补丁或升级到最新版本。"},
    "85885":{"risk":"【紧急】","vul":"PHP 5.4.x < 5.4.45 多个漏洞","description":"PHP 5.4.x < 5.4.45 多个漏洞  ","solution":"建议及时更新补丁或升级到最新版本。"},
    "17796":{"risk":"【高危】","vul":"PHP 4.x < 4.3.0 ZendEngine 整数溢出","description":"PHP 4.x < 4.3.0 ZendEngine 整数溢出漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "15973":{"risk":"【高危】","vul":"PHP < 4.3.10 / 5.0.3 多个漏洞","description":"PHP < 4.3.10 / 5.0.3 多个漏洞  ","solution":"建议及时更新补丁或升级到最新版本。"},
    "18033":{"risk":"【高危】","vul":"PHP < 4.3.11 / 5.0.3 多个","description":"PHP < 4.3.11 / 5.0.3 存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "11850":{"risk":"【高危】","vul":"PHP < 4.3.3 多个漏洞","description":"PHP < 4.3.3 存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "20111":{"risk":"【高危】","vul":"PHP < 4.4.1 / 5.0.6 多个漏洞","description":"PHP < 4.4.1 / 5.0.6 存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "22268":{"risk":"【高危】","vul":"PHP < 4.4.3 / 5.1.4 多个漏洞","description":"PHP < 4.4.3 / 5.1.4 存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "17710":{"risk":"【高危】","vul":"PHP < 4.4.4 多个漏洞","description":"PHP < 4.4.4 存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "24906":{"risk":"【高危】","vul":"PHP < 4.4.5 多个漏洞","description":"PHP < 4.4.5 存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "29833":{"risk":"【高危】","vul":"PHP < 4.4.8 多个漏洞","description":"PHP < 4.4.8 存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "33849":{"risk":"【高危】","vul":"PHP < 4.4.9 多个漏洞","description":"PHP < 4.4.9 存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "41014":{"risk":"【高危】","vul":"PHP < 5.2.11 多个漏洞","description":"PHP < 5.2.11 存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "35067":{"risk":"【高危】","vul":"PHP < 5.2.8 多个漏洞","description":"PHP < 5.2.8 存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "58966":{"risk":"【高危】","vul":"PHP < 5.3.11 多个漏洞","description":"PHP < 5.3.11存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "58988":{"risk":"【高危】","vul":"PHP < 5.3.12 / 5.4.2 CGI 查询字符串代码执行","description":"PHP < 5.3.12 / 5.4.2 CGI 查询字符串代码执行漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "57537":{"risk":"【高危】","vul":"PHP < 5.3.9 多个漏洞","description":"PHP < 5.3.9 存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "72881":{"risk":"【高危】","vul":"PHP 5.4.x < 5.4.26 多个漏洞","description":"PHP 5.4.x < 5.4.26 存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "77402":{"risk":"【高危】","vul":"PHP 5.4.x < 5.4.32 多个漏洞","description":"PHP 5.4.x < 5.4.32 存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "78545":{"risk":"【高危】","vul":"PHP 5.4.x < 5.4.34 多个漏洞","description":"PHP 5.4.x < 5.4.34 存在多个安全漏洞 ","solution":"建议及时更新补丁或升级到最新版本。"},
    "79246":{"risk":"【高危】","vul":"PHP 5.4.x < 5.4.35 'donote' DoS","description":"PHP 5.4.x < 5.4.35 'donote' DoS  ","solution":"建议及时更新补丁或升级到最新版本。"},
    "80330":{"risk":"【高危】","vul":"PHP 5.4.x < 5.4.36 'process_nested_data' RCE","description":"PHP 5.4.x < 5.4.36 'process_nested_data' RCE  ","solution":"建议及时更新补丁或升级到最新版本。"},
    "81080":{"risk":"【高危】","vul":"PHP 5.4.x < 5.4.37 多个漏洞","description":"PHP 5.4.x < 5.4.37 存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "81510":{"risk":"【高危】","vul":"PHP 5.4.x < 5.4.38 多个漏洞 (GHOST)","description":"PHP 5.4.x < 5.4.38 存在多个安全漏洞 (GHOST)  ","solution":"建议及时更新补丁或升级到最新版本。"},
    "82025":{"risk":"【高危】","vul":"PHP 5.4.x < 5.4.39 多个漏洞","description":"PHP 5.4.x < 5.4.39 存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "83517":{"risk":"【高危】","vul":"PHP 5.4.x < 5.4.41 多个漏洞","description":"PHP 5.4.x < 5.4.41 存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "84362":{"risk":"【高危】","vul":"PHP 5.4.x < 5.4.42 多个漏洞","description":"PHP 5.4.x < 5.4.42 存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "85298":{"risk":"【高危】","vul":"PHP 5.4.x < 5.4.44 多个漏洞","description":"PHP 5.4.x < 5.4.44 存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "39480":{"risk":"【中危】","vul":"PHP < 5.2.10 多个漏洞","description":"PHP < 5.2.10 存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "43351":{"risk":"【中危】","vul":"PHP < 5.2.12 多个漏洞","description":"PHP < 5.2.12 存在多个安全漏洞 ","solution":"建议及时更新补丁或升级到最新版本。"},
    "35750":{"risk":"【中危】","vul":"PHP < 5.2.9 多个漏洞","description":"PHP < 5.2.9 存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "44921":{"risk":"【中危】","vul":"PHP < 5.3.2 / 5.2.13 多个漏洞","description":"PHP < 5.3.2 / 5.2.13 存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "11444":{"risk":"【中危】","vul":"PHP Mail 函数头","description":"PHP Mail 存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "17687":{"risk":"【中危】","vul":"PHP Multiple Image Processing 文件处理函数DOS","description":"PHP Multiple Image Processing 文件处理函数DOS漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "15436":{"risk":"【中危】","vul":"PHP php_variables.c 多个变量内存泄露","description":"PHP php_variables.c 存在多个变量内存泄露漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "11468":{"risk":"【中危】","vul":"PHP socket_iovec_alloc() 函数溢出漏洞","description":"PHP socket_iovec_alloc() 函数溢出漏洞  ","solution":"建议及时更新补丁或升级到最新版本。"},
    "71927":{"risk":"【中危】","vul":"PHP 5.4.x < 5.4.24 多个漏洞","description":"PHP 5.4.x < 5.4.24存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "73338":{"risk":"【中危】","vul":"PHP 5.4.x < 5.4.27 awk Magic Parsing BEGIN DoS","description":"PHP 5.4.x < 5.4.27 awk Magic Parsing BEGIN DoS  ","solution":"建议及时更新补丁或升级到最新版本。"},
    "73862":{"risk":"【中危】","vul":"PHP 5.4.x < 5.4.28 FPM Unix Socket 权限提升漏洞","description":"PHP 5.4.x < 5.4.28 FPM Unix Socket 权限提升漏洞  ","solution":"建议及时更新补丁或升级到最新版本。"},
    "74291":{"risk":"【中危】","vul":"PHP 5.4.x < 5.4.29 'src/cdf.c' 多个漏洞","description":"PHP 5.4.x < 5.4.29 'src/cdf.c'存在多个安全漏洞","solution":"建议及时更新补丁或升级到最新版本。"},
    "84671":{"risk":"【中危】","vul":"PHP 5.4.x < 5.4.43 多个漏洞 (BACKRONYM)","description":"PHP 5.4.x < 5.4.43 存在多个安全漏洞(BACKRONYM)  ","solution":"建议及时更新补丁或升级到最新版本。"},
    "17709":{"risk":"【低危】","vul":"PHP < 4.4.2 多个XSS","description":"PHP < 4.4.2 存在多个XSS漏洞","solution":"建议及时更新补丁或升级到最新版本。"},

    # HP 系统管理页面
    "91222":{"risk":"【紧急】","vul":"HP 系统管理页面 多个漏洞(HPSBMU03593) ","description":"HP 系统管理页面 存在多个安全漏洞(HPSBMU03593) 。","solution":"建议及时更新补丁或升级到最新版本。"},
    "85181":{"risk":"【紧急】","vul":"HP 系统管理页面 < 7.2.5 / 7.4.1 多个漏洞(POODLE) ","description":"HP 系统管理页面 < 7.2.5 / 7.4.1 存在多个安全漏洞(POODLE) 。","solution":"建议及时更新补丁或升级到最新版本。"},
    "90150":{"risk":"【紧急】","vul":"HP 系统管理页面 < 7.5.4 多个漏洞(Logjam) ","description":"HP 系统管理页面 < 7.5.4 存在多个安全漏洞(Logjam) 。","solution":"建议及时更新补丁或升级到最新版本。"},
    "94654":{"risk":"【紧急】","vul":"HP 系统管理页面 < 7.6 多个漏洞(HPSBMU03653) (httpoxy) ","description":"HP 系统管理页面 < 7.6 存在多个安全漏洞(HPSBMU03653) (httpoxy) 。","solution":"建议及时更新补丁或升级到最新版本。"},
    "46015":{"risk":"【紧急】","vul":"HP 系统管理页面 < 6.0.0.96 / 6.0.0-95 多个漏洞","description":"HP 系统管理页面 < 6.0.0.96 / 6.0.0-95 存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "53532":{"risk":"【紧急】","vul":"HP 系统管理页面 < 6.3 多个漏洞","description":"HP 系统管理页面 < 6.3 存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "58811":{"risk":"【紧急】","vul":"HP 系统管理页面 < 7.0 多个漏洞","description":"HP 系统管理页面 < 7.0 存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "59851":{"risk":"【高危】","vul":"HP 系统管理页面 < 7.1.1 多个漏洞","description":"HP 系统管理页面 < 7.1.1 存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "66541":{"risk":"【高危】","vul":"HP 系统管理页面 < 7.2.0.14 iprange 参数命令注入","description":"HP 系统管理页面 < 7.2.0.14 iprange参数命令注入 。","solution":"建议及时更新补丁或升级到最新版本。"},
    "69020":{"risk":"【高危】","vul":"HP 系统管理页面 < 7.2.1.0 多个漏洞(BEAST) ","description":"HP 系统管理页面 < 7.2.1.0 存在多个安全漏洞(BEAST) 。","solution":"建议及时更新补丁或升级到最新版本。"},
    "76345":{"risk":"【高危】","vul":"HP 系统管理页面 < 7.2.4.1 / 7.3.3.1 OpenSSL 多个漏洞","description":"HP 系统管理页面 < 7.2.4.1 / 7.3.3.1 OpenSSL 存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "46677":{"risk":"【高危】","vul":"HP 系统管理页面 < 6.1.0.102 / 6.1.0-103 多个漏洞","description":"HP 系统管理页面 < 6.1.0.102 / 6.1.0-103 存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "49272":{"risk":"【高危】","vul":"HP 系统管理页面 < 6.2 多个漏洞","description":"HP 系统管理页面 < 6.2 存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "90251":{"risk":"【高危】","vul":"HP 系统管理页面 < 7.2.6 多个漏洞(FREAK) ","description":"HP 系统管理页面 < 7.2.6 存在多个安全漏洞(FREAK) 。","solution":"建议及时更新补丁或升级到最新版本。"},
    "70118":{"risk":"【高危】","vul":"HP 系统管理页面 ginkgosnmp.inc 命令注入","description":"HP 系统管理页面 ginkgosnmp.inc 命令注入漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "103530":{"risk":"【高危】","vul":"HP 系统管理页面 < 7.6.1 多个漏洞(HPSBMU03753)","description":"HP 系统管理页面 < 7.6.1 存在多个安全漏洞(HPSBMU03753)。","solution":"建议及时更新补丁或升级到最新版本。"},
    "38832":{"risk":"【中危】","vul":"HP 系统管理页面 < 3.0.1.73 多个缺陷","description":"HP 系统管理页面 < 3.0.1.73 存在多个缺陷 。","solution":"建议及时更新补丁或升级到最新版本。"},
    "72959":{"risk":"【中危】","vul":"HP 系统管理页面 < 7.3 多个漏洞","description":"HP 系统管理页面 < 7.3 存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},

    # 版本过低
    "56997":{"risk":"【紧急】","vul":"VMware ESX / ESXi 官方不支持","description":"VMware ESX / ESXi 版本过低，官方不再提供支持。","solution":"建议升级到最新版本。"},
    "78555":{"risk":"【紧急】","vul":"OpenSSL 官方不支持 ","description":"OpenSSL 版本过低，官方不再提供支持。","solution":"建议升级到最新版本。"},
    "19699":{"risk":"【紧急】","vul":"Microsoft Windows NT 4.0 官方不支持 ","description":"Microsoft Windows NT 4.0 版本过低，官方不再提供支持。","solution":"建议升级到最新版本。"},
    "84729":{"risk":"【紧急】","vul":"Microsoft Windows Server 2003 官方不支持(ERRATICGOPHER)  ","description":"Microsoft Windows Server 2003 版本过低，官方不再提供支持 (ERRATICGOPHER)。","solution":"建议升级到最新版本。"},
    "73182":{"risk":"【紧急】","vul":"Microsoft Windows XP 官方不支持(ERRATICGOPHER)  ","description":"Microsoft Windows XP 版本过低，官方不再提供支持 (ERRATICGOPHER) 。","solution":"建议升级到最新版本。"},
    "55786":{"risk":"【紧急】","vul":"Oracle Database 官方不支持","description":"Oracle Database 版本过低，官方不再提供支持。","solution":"建议升级到最新版本。"},
    "58987":{"risk":"【紧急】","vul":"PHP 官方不支持","description":"PHP 版本过低，官方不再提供支持。","solution":"建议升级到最新版本。"},
    "97994":{"risk":"【紧急】","vul":"Microsoft IIS 6.0 官方不支持","description":"Microsoft IIS 6.0 版本过低，官方不再提供支持。","solution":"建议升级到最新版本。"},
    "34460":{"risk":"【高危】","vul":"Web Server官方不支持","description":"Web Server 版本过低，官方不再提供支持。","solution":"建议升级到最新版本。"},

    # SSL
    "94437":{"risk":"【中危】","vul":"SSL 支持64-bit长度的密码套件 (SWEET32)","description":"SSL 支持64-bit长度的密码套件 (SWEET32) ，存在安全隐患。","solution":"建议及时更新补丁或升级到最新版本。"},
    "51192":{"risk":"【中危】","vul":"SSL 证书不受信任","description":"SSL 证书不受信任 ，存在安全隐患。","solution":"建议及时更新补丁或升级到最新版本。"},
    "35291":{"risk":"【中危】","vul":"SSL 证书签名使用弱哈希算法","description":"SSL 证书签名使用弱哈希算法，存在安全隐患。","solution":"建议及时更新补丁或升级到最新版本。"},
    "42873":{"risk":"【中危】","vul":"SSL 支持中等长度的密码套件","description":"SSL 支持中等长度的密码套件，存在安全隐患。","solution":"建议及时更新补丁或升级到最新版本。"}, 
    "65821":{"risk":"【低危】","vul":"SSL 支持RC4密码套件 (Bar Mitzvah)","description":"SSL 支持RC4密码套件 (Bar Mitzvah) ，存在安全隐患。","solution":"建议及时更新补丁或升级到最新版本。"},
    "57582":{"risk":"【中危】","vul":"SSL 自签名Certificate","description":"SSL 自签名证书，存在安全隐患。","solution":"建议及时更新补丁或升级到最新版本。"},
    "20007":{"risk":"【中危】","vul":"SSL Version 2 and 3 协议","description":"SSL Version 2 and 3 协议  ，存在安全隐患。","solution":"建议及时更新补丁或升级到最新版本。"}, 

    # openssl
    "74363":{"risk":"【高危】","vul":"OpenSSL 0.9.8 < 0.9.8za多个漏洞","description":"OpenSSL 0.9.8 < 0.9.8za存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "77086":{"risk":"【高危】","vul":"OpenSSL 0.9.8 < 0.9.8zb多个漏洞","description":"OpenSSL 0.9.8 < 0.9.8zb存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "17766":{"risk":"【高危】","vul":"OpenSSL < 0.9.8p / 1.0.0b缓冲区溢出","description":"OpenSSL < 0.9.8p / 1.0.0b缓冲区溢出。","solution":"建议及时更新补丁或升级到最新版本。"},
    "57459":{"risk":"【高危】","vul":"OpenSSL < 0.9.8s多个漏洞","description":"OpenSSL < 0.9.8s存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "58799":{"risk":"【高危】","vul":"OpenSSL < 0.9.8w ASN.1 asn1_d2i_read_bio内存损坏","description":"OpenSSL < 0.9.8w ASN.1 asn1_d2i_read_bio内存损坏。","solution":"建议及时更新补丁或升级到最新版本。"},
    "17751":{"risk":"【高危】","vul":"OpenSSL 0.9.6 CA基本约束验证漏洞","description":"OpenSSL 0.9.6 CA基本约束验证漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "17746":{"risk":"【高危】","vul":"OpenSSL < 0.9.6e多个漏洞","description":"OpenSSL < 0.9.6e存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "17752":{"risk":"【高危】","vul":"OpenSSL < 0.9.7-beta3缓冲区溢出","description":"OpenSSL < 0.9.7-beta3缓冲区溢出。","solution":"建议及时更新补丁或升级到最新版本。"},
    "17760":{"risk":"【高危】","vul":"OpenSSL < 0.9.8f多个漏洞","description":"OpenSSL < 0.9.8f存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "59076":{"risk":"【中危】","vul":"OpenSSL 0.9.8 < 0.9.8x DTLS CBC dos漏洞","description":"OpenSSL 0.9.8 < 0.9.8x DTLS CBC dos漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "78552":{"risk":"【中危】","vul":"OpenSSL 0.9.8 < 0.9.8zc多个漏洞（POODLE）","description":"OpenSSL 0.9.8 < 0.9.8zc多个漏洞（POODLE）。","solution":"建议及时更新补丁或升级到最新版本。"},
    "80566":{"risk":"【中危】","vul":"OpenSSL 0.9.8 < 0.9.8zd多个漏洞（FREAK）","description":"OpenSSL 0.9.8 < 0.9.8zd多个漏洞（FREAK）。","solution":"建议及时更新补丁或升级到最新版本。"},
    "82030":{"risk":"【中危】","vul":"OpenSSL 0.9.8 < 0.9.8zf多个漏洞","description":"OpenSSL 0.9.8 < 0.9.8zf存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "84151":{"risk":"【中危】","vul":"OpenSSL 0.9.8 < 0.9.8zg多个漏洞","description":"OpenSSL 0.9.8 < 0.9.8zg存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "87219":{"risk":"【中危】","vul":"OpenSSL 0.9.8 < 0.9.8zh X509_ATTRIBUTE内存泄漏DoS","description":"OpenSSL 0.9.8 < 0.9.8zh X509_ATTRIBUTE内存泄漏DoS。","solution":"建议及时更新补丁或升级到最新版本。"},
    "56996":{"risk":"【中危】","vul":"OpenSSL < 0.9.8小时多个漏洞","description":"OpenSSL < 0.9.8小时存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "17761":{"risk":"【中危】","vul":"OpenSSL < 0.9.8i dos漏洞","description":"OpenSSL < 0.9.8i dos漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "17762":{"risk":"【中危】","vul":"OpenSSL < 0.9.8j签名欺骗","description":"OpenSSL < 0.9.8j签名欺骗。","solution":"建议及时更新补丁或升级到最新版本。"},
    "17763":{"risk":"【中危】","vul":"OpenSSL < 0.9.8k多个漏洞","description":"OpenSSL < 0.9.8k存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "17765":{"risk":"【中危】","vul":"OpenSSL < 0.9.8l多个漏洞","description":"OpenSSL < 0.9.8l存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "17767":{"risk":"【中危】","vul":"OpenSSL < 0.9.8p / 1.0.0e双重免费漏洞","description":"OpenSSL < 0.9.8p / 1.0.0e双重免费漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "58564":{"risk":"【中危】","vul":"OpenSSL < 0.9.8u多个漏洞","description":"OpenSSL < 0.9.8u存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "64532":{"risk":"【中危】","vul":"OpenSSL < 0.9.8y多个漏洞","description":"OpenSSL < 0.9.8y存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "17745":{"risk":"【中危】","vul":"OpenSSL < 0.9.6b可预测随机生成器","description":"OpenSSL < 0.9.6b可预测随机生成器。","solution":"建议及时更新补丁或升级到最新版本。"},
    "17747":{"risk":"【中危】","vul":"OpenSSL < 0.9.6f dos漏洞","description":"OpenSSL < 0.9.6f dos漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "11267":{"risk":"【中危】","vul":"OpenSSL < 0.9.6j / 0.9.7b多个漏洞","description":"OpenSSL < 0.9.6j / 0.9.7b存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "17748":{"risk":"【中危】","vul":"OpenSSL < 0.9.6k dos漏洞","description":"OpenSSL < 0.9.6k dos漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "17749":{"risk":"【中危】","vul":"OpenSSL < 0.9.6l dos漏洞","description":"OpenSSL < 0.9.6l dos漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "12110":{"risk":"【中危】","vul":"OpenSSL < 0.9.6m / 0.9.7d多个远程DoS","description":"OpenSSL < 0.9.6m / 0.9.7d多个远程DoS。","solution":"建议及时更新补丁或升级到最新版本。"},
    "17759":{"risk":"【中危】","vul":"OpenSSL < 0.9.8弱缺省配置","description":"OpenSSL < 0.9.8弱缺省配置。","solution":"建议及时更新补丁或升级到最新版本。"},
    "17754":{"risk":"【低危】","vul":"OpenSSL < 0.9.7f不安全的临时文件创建","description":"OpenSSL < 0.9.7f不安全的临时文件创建。","solution":"建议及时更新补丁或升级到最新版本。"},

    # openssh
    "44077":{"risk":"【高危】","vul":"OpenSSH < 4.​​5多个漏洞","description":"OpenSSH < 4.​​5存在多个安全漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "44078":{"risk":"【高危】","vul":"OpenSSH < 4.​​7可信X11 Cookie连接策略绕过","description":"OpenSSH < 4.​​7可信X11 Cookie连接策略绕过。","solution":"建议及时更新补丁或升级到最新版本。"},
    "44065":{"risk":"【中危】","vul":"OpenSSH < 5.2 CBC明文泄露漏洞","description":"OpenSSH < 5.2 CBC明文泄露漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "44076":{"risk":"【中危】","vul":"OpenSSH < 4.​​3 scp命令行文件名处理命令注入漏洞","description":"OpenSSH < 4.​​3 scp命令行文件名处理命令注入漏洞。","solution":"建议及时更新补丁或升级到最新版本。"},
    "44079":{"risk":"【中危】","vul":"OpenSSH < 4.​​9'ForceCommand'指令旁路","description":"OpenSSH < 4.​​9'ForceCommand'指令旁路。","solution":"建议及时更新补丁或升级到最新版本。"},
    "31737":{"risk":"【中危】","vul":"OpenSSH X11转发会话劫持","description":"OpenSSH X11转发会话劫持。","solution":"建议及时更新补丁或升级到最新版本。"},

    # NTP
    "97861":{"risk":"【中危】","vul":"NTP Mode 6","description":"NTP Mode 6。","solution":"建议限制NTP模式6的查询。"},
}


'''
def load_html(filename,dataElementOrder=['host','port','vul','OS'],groupby="plugin",zeroFlag = False):
    ipList ,resList = [],[]
    print dataElementOrder
    if groupby == 'host':
        if os.path.isfile(filename):
            osInfo,ipInfo = "Unknown","Unknown"
            hostFlag,vulFlag,osInfoFlag,ipInfoFlag,infoFlag,vulFlag = False,False,False,False,False,False
            with open(filename,"rb") as infile:
                for line in infile.readlines():
                    
                    if "Vulnerabilities By Host" in line :
                        # print '1'
                        vulFlag = True if hostFlag else False
                        hostFlag = False if hostFlag else True
                    if hostFlag :
                        temptext =  re.search(r'(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|[0-9])(?:\.(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|[0-9])){3}',line)
                        if temptext != None:
                            ipList.append(temptext.group())
                    elif vulFlag:
                        # print '1'
                        if '>IP:<' in line:      # 匹配第一次ip信息
                            ipInfoFlag = True   
                        elif ipInfoFlag :       # 匹配第一次ip信息
                            temptext = re.search(r'(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|[0-9])(?:\.(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|[0-9])){3}',line)
                            if temptext != None:
                                ipInfo = temptext.group()
                                ipInfoFlag = False
                                infoFlag = True   # 防止有ip没有os的读取逻辑问题
                        elif '>OS:<' in line:   # 匹配第一次OS信息
                            osInfoFlag = True
                        elif osInfoFlag:        # 匹配第一次OS信息
                            temptext = re.search(r'>[a-zA-Z0-9\, \.\-\(\)]+<',line)
                            if temptext != None:
                                osInfo = temptext.group()[1:-1]
                                osInfoFlag = False
                                infoFlag = False 
                        else:
                            temptext =  re.search(r'btag\-(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|[0-9])(?:\.(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|[0-9])){3}\-\d+\/\w+\-\d+',line)
                            if temptext != None:
                                if infoFlag:     # infoFlag 开关打开，说明os信息不匹配，重置osInfo
                                    osInfo = "Unknown"
                               
                                tag ,host , port , protocal ,pulginid1 = re.split(r'-|/',temptext.group())
                            else:
                                temptext = re.search(r'\d+ - [a-zA-Z 0-9\-/\(\)\.\,\&\;]+',line)
                                if temptext != None:
                                    temp = temptext.group().split(' - ')
                                    #print temp
                                    #print len(temp)
                                    if len(temp)>2:
                                        pulginid2, vul =temp[0], temp[1]+temp[2]
                                    else: 
                                        pulginid2, vul =  temp
                                    vul = vul.replace("&lt;","<").replace("&gt;",">")
                                    if pulginid2 == pulginid2 and pulginid2 not in pulginidBanList:
                                        vulFlag = True   # 开启匹配漏洞信息
                                        resDic = {"host":host,"port":port,"protocal":protocal,"pulginid":pulginid1,"vul":vul,"OS":osInfo}
                                        resList.append(resDic)
                                        # print resDic
                                        #oufile.write("host: "+host+", port: "+port+", protocal: "+protocal+", pulginid: "+pulginid1+", vul: "+vul+", OS: "+ osInfo+"\r\n")
                                        # oufile.write("host: "+host+", port: "+port+", vul: "+vul+", OS: "+ osInfo+"\r\n")
                                #if vulFlag : # 漏洞信息开关打开
                                    
        else:
            print "no file"
                                    # = False
    resList = sorted(resList, key=lambda x: (x[dataElementOrder[0]], x[dataElementOrder[1]], x[dataElementOrder[2]],x[dataElementOrder[3]]))
    with open(filename+ "_res.txt","wb") as oufile:
        # 按照漏洞排
        tempDateKey =  ""
        for tempdic in resList:
            res = ""
            if tempDateKey != tempdic[dataElementOrder[0]]:
                oufile.write("\r\n\r\n"+dataElementOrder[0]+": "+tempdic[dataElementOrder[0]]+ ":\r\n")
                tempDateKey = tempdic[dataElementOrder[0]]
            for i in xrange(1,len(dataElementOrder)):
                res += dataElementOrder[i]+": "+tempdic[dataElementOrder[i]]+ ", "
            oufile.write(res[:-2]+"\r\n")
            #oufile.write(dataElementOrder[0]+": "+tempdic[dataElementOrder[0]]+ ", "+
                          #dataElementOrder[1]+": "+tempdic[dataElementOrder[1]]+ ", "+
                          #dataElementOrder[2]+": "+tempdic[dataElementOrder[2]]+ ", "+
                          #dataElementOrder[3]+": "+tempdic[dataElementOrder[3]]+ "\r\n");
            
            #oufile.write("host: "+tempdic['host']+", port: "+tempdic['port']+", vul: "+tempdic['vul']+", OS: "+ tempdic['OS']+"\r\n")

    return  ipList,  resList
'''

def getContent(line):
    line = line.replace('<br>'," ")
    temptext =  re.search(r'>[a-zA-Z0-9\.\-:\ &;\',_\/\(\)\=]{2,}<',line)
    if temptext != None:
        text = temptext.group()[1:-1]
        return text
    return None

osInfo,ipInfo,portInfo,vulInfo,pulginidInfo,riskInfo,serviceInfo = "Unknown","Unknown","Unknown","Unknown","Unknown","Unknown","Unknown"
hostFlag,vulFlag,osInfoFlag,ipInfoFlag,infoFlag,vulFlag,riskFlag = False,False,False,False,False,False,False
# portFlag = False

def loadHostMode(text,resList):
    global osInfoFlag,ipInfoFlag,infoFlag,riskFlag
    # global portFlag 
    global osInfo,ipInfo
    global portInfo,vulInfo,pulginidInfo,riskInfo,serviceInfo
    # global hostFlag,vulFlag,vulFlag
    temptext = re.search(r'\d{1,5}\/(tcp|udp|icmp)',text)
    if 'IP:' in text:      # 匹配第一次ip信息
        ipInfoFlag = True
        osInfo = "Unknown"
    elif ipInfoFlag :# 匹配第一次ip信息
        ipInfo = text
        ipInfoFlag = False
        infoFlag = True   # 防止有ip没有os的读取逻辑问题
    elif 'OS:' in text:   # 匹配第一次OS信息
        osInfoFlag = True
    elif osInfoFlag:        # 匹配第一次OS信息
        osInfo = text
        osInfoFlag = False
        infoFlag = False
    elif temptext!= None and len(text)<13:  #  防止匹配到Port 23/tcp was found to be open  Cisco
        portInfo = "("+text+")"
    elif "Ports" == text:
        if pulginidInfo not in pulginidBanList:
            res = {"host":ipInfo,"port":portInfo,"os":osInfo,"vul":vulInfo,"pulginid":pulginidInfo,"risk":riskInfo}
            return res  
    elif "Risk Factor" in text :
        riskFlag = True
    elif riskFlag :
        riskInfo = text
        riskFlag = False
    else:
        temptext = re.search(r'^\d+ - [a-zA-Z 0-9\-/\(\)\.\,\&\;\_\:\'\"\=]+',text) # 更新正则，防止匹配到 Upgrade to Oracle 9.2.0.3 - http://metalink.oracle.com
        if temptext!= None : 
            temp = temptext.group().replace("&lt;","<").replace("&gt;",">").split(' - ')
            pulginidInfo,vulInfo = temp[0],' '.join(temp[1:])


def loadVulMode(text,resList):
    pass

def loadHtml(filename,reportMode = "vul"):
    myList, resList = [],[]
    myFlag = 0
    temptext = None
    with open(filename,"rb") as infile:
        for line in infile.readlines():
            text = getContent(line)
            if text != None:
                if myFlag == 2 and reportMode == "host":
                    res = loadHostMode(text,resList)
                    if res!=None :
                        resList.append(res)
                elif myFlag == 2 and reportMode == "vul":
                    res = loadVulMode(text,resList)
                    if res!=None :
                        resList.append(res)
                elif "Vulnerabilities By Host" in text :
                    reportMode = "host"
                    myFlag +=1
                elif "Vulnerabilities By Plugin" in text:
                    reportMode = "vul"
                    myFlag +=1 
                elif myFlag == 1 :
                    #print text
                    if reportMode == "vul":
                        temptext = re.search(r'\d+ \(\d+\)\ [0-9a-zA-Z:\- &;\(\)\/_\=\.]+',text)
                    else:
                        temptext =  re.search(r'(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|[0-9])(?:\.(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|[0-9])){3}',text)
                    if temptext != None:
                        myList.append(temptext.group().replace("&lt;","<").replace("&gt;",">"))
    return myList,resList
                

def deal(filename,dataKey):
    print "[+] Dealing file (" + filename +")..."
    myList,resList = loadHtml(filename)
    outfile(filename,dataKey,myList,resList)


def outfile(filename,dataKey,myList,resList):
    '''
            host os
                vul port
                vul port

            vul solu
                host port 
                host port
    '''
    resList = sorted(resList, key=lambda x: (x['host'], x['port'], x['vul']))
    #resList = sorted(resList, key=lambda x: (x['vul'], x['host'], x['port']))
    with open(filename+"_res.txt","wb") as f:
        for res in resList:
            if pulginidDic.has_key(res['pulginid']):
                pulgin = pulginidDic[res['pulginid']]
                #f.write("||".join([res['host'],res['port'],res['os'],pulgin["risk"],pulgin["vul"],res['pulginid'],pulgin["description"],pulgin["solution"],"\r\n"]))
                f.write("  ".join([pulgin["risk"],pulgin["vul"],res['pulginid'],res['host'],res['port'],res['os'],pulgin["description"],pulgin["solution"],"\r\n"]))
            else:
                #f.write("||".join([res['host'],res['port'],res['os'],res['risk'],res['vul'],res['pulginid'],"\r\n"]))
                f.write("  ".join([res['risk'],res['vul'],res['pulginid'],res['host'],res['port'],res['os'],"\r\n"]))

def argSet(parser):
    parser.add_argument("-F", "--filename",type=str, help="Load file e.g. a.html,/tmp/test/", default=None,required=False)
    parser.add_argument("-K", "--dataKey",type=str,help='Output key e.g. Host,OS,Port', default='risk,vul,host,port,os')
    # parser.add_argument("-O", "--out",type=str,help="Output file", default=None)
    # parser.add_argument("-", "--verbose",action='store_true',help="verbose", default=False)
    return parser

def handle(args):
    filename = args.filename
    filename = './'
    # filename = args.filename
    # out = args.out
    dataKey = args.dataKey
    if dataKey not in ['vul','host']:
        dataKey = 'host'
    print "[+] Start run."
    if filename != None:
        if os.path.isfile(filename):
            deal(filename,dataKey)
        elif os.path.isdir(filename):
            print "[+] Dealing dir (" + filename +") by " +dataKey + "..."
            for myfile in os.listdir(filename) :
                if os.path.splitext(myfile)[1] == '.html':  # 排除非nessus文件
                    deal(myfile,dataKey)
        else:
            print "[+] The path is not exist!"
    else:
        print "[-] The path is not null!"
    print "[+] End of run."
        
if __name__=='__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser = argSet(parser)
    args = parser.parse_args()
    handle(args)
    
