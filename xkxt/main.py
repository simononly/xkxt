#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import urllib
import urllib2
import cookielib
import time
import MySQLdb
import valcode
import mail
from bs4 import BeautifulSoup
from multiprocessing import Pool


def getinfo_db():
    #以下为数据库连接信息，如果服务器是本机，请尽量不用localhost，直接使用127.0.0.1
    try:
        db=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='project')
    except:
        print "exception: database connect error, please check! "
        exit(-1)
    cursor=db.cursor()
    sql='''select stuid,xkxt,mail from userinfo'''
    try:
        temp=cursor.execute(sql)
        db.commit()
        res=cursor.fetchmany(temp)
        listid=[str(x[0]) for x in res]
        listpwd=[x[1] for x in res]
        listmail=[x[2] for x in res]
    except:
        db.rollback()
        print "exception: database exception, select did not work!"
        listid=[]
        listpwd=[]
        listmail=[]
    cursor.close()
    db.close()
    if len(listid)==0 and len(listpwd==0):
        print 'No message get from database, exit! '
        exit(-1)
    return listid,listpwd,listmail

def login(userinfo):
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
    #获取验证码
    request=urllib2.Request("http://222.30.32.10/ValidateCode",headers=headers)
    name=path+userinfo[0]+".jpeg"
    conn=urllib2.urlopen(request)
    f=open(name,'wb')
    f.write(conn.read())
    f.close()

    code=valcode.vacode(userinfo[0])

    st = u'确 认'
    st = st.encode('gb2312')
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
    #text=response.read()
    #text=text
    #print text #for debug
    request=urllib2.Request('http://222.30.32.10/stdleft.jsp')
    response=urllib2.urlopen(request)
    text=response.read()
    if len(text)==15211:
        return 1
    else:
        return 0

def get_grade(userinfo):
    request=urllib2.Request('http://222.30.32.10/xsxk/studiedAction.do')
    response=urllib2.urlopen(request)
    text=response.read()
    text=text.decode('gb2312').encode('utf-8')

    soup = BeautifulSoup(text)

    s=soup.find_all('tr')[-1].encode('gb2312')
    # 编码问题，出此下策。。。。IDE的编码我也是醉了。。。。
    length=len(soup.find_all('tr'))
    result=''
    for x in xrange(1,length-3):
        result+=soup.find_all('tr')[x].encode('gb2312')
    page=int(s[749:750])
    pages=int(s[741:742])

    if pages!=1:
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

    #print result #for debug
    result=str(result)
    path='E:\\ValidateCode\\'+userinfo[0]+".txt"
    if os.path.exists(path):
        f=open(path,'rb')
        content=f.read()
        f.close()
        content=str(content)
    else:
        content=''
    if result==content:
        print userinfo[0]+' '+'Not change'
    else:
        print userinfo[0]+' '+'change!! '
        f=open('E:\\ValidateCode\\'+userinfo[0]+".txt",'wb')
        f=f.write(result)
        maillist=[userinfo[2]]

        head='''<html>
                <head>
                <meta http-equiv="Content-Type" content="text/html; charset=gb18030" />
                </head>
                <body>
                <font size="6px" color='red'><strong>Contact admin: eling_mail at 163.com</strong></font>
                <br>Your student id is '''+userinfo[0]+'''<table boder=1>'''
        button='''
                </table>
                </body>
                </html>'''

        mail.send_mail(maillist,'成绩通知 from eling',head+result+button)
        print userinfo[0]+' mail send success! '
        f.close()



def run(userinfo):
    print userinfo
    userinfo=userinfo.split('|',2)
    timeout=3
    while timeout>0:
        if login(userinfo)==1:
            get_grade(userinfo)
            break
        else:
            timeout=timeout-1
    if timeout==0:
        print userinfo[0]+' login failed,wrong password or username!'


if __name__=='__main__':
    print 'program start at: '+time.ctime()

    listid,listpwd,listmail=getinfo_db()#listid和listpwd可供扩展

    #转换成字符串
    listinfo=[x+'|'+y+'|'+z for x,y,z in zip(listid,listpwd,listmail)]
    #print listinfo #for debug
    pool = Pool(processes=10)
    for i in listinfo:
        result=pool.apply_async(run,(i,))
    pool.close()
    pool.join()
    print 'This mession ends at: '+time.ctime()
