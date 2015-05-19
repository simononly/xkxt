#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import threading
from multiprocessing import Pool
import MySQLdb
import login_xkxt

def get_info():
    #以下为数据库连接信息，如果服务器是本机，请尽量不用localhost，直接使用127.0.0.1
    db=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='project')
    cursor=db.cursor()
    sql='''select stuid,xkxt from userinfo'''
    try:
        temp=cursor.execute(sql)
        db.commit()
        res=cursor.fetchmany(temp)
        listid=[str(x[-2]) for x in res]
        listpwd=[x[1] for x in res]
    except:
        db.rollback()
        print "exception: database exception, select did not work!"
        listid=[]
        listpwd=[]
    cursor.close()
    db.close()
    return listid,listpwd
#
#class multiquery(threading.Thread):
#    def __init__(self,listid,listpwd,thread_num):
#        threading.Thread.__init__(self)
#        self.listid=listid
#        self.listpwd=listpwd
#        self.thread_num=thread_num
#
def show(s):
    print s
    s=s.split('|',1)
    login_xkxt.login_to_xkxt(s)


if __name__=='__main__':
    #listid和listpwd可供扩展
    listid,listpwd=get_info()
    while len(listid)==0 and len(listpwd)==0:
        listid,listpwd==get_info()
    #转换成字符串
    listinfo=[x+'|'+y for x,y in zip(listid,listpwd)]
    #print listinfo
    pool = Pool(processes=3)
    for i in listinfo:
        result=pool.apply_async(show,(i,))
    pool.close()
    pool.join()
    print 'This mession ends! '






