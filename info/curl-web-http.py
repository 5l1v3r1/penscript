#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'orleven'
import threading
import requests
import argparse
import sys 
import os
import platform
import chardet
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
type=sys.getfilesystemencoding()
#reload(sys)
#sys.setdefaultencoding('utf-8')
'''
    批量检测目标是否属于Web应用，并检测关键词，以及得到http请求方法
    Usage:
        python curl.py -K title -T 3 -F file.txt
        python curl.py -K status -F file.txt
        python curl.py -F file.txt -V
        python curl.py -F file.txt -S admin,管理,后台 -N 100 -V 
    目标格式:
        http://www.baidu.com
        http://192.168.1.11
        http://192.168.1.22:80
'''
#sysstr = platform.system() 
targetList = [
    "http://147.520wawa.com",
"http://19y.520wawa.com",
"http://52ly.520wawa.com",
"http://52wawa.520wawa.com",
"http://ab.520wawa.com",
"http://ababy.520wawa.com",
"http://abcyey.520wawa.com",
"http://absyyey.520wawa.com",
"http://adeyey.520wawa.com",
"http://aibao.520wawa.com",
"http://aidier.520wawa.com",
"http://aj.520wawa.com",
"http://ajyangguang.520wawa.com",
"http://ajyy.520wawa.com",
"http://ajzjh.520wawa.com",
"http://aljb.520wawa.com",
"http://amc.520wawa.com",
"http://anan.520wawa.com",
"http://ananyey.520wawa.com",
"http://andou.520wawa.com",
"http://angela.520wawa.com",
"http://angelyey.520wawa.com",
"http://angleyey.520wawa.com",
"http://aqe.520wawa.com",
"http://aqeyey.520wawa.com",
"http://arqdeyey.520wawa.com",
"http://athena.520wawa.com",
"http://ayxdfcyey.520wawa.com",
"http://ayzjzx.520wawa.com",
"http://baihe.520wawa.com",
"http://bailing.520wawa.com",
"http://bakfzx.520wawa.com",
"http://baobei.520wawa.com",
"http://bbdyyy.520wawa.com",
"http://bbt.520wawa.com",
"http://bbtzjy.520wawa.com",
"http://bbx.520wawa.com",
"http://bbyxyzy.520wawa.com",
"http://bczzx.520wawa.com",
"http://bdfsql.520wawa.com",
"http://bdfyyyey.520wawa.com",
"http://bdyey.520wawa.com",
"http://beilei.520wawa.com",
"http://bhtzy.520wawa.com",
"http://bhxcyey.520wawa.com",
"http://bhzxyey.520wawa.com",
"http://bjhoinghtyyey.520wawa.com",
"http://bjyey.520wawa.com",
"http://bjys.520wawa.com",
"http://bl.520wawa.com",
"http://blk.520wawa.com",
"http://blkbyy.520wawa.com",
"http://blkyjzx.520wawa.com",
"http://blog1.520wawa.com",
"http://bly.520wawa.com",
"http://blygyzy.520wawa.com",
"http://blzyey.520wawa.com",
"http://bnsjyey.520wawa.com",
"http://boyayoujiao.520wawa.com",
"http://bsxxts.520wawa.com",
"http://bwwyey.520wawa.com",
"http://byczhs.520wawa.com",
"http://byqxbs.520wawa.com",
"http://cahmyey.520wawa.com",
"http://cbfwyey.520wawa.com",
"http://cbwjsyg.520wawa.com",
"http://cbyey.520wawa.com",
"http://cctsjy.520wawa.com",
"http://ccyg.520wawa.com",
"http://cd22y.520wawa.com",
"http://cddwyey.520wawa.com",
"http://cdmm.520wawa.com",
"http://cdsjx.520wawa.com",
"http://cdsl.520wawa.com",
"http://cdxteyey.520wawa.com",
"http://cdxts.520wawa.com",
"http://cfjt.520wawa.com",
"http://changzheng.520wawa.com",
"http://chey.520wawa.com",
"http://chgs.520wawa.com",
"http://chjdyey.520wawa.com",
"http://chqj.520wawa.com",
"http://chunfeng.520wawa.com",
"http://chunxin.520wawa.com",
"http://chuying.520wawa.com",
"http://circle.520wawa.com",
"http://clsyyey.520wawa.com",
"http://cnyey.520wawa.com",
"http://cpsjzx.520wawa.com",
"http://cql.520wawa.com",
"http://cqtxxyyey.520wawa.com",
"http://cqyey.520wawa.com",
"http://cqyg.520wawa.com",
"http://cshy.520wawa.com",
"http://cshyyjzx.520wawa.com",
"http://csttyey.520wawa.com",
"http://csyr.520wawa.com",
"http://cx.520wawa.com",
"http://cybb.520wawa.com",
"http://cyeryou.520wawa.com",
"http://cyjy.520wawa.com",
"http://cysanyou.520wawa.com",
"http://cysiyou.520wawa.com",
"http://cyxtxyey.520wawa.com",
"http://cyyiyou.520wawa.com",
"http://dagang.520wawa.com",
"http://daxw.520wawa.com",
"http://dazhihui.520wawa.com",
"http://ddsyey.520wawa.com",
"http://ddzzxyey.520wawa.com",
"http://desyxxfs.520wawa.com",
"http://dfay.520wawa.com",
"http://dfbbsyey.520wawa.com",
"http://dfh.520wawa.com",
"http://dfj.520wawa.com",
"http://dfxhf.520wawa.com",
"http://dfzzyey.520wawa.com",
"http://dgyd.520wawa.com",
"http://dgyey.520wawa.com",
"http://dingdian.520wawa.com",
"http://dishini.520wawa.com",
"http://disi.520wawa.com",
"http://djksyey.520wawa.com",
"http://djyey.520wawa.com",
"http://dlc.520wawa.com",
"http://dlyey.520wawa.com",
"http://dlyg.520wawa.com",
"http://dlyggj.520wawa.com",
"http://dlysyey.520wawa.com",
"http://dlzctyey.520wawa.com",
"http://dongcheng.520wawa.com",
"http://dongfang.520wawa.com",
"http://dpygbbyey.520wawa.com",
"http://dqbb.520wawa.com",
"http://dqqqyzy.520wawa.com",
"http://dsbyey.520wawa.com",
"http://dseyey.520wawa.com",
"http://dshc.520wawa.com",
"http://dssyxx.520wawa.com",
"http://dszdsyey.520wawa.com",
"http://dthty.520wawa.com",
"http://dtyoyo.520wawa.com",
"http://dtyxyey.520wawa.com",
"http://dtztyzx.520wawa.com",
"http://dwjsyey.520wawa.com",
"http://dx.520wawa.com",
"http://dxfx.520wawa.com",
"http://dyhm.520wawa.com",
"http://dyljzxyey.520wawa.com",
"http://dyxsyyey.520wawa.com",
"http://dzdfc.520wawa.com",
"http://dzhty.520wawa.com",
"http://dzsbgsyey.520wawa.com",
"http://dzsy.520wawa.com",
"http://dzxlg.520wawa.com",
"http://ep.520wawa.com",
"http://essyxxyey.520wawa.com",
"http://eszycyey.520wawa.com",
"http://fct.520wawa.com",
"http://fdyfy.520wawa.com",
"http://fjsgsy.520wawa.com",
"http://fjsjyey.520wawa.com",
"http://flyyey.520wawa.com",
"http://frqygyey.520wawa.com",
"http://fsygyey.520wawa.com",
"http://fuguilu.520wawa.com",
"http://fxzl.520wawa.com",
"http://gchzyey.520wawa.com",
"http://gclyey.520wawa.com",
"http://gdyey.520wawa.com",
"http://gdzxyey.520wawa.com",
"http://gfqzzx.520wawa.com",
"http://ggzxbl.520wawa.com",
"http://gjyey.520wawa.com",
"http://gkzzxyey.520wawa.com",
"http://gl2y.520wawa.com",
"http://glxcyey.520wawa.com",
"http://glzxyey.520wawa.com",
"http://glzzxyey.520wawa.com",
"http://gmbyy.520wawa.com",
"http://gnxqmyey.520wawa.com",
"http://gxqzdsy.520wawa.com",
"http://gxsdggyey.520wawa.com",
"http://gxsygyey.520wawa.com",
"http://gxym.520wawa.com",
"http://gxymyey.520wawa.com",
"http://gy.520wawa.com",
"http://gyxxyey.520wawa.com",
"http://gzxxyey.520wawa.com",
"http://gzxyyey.520wawa.com",
"http://gzygbbyey.520wawa.com",
"http://haimeiyey.520wawa.com",
"http://hangt.520wawa.com",
"http://hanting.520wawa.com",
"http://hanwang.520wawa.com",
"http://hcqzhyey.520wawa.com",
"http://hcxsyyey.520wawa.com",
"http://hdyyyey.520wawa.com",
"http://heao.520wawa.com",
"http://hedd.520wawa.com",
"http://heddyey.520wawa.com",
"http://heddyy.520wawa.com",
"http://hengcun.520wawa.com",
"http://hengcunyey.520wawa.com",
"http://hhl.520wawa.com",
"http://hhlyery.520wawa.com",
"http://hhlyzy.520wawa.com",
"http://hhyey.520wawa.com",
"http://hhzsyyey.520wawa.com",
"http://hhzyey.520wawa.com",
"http://hhzys.520wawa.com",
"http://hj.520wawa.com",
"http://hjsqzxyey.520wawa.com",
"http://hjyey.520wawa.com",
"http://hlb.520wawa.com",
"http://hldwhhc.520wawa.com",
"http://hlhty.520wawa.com",
"http://hljtyey.520wawa.com",
"http://hljyey.520wawa.com",
"http://hll.520wawa.com",
"http://hlyey.520wawa.com",
"http://hmbyey.520wawa.com",
"http://hmxygyey.520wawa.com",
"http://hmyey.520wawa.com",
"http://hnisc.520wawa.com",
"http://hnmy.520wawa.com",
"http://hongqi.520wawa.com",
"http://hqyzyey.520wawa.com",
"http://hsyey.520wawa.com",
"http://htlf.520wawa.com",
"http://hty.520wawa.com",
"http://htyyey.520wawa.com",
"http://huangjia.520wawa.com",
"http://huaqing.520wawa.com",
"http://huayu.520wawa.com",
"http://hxayrazj.520wawa.com",
"http://hxayzjzx.520wawa.com",
"http://hxwl.520wawa.com",
"http://hyqzzx.520wawa.com",
"http://hzdcyey.520wawa.com",
"http://hzdgyey.520wawa.com",
"http://hzhedd.520wawa.com",
"http://hzsxtsyey.520wawa.com",
"http://hzsyhyey.520wawa.com",
"http://hzxbs.520wawa.com",
"http://hzxy.520wawa.com",
"http://hzxyyy.520wawa.com",
"http://hzy.520wawa.com",
"http://hzyumiao.520wawa.com",
"http://jbb.520wawa.com",
"http://jbbpgyzy.520wawa.com",
"http://jbl.520wawa.com",
"http://jcbyey.520wawa.com",
"http://jchyyey.520wawa.com",
"http://jdc.520wawa.com",
"http://jdsygyey.520wawa.com",
"http://jdxpyey.520wawa.com",
"http://jfhmyey.520wawa.com",
"http://jfyg.520wawa.com",
"http://jgdy.520wawa.com",
"http://jiananmeidibaobei.520wawa.com",
"http://jiaoyu.520wawa.com",
"http://jinbaobei.520wawa.com",
"http://jinbeilei.520wawa.com",
"http://jingjing.520wawa.com",
"http://jingqiaoyey.520wawa.com",
"http://jinhaigui.520wawa.com",
"http://jinlb.520wawa.com",
"http://jinri.520wawa.com",
"http://jinseyg.520wawa.com",
"http://jinsha.520wawa.com",
"http://jintong.520wawa.com",
"http://jinyangguang.520wawa.com",
"http://jinyaoshi.520wawa.com",
"http://jjnyey.520wawa.com",
"http://jjsxx.520wawa.com",
"http://jl.520wawa.com",
"http://jlhty.520wawa.com",
"http://jlhyey.520wawa.com",
"http://jlqtz.520wawa.com",
"http://jlyey.520wawa.com",
"http://jmyey.520wawa.com",
"http://jn2yey.520wawa.com",
"http://jnzzxyey.520wawa.com",
"http://jpgyey.520wawa.com",
"http://jqjgey.520wawa.com",
"http://js.520wawa.com",
"http://jsjdq.520wawa.com",
"http://jsqx.520wawa.com",
"http://jssnqyey.520wawa.com",
"http://jstn.520wawa.com",
"http://jsxygyey.520wawa.com",
"http://jsyg.520wawa.com",
"http://jsygsy.520wawa.com",
"http://jsygyey.520wawa.com",
"http://jsylyey.520wawa.com",
"http://jsyy.520wawa.com",
"http://jtnyey.520wawa.com",
"http://jtys.520wawa.com",
"http://jtyzy.520wawa.com",
"http://junyiyey.520wawa.com",
"http://jwyey.520wawa.com",
"http://jxsgsyjyey.520wawa.com",
"http://jxxinlei.520wawa.com",
"http://jxy.520wawa.com",
"http://jxyey.520wawa.com",
"http://jygyey.520wawa.com",
"http://jyjdeyey.520wawa.com",
"http://jyjyey.520wawa.com",
"http://jys.520wawa.com",
"http://jysjgyey.520wawa.com",
"http://jysyery.520wawa.com",
"http://jyxty.520wawa.com",
"http://jyyc.520wawa.com",
"http://jyzxyey.520wawa.com",
"http://jz.520wawa.com",
"http://jzdfc.520wawa.com",
"http://jzllyey.520wawa.com",
"http://jzsyyey.520wawa.com",
"http://jzygyey.520wawa.com",
"http://kangyi.520wawa.com",
"http://kblktyzy.520wawa.com",
"http://ketyey.520wawa.com",
"http://kjxjbbyey.520wawa.com",
"http://kl.520wawa.com",
"http://klmyzx.520wawa.com",
"http://klqh.520wawa.com",
"http://klx.520wawa.com",
"http://klyg.520wawa.com",
"http://knyey.520wawa.com",
"http://kqzxyey.520wawa.com",
"http://ksjsyg.520wawa.com",
"http://ksyey.520wawa.com",
"http://kxceryou.520wawa.com",
"http://kzyey.520wawa.com",
"http://kzzqyey.520wawa.com",
"http://langh.520wawa.com",
"http://lantianyey.520wawa.com",
"http://laxjl.520wawa.com",
"http://lcdfc.520wawa.com",
"http://lchyyey.520wawa.com",
"http://lclt.520wawa.com",
"http://lcwht.520wawa.com",
"http://lczxyey.520wawa.com",
"http://ldjpg.520wawa.com",
"http://ldxxyey.520wawa.com",
"http://lele.520wawa.com",
"http://lgdsyey.520wawa.com",
"http://lgdxyey.520wawa.com",
"http://lgyeyzj.520wawa.com",
"http://lhbb.520wawa.com",
"http://lhxyey.520wawa.com",
"http://lhyj.520wawa.com",
"http://lijia.520wawa.com",
"http://ljlyey.520wawa.com",
"http://ljzxyey.520wawa.com",
"http://lls.520wawa.com",
"http://lpzzx.520wawa.com",
"http://lqsa.520wawa.com",
"http://lssjyey.520wawa.com",
"http://lsxjtyey.520wawa.com",
"http://ltyb.520wawa.com",
"http://ltzxyey.520wawa.com",
"http://luzhiboya.520wawa.com",
"http://lwdeyey.520wawa.com",
"http://lwqqy.520wawa.com",
"http://lxhyey.520wawa.com",
"http://lxjgyey.520wawa.com",
"http://lxsyey.520wawa.com",
"http://lxyj.520wawa.com",
"http://lxzygyey.520wawa.com",
"http://lycx.520wawa.com",
"http://lynlw.520wawa.com",
"http://lyqyey.520wawa.com",
"http://lyygyey.520wawa.com",
"http://mdlsun.520wawa.com",
"http://mfcbyey.520wawa.com",
"http://mimiyey.520wawa.com",
"http://mjo.520wawa.com",
"http://mlqygsyy.520wawa.com",
"http://mlw.520wawa.com",
"http://mmys.520wawa.com",
"http://mrzxyey.520wawa.com",
"http://mszzxyey.520wawa.com",
"http://mtgcyey.520wawa.com",
"http://mtslsyyey.520wawa.com",
"http://mxd.520wawa.com",
"http://mxg.520wawa.com",
"http://mxxsyyey.520wawa.com",
"http://mxygyey.520wawa.com",
"http://myxhs.520wawa.com",
"http://myyery.520wawa.com",
"http://mzy.520wawa.com",
"http://mzyey.520wawa.com",
"http://nanbo.520wawa.com",
"http://nanjieyey.520wawa.com",
"http://nbkjyey.520wawa.com",
"http://ncyd.520wawa.com",
"http://newbridge.520wawa.com",
"http://ngcshy.520wawa.com",
"http://nhxsyyey.520wawa.com",
"http://njrjlyey.520wawa.com",
"http://njtx.520wawa.com",
"http://njygysyey.520wawa.com",
"http://nksy.520wawa.com",
"http://nkzxyey.520wawa.com",
"http://nldfcyey.520wawa.com",
"http://nldfczj.520wawa.com",
"http://nnjbb.520wawa.com",
"http://nsjfyey.520wawa.com",
"http://osmc.520wawa.com",
"http://ozhyyey.520wawa.com",
"http://pbxjbl.520wawa.com",
"http://pdsxtsyey.520wawa.com",
"http://pengzhou.520wawa.com",
"http://pjxsj.520wawa.com",
"http://pkcd.520wawa.com",
"http://pkxsjyey.520wawa.com",
"http://pwcyey.520wawa.com",
"http://pxjcy.520wawa.com",
"http://pxjg.520wawa.com",
"http://pxtyn.520wawa.com",
"http://pxyg.520wawa.com",
"http://py.520wawa.com",
"http://qcygyey.520wawa.com",
"http://qdxbh.520wawa.com",
"http://qhbb.520wawa.com",
"http://qhjgyey.520wawa.com",
"http://qhtzxyey.520wawa.com",
"http://qingan.520wawa.com",
"http://qinqin.520wawa.com",
"http://qiya.520wawa.com",
"http://qiyi.520wawa.com",
"http://qjfzyey.520wawa.com",
"http://qjmmyey.520wawa.com",
"http://qjsyyey.520wawa.com",
"http://qlpyey.520wawa.com",
"http://qmyey.520wawa.com",
"http://qmz.520wawa.com",
"http://qqb.520wawa.com",
"http://qqbaby.520wawa.com",
"http://qqc.520wawa.com",
"http://qsyg.520wawa.com",
"http://qwyey.520wawa.com",
"http://qydeyey.520wawa.com",
"http://qydyyey.520wawa.com",
"http://qyl.520wawa.com",
"http://qymzbs.520wawa.com",
"http://qzssyyey.520wawa.com",
"http://rjgj.520wawa.com",
"http://ruanshe.520wawa.com",
"http://ryyey.520wawa.com",
"http://sdsz.520wawa.com",
"http://sdwjyey.520wawa.com",
"http://sf.520wawa.com",
"http://sfjykt.520wawa.com",
"http://sghtyyey.520wawa.com",
"http://sgy.520wawa.com",
"http://sgzygsy.520wawa.com",
"http://sh.520wawa.com",
"http://shidai.520wawa.com",
"http://shuiguolanzi.520wawa.com",
"http://shuiyue.520wawa.com",
"http://shxt.520wawa.com",
"http://shzggyey.520wawa.com",
"http://sijie.520wawa.com",
"http://siyuan.520wawa.com",
"http://sjzg.520wawa.com",
"http://sjzx.520wawa.com",
"http://skpld.520wawa.com",
"http://slxsy.520wawa.com",
"http://slxtsyey.520wawa.com",
"http://slyzy.520wawa.com",
"http://smxblyey.520wawa.com",
"http://snjt.520wawa.com",
"http://sszzxyey.520wawa.com",
"http://stg.520wawa.com",
"http://supo.520wawa.com",
"http://swyey.520wawa.com",
"http://sxmdyey.520wawa.com",
"http://sxsjzx.520wawa.com",
"http://sxxl.520wawa.com",
"http://sxxlyey.520wawa.com",
"http://syyey.520wawa.com",
"http://syyg.520wawa.com",
"http://syyhysyey.520wawa.com",
"http://szbowen.520wawa.com",
"http://szfubaby.520wawa.com",
"http://szfyyey.520wawa.com",
"http://szsfc.520wawa.com",
"http://szsqlyghy.520wawa.com",
"http://sztianle.520wawa.com",
"http://tcsy.520wawa.com",
"http://tfxqxl.520wawa.com",
"http://tfytes.520wawa.com",
"http://thsj.520wawa.com",
"http://thyey.520wawa.com",
"http://tianhe.520wawa.com",
"http://tianhongyey.520wawa.com",
]
resultDic = {}
threadList = []
resultList = []
def _curl(target,i,timeout=3,searchList=[]):
    dic = {}
    dic['id'] = str(i)
    dic['search'] = []
    dic['host'] = target.split(':')[0].strip('https://').strip('http://')
    url = target.strip(' ')
    try:
        
        result = requests.get(url, timeout=int(timeout),verify=False)
        soup = BeautifulSoup(result.text, "html5lib")
        dic['target'] = url
        dic['status'] = str(result.status_code)
        dic['flag'] = True
        dic['host'] = target
        mytitle =  soup.title.string
        content =  result.text
        for searchkey in searchList:
            if searchkey in mytitle.encode(result.encoding).decode('utf-8').encode(type) or searchkey in content.encode(result.encoding).decode('utf-8').encode(type):
                #print searchkey,mytitle.encode(result.encoding).decode('utf-8').encode(type)
                dic['search'].append(searchkey)
        if mytitle == None or mytitle =='':
            dic['title'] = "None Title"
        else:
            dic['title'] =  mytitle.encode(result.encoding)
        code = chardet.detect(title)['encoding'] if chardet.detect(title)['encoding'] not in ['ISO-8859-5','KOI8-R','IBM855'] else 'gbk'
        # print(title.decode(code)+":"+code)
        mytitle = title.decode(code).strip().replace("\r","").replace("\n","")
    except:
        dic['title'] = "Curl Failed"
        dic['status'] = "0"
        dic['target'] = target
        dic['host'] = target
        dic['flag'] = False
    url = target.strip(' ')
    try:
        result1 = requests.options(url+"/testbyah", timeout=int(timeout))
        dic['head_allow'] = result1.headers['Allow']
    except:
        dic['head_allow'] = "Not Allow"
    return dic

