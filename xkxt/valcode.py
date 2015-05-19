#!/usr/bin/env python
#-*- coding:utf-8 -*-
from PIL import Image
import Image,ImageEnhance,ImageFilter

def image_to_char(img):
    #这个函数可以把二值化以后的图片转化为一个字符，返回值为字符
    result=0#最大的匹配数
    char='1'#初始化结果，如果没有识别出来，将结果置为1
    for z in xrange(10):
        score=0
        imgstd=Image.open('E:\\ValidateCode\\standard\\' +str(z)+  '.gif')#标准字模
        imgstd=imgstd.convert("RGBA")#进行RGBA解析
        datastd=imgstd.load()
        data=img.load()
        for x in xrange(img.size[0]-imgstd.size[0]+1):#但需要识别的图片比标准大时，进行遍历识别，如果比标准小，为减少运算，放弃识别。
            #可以改进
            for y in xrange(img.size[1]-imgstd.size[1]+1):
                score_temp=0
                for xx in xrange(imgstd.size[0]):
                    for yy in xrange(imgstd.size[1]):
                        if(datastd[xx,yy]==data[xx+x,yy+y]):
                            score_temp=score_temp+1
                if(score_temp>score):
                    score=score_temp
        if(score>result):
            result=score
            char=str(z)
    return char

def vacode(id):
    img = Image.open('E:\\ValidateCode\\' +id + '.jpeg')
    img = img.convert("RGBA")
    pixdata = img.load()
    #以下代码进行RGB二值化，我又造轮子了是吧，嗯，我就知道。
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][0] < 100:
                pixdata[x, y] = (0, 0, 0, 255)
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][1] < 165:
                pixdata[x, y] = (0, 0, 0, 255)
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][2] > 0:
                pixdata[x, y] = (255, 255, 255, 255)
    #以下进行单个点的识别并去除。
    for y in xrange(1,img.size[1]-1):
        for x in xrange(1,img.size[0]-1):
            if pixdata[x,y]==(0,0,0,255):
                if pixdata[x-1,y]==(0,0,0,255):continue
                if pixdata[x-1,y-1]==(0,0,0,255):continue
                if pixdata[x-1,y+1]==(0,0,0,255):continue
                if pixdata[x,y-1]==(0,0,0,255):continue
                if pixdata[x,y+1]==(0,0,0,255):continue
                if pixdata[x+1,y+1]==(0,0,0,255):continue
                if pixdata[x+1,y]==(0,0,0,255):continue
                if pixdata[x+1,y-1]==(0,0,0,255):continue
                pixdata[x,y]=(255,255,255,255)
    #以下分割各个字符，如果连在一起，摊手，无法识别，我也知道没什么技术含量。。。。。对图片处理不熟悉。。。。
    current=0
    listx=[]#存储颜色改变时的x坐标
    for x in xrange(img.size[0]):
        color=0
        for y in xrange(img.size[1]):
            if pixdata[x,y]==(0,0,0,255):color=1
        if(current==0 and color==1):
            listx.append(x)
            current=1
        if(current==1 and color==0):
            listx.append(x)
            current=0
    #如果两个字符连在一起，摊手摊手，返回吧。。。无法识别
    if(listx.__sizeof__()%2!=0):return ''
    listy=[]#存储y轴上黑色开始的位置，没错，就是用投影把大块空白去掉。
    for z in xrange(4):
        start=listx[z*2]
        end=listx[z*2+1]
        flag=0
        for y in xrange(img.size[1]):
            if(flag==0):
                for x in xrange(start,end):
                    if pixdata[x,y]==(0,0,0,255):
                        listy.append(y)
                        flag=1
                        break
            else:break
        flag=0
        for y in xrange(img.size[1]):
            if(flag==0):
                for x in xrange(start,end):
                    if pixdata[x,img.size[1]-y-1]==(0,0,0,255):
                        listy.append(img.size[1]-y-1)
                        flag=1
                        break
            else:break
    img1=img.crop((listx[0],listy[0],listx[1],listy[1]+1))
    img2=img.crop((listx[2],listy[2],listx[3],listy[3]+1))
    img3=img.crop((listx[4],listy[4],listx[5],listy[5]+1))
    img4=img.crop((listx[6],listy[6],listx[7],listy[7]+1))
    return image_to_char(img1)+image_to_char(img2)+image_to_char(img3)+image_to_char(img4)
