#!/usr/bin/env python
#-*- coding:utf-8 -*-

import urllib
import urllib2
import cookielib
import valcode
from bs4 import BeautifulSoup


def login_to_xkxt(userinfo):
    #print 'test here'
    path="E:\\ValidateCode\\"
    hosturl='http://222.30.32.10'
    posturl='http://222.30.32.10/stdloginAction.do'
    headers={\
        'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded'

    }

    # 这是一个cookie处理器，它能从服务器下载cookie到本地
    # 并且在使用urllib2.Request时可以自动发送cookie
    cj=cookielib.LWPCookieJar()
    cookie_support=urllib2.HTTPCookieProcessor(cj)
    opener=urllib2.build_opener(cookie_support,urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    # 获取cookie
    request=urllib2.Request(hosturl,headers=headers)
    response = urllib2.urlopen(request)

    request=urllib2.Request("http://222.30.32.10/ValidateCode",headers=headers)
    name=path+userinfo[0]+".jpeg"
    conn=urllib2.urlopen(request)
    f=open(name,'wb')
    f.write(conn.read())
    f.close()

    code=valcode.vacode(userinfo[0])

    st = u'确 认'
    st = st.encode('gb2312')
    #print code
    postData = {
        'operation' : '',
        'usercode_text' : userinfo[0],
        'userpwd_text' : userinfo[1],
        'checkcode_text':code,
        'submittype':st
    }
    postData=urllib.urlencode(postData)
    request=urllib2.Request(posturl,postData,headers)
    response=urllib2.urlopen(request)
    text=response.read()
    text=text.decode('gb2312').encode('utf-8')

    request=urllib2.Request('http://222.30.32.10/xsxk/studiedAction.do')
    response=urllib2.urlopen(request)
    text=response.read()
    text=text.decode('gb2312').encode('utf-8')

    #f=open('E:\\ValidateCode\\'+userinfo[0]+".txt",'wb')
    #f.write(text)
    #f.close()


    #f=open("E:\\ValidateCode\\1312618.txt",'r')
    #content=f.read()

    soup = BeautifulSoup(text)

    #print(soup.prettify().replace(u'\xa0', ''))
    #print soup.find_all('tr')[2].encode('gb2312')
    s=soup.find_all('tr')[-1].encode('gb2312')
    # 编码问题，出此下策。。。。IDE的编码我也是醉了。。。。
    length=len(soup.find_all('tr'))
    #print soup.find_all('tr')[1].encode('gb2312')
    result=''
    for x in xrange(1,length-3):
        result+=soup.find_all('tr')[x].encode('gb2312')
    page=int(s[749:750])
    pages=int(s[741:742])
    for x in xrange(2,pages):
        request=urllib2.Request('http://222.30.32.10/xsxk/studiedPageAction.do?page=next')
        response=urllib2.urlopen(request)
        text=response.read()
        text=text.decode('gb2312').encode('utf-8')
        soup=BeautifulSoup(text)
        length=len(soup.find_all('tr'))
        for x in xrange(2,length-3):
            result+=soup.find_all('tr')[x].encode('gb2312')
    request=urllib2.Request('http://222.30.32.10/xsxk/studiedPageAction.do?page=next')
    response=urllib2.urlopen(request)
    text=response.read()
    text=text.decode('gb2312').encode('utf-8')
    soup=BeautifulSoup(text)
    length=len(soup.find_all('tr'))
    for x in xrange(2,length-2):
        result+=soup.find_all('tr')[x].encode('gb2312')
    print result
    result=str(result)
    f=open('E:\\ValidateCode\\'+userinfo[0]+".txt",'rb')
    content=f.read()
    f.close()
    content=str(content)
    if result==content:
        print 'it works'



if __name__=='__main__':
    a=['1312618','153542']
    login_to_xkxt(a)