def curl(threadId,timeout,threadNum,verbose,searchList):
    for i in xrange(threadId,len(targetList),threadNum):
        dic = _curl(targetList[i],i,timeout,searchList)
        resultList.append(dic)
        if verbose and  dic['status'] !="0" :
            if chardet.detect(dic['title'])['encoding'].lower()=='utf-8':    
                title = dic['title'].decode('utf-8').encode(type)
            else:
                title =  dic['title']
            try:
                print "[%s]\t%s\t%s\t%s\t%s" % (dic['id'],dic['target'],dic['status'],title,','.join(dic['search'])),
            except:
                print "[%s]\t%s\t%s\t%s\t%s" % (dic['id'],dic['target'],dic['status'],"Title Code Error",','.join(dic['search'])),
def scan(threadNum,timeout,verbose,searchList):
    print "[.] Run start: Total " + str(len(targetList)) + " request!"
    for threadId in xrange(0,threadNum):
        t = threading.Thread(target=curl,args=(threadId,timeout,threadNum,verbose,searchList,))
        t.start()
        threadList.append(t)
    for num in xrange(0,threadNum):
        threadList[num].join()
    print "\r\n[.] Run over!"

def printlog(key,out):
    print "=================== Order by " + key + " ======================="
    print "[.] Start to output!"
    resList =  sorted(resultList,key = lambda e:e.__getitem__(key))
    temp = "NoNasdon!asd32@NoneNone"
    
    if out!=None:
        with open(out,'wb') as f :
            for value in resList:
                if chardet.detect(value['title'])['encoding'].lower()=='utf-8':    
                    title = value['title'].decode('utf-8').encode(type)
                else:
                    title =  value['title']
                if temp != value[key] and key != 'id' :
                    try:
                        f.write("\r\n["+title+"]\r\n")
                    except:
                        f.write("\r\n[Title Code Error]\r\n")
                try:
                    f.write("[%s]\t[%s]\t%s\t%s\t%s\t%s\r\n" % (value['id'],value['status'],value['target'],value['head_allow'],title,','.join(value['search'])))
                except:                
                    f.write("[%s]\t[%s]\t%s\t%s\t%s\t%s\r\n" % (value['id'],value['status'],value['target'],value['head_allow'],"[Title Code Error]",','.join(value['search'])))
                temp = value[key]
        print "[.] Save result into "+ out + "!"
    else:
        for value in resList:
            if chardet.detect(value['title'])['encoding'].lower()=='utf-8':    
                title = value['title'].decode('utf-8').encode(type)
            else:
                title =  value['title']
            if temp != value[key] and key != 'id' :
                try:
                    print "\r\n["+title+"]"
                except:
                    print "\r\n[Title Code Error]"
            try:
                print "[%s]\t[%s]\t%s\t%s\t%s\t%s" % (value['id'],value['status'],value['target'],value['head_allow'],title,','.join(value['search']))
            except :
                print "[%s]\t[%s]\t%s\t%s\t%s\t%s" % (value['id'],value['status'],value['target'],value['head_allow'],"[Title Code Error]",','.join(value['search']))
            temp = value[key]
    print "[.] End output!"
    print "======================================================="

