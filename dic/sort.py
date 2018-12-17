#! /usr/python
# coding:utf-8
__author__ = 'leven'
import re
'''
字典排序去重
'''
with open('chinaUser2.txt', 'rb') as f1, open('chinaUser_2.txt', 'wb')as f2:
    dics = {}
    for line in f1.readlines():
        text = line.replace('\r','').replace('\n','')
        dics[text]=1
        #lis = re.split('\|\|',text)
        #if lis[0] not in dics:
             #dics[lis[0]] = ""
        #if lis[1] not in dics[lis[0]]:
            #dics[lis[0]]+=lis[1]+":" + lis[4]+"!"

            
        #if lis[1] not in dics[lis[0]]:
            #print lis[0]+"---"+ lis[2]
            #dics[lis[0]+"---"+ lis[2]]+=lis[1]+"::"+""+lis[4]
            #print lis[0]
            #dics[lis[0]]=lis[2]
            
        #temptext =  re.search(r'(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|[0-9])(?:\.(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|[0-9])){3}',text)
        #if temptext != None:
        #    ip = temptext.group()
        #    if line[:len(ip)] not in dics:
        #        dics[line[:len(ip)]] = ""
        #    dics[line[:len(ip)]]+=line[len(ip):]
        #    #print line[:len(ip)],dics[line[:len(ip)]]
    #dics = {"Ddd":1,"b":1,"a":2,"vvv":1}
    dicst = sorted(dics.iteritems(), key=lambda e:e[0], reverse=False)
    #print dicst
    for key in dicst:
        f2.write(key[0]+"\r\n")
       #f2.write(key+"---"+dicst[key]+"\r\n")
    