def argSet(parser):
    parser.add_argument("-K", "--key", type=str, help="The order key e.g. title、status、host", default="id")
    parser.add_argument("-T", "--timeout", type=str, help="Timeout", default="3")
    parser.add_argument("-F", "--file",type=str, help="Load ip dictionary e.g. 192.168.1.2:8080", default=None)
    parser.add_argument("-V", "--verbose",action='store_true',help="verbose", default=False)
    parser.add_argument("-O", "--out",type=str, help="output file e.g res.txt", default=None)
    parser.add_argument("-S", "--search",type=str, help="search key in title or content,e.g. 管理,后台", default=None)
    parser.add_argument("-N", "--threadnum",type=int, help="Thread Num e.g. 10", default=10)
    return parser


def handle(args):
    key = args.key
    timeout = args.timeout
    filename = args.file
    out = args.out
    threadnum = args.threadnum
    verbose = args.verbose
    search = args.search
    searchList = []
    if search!=None:
        searchList=search.split(',')
    if key not in ['title','status','host','head_allow','id','search']:
        key = 'id'
    if filename != None:
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                for line in f.readlines():
                    myline = line.strip('\n').strip('\r')
                    targetList.append(myline)
        else:
            print "[-] The path is not exist!"
    scan(threadnum,timeout,verbose,searchList)
    printlog(key,out)

if __name__=='__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser = argSet(parser)
    args = parser.parse_args()
    handle(args)




