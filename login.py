#!/usr/bin/python
# -*- coding: utf8 -*-

import requests
from bs4 import BeautifulSoup as bs
from requests.adapters import HTTPAdapter
import ssl
from requests.packages.urllib3.poolmanager import PoolManager
class MyAdapter(HTTPAdapter):
     def init_poolmanager(self, connections, maxsize, block=False):
         self.poolmanager = PoolManager(num_pools=connections,
                                        maxsize=maxsize,
                                        block=block,
                                        ssl_version=ssl.PROTOCOL_TLSv1)

def Login(user, password):
#def Login():
    ################################type here################################
    #user = raw_input('student id:')
    #password = raw_input('password:')
    ################################type here################################
    
    
    
    session1 = requests.session()
    session1.mount('https://', MyAdapter())
    
    pre = session1.get("https://if163.aca.ntu.edu.tw/eportfolio/login.asp")
    
    pre = session1.get("https://web2.cc.ntu.edu.tw/p/s/login2/p1.php")
    cookie =  requests.utils.dict_from_cookiejar(pre.cookies)
    
    
    header = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-TW,zh;q=0.8,en;q=0.6',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Content-Length':'51',
    'Content-Type':'application/x-www-form-urlencoded',
    'Host':'web2.cc.ntu.edu.tw',
    'Origin':'https://web2.cc.ntu.edu.tw',
    'Referer':'https://web2.cc.ntu.edu.tw/p/s/login2/p1.php',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'
    }
    
    
    login = { 
    'Submit':"%E7%99%BB%E5%85%A5"
    }
    
    login['user'] = user
    login['pass'] = password
    
    res = session1.post("https://web2.cc.ntu.edu.tw/p/s/login2/p1.php",data=login,cookies=cookie,headers=header)
    res.encoding = 'big5'
    
    reg = session1.get("https://if163.aca.ntu.edu.tw/eportfolio/student/GRC.asp",cookies = requests.utils.dict_from_cookiejar(res.cookies))
    reg.encoding = 'big5'
    
    
    soup = bs(reg.text, "html.parser")
    for items in soup.find_all('a',href=True,text="進入修課檢視系統"):
        des = session1.get(items['href'])
    des.encoding = 'big5'
    
    #print des.text

    soup = bs(des.text, "html.parser")
    font = soup.select("tr")

    takenCourses =[]
    neccessaries = dict()
    grouped = []
    undone = {
    'A' : True,
    'B' : True,
    'C' : True,
    'D' : True,
    'E' : True
    }
    exp = {
    'A' : [],
    'B' : [],
    'C' : [],
    'D' : [],
    'E' : []

    }
    grouped.append([0,'指定選修']) 
    grouped.append([0,'一般選修']) 
    grouped.append([0,'通識'])  
    grouped.append([4,'體育'])      
    grouped.append([4])        #'實驗'
    grouped.append([3])        #'第F群'
    grouped.append([3])        #'第G群'
    i = 0
    flag = ''
    for a in font:
        i += 1
        flag = setflag(a.text[2:5],flag)
        #print '\n' + "NNNNNNNN  "+ str(i)  
        addto(grouped,a,flag,undone,exp)
        b = a.findAll("td")
        if len(b) == 1:
            if b[0].text[4:10] == '      ' and not b[0].text[10] == ' ': #text[4~9]
                grouped[0][0] = int(b[0].text[37:39])  #指定選修
                grouped[1][0] = int(b[0].text[48:50]) #一般選修
                grouped[2][0] = int(b[0].text[56:58]) #通識

        if len(b) == 9:
            if b[7].text == u' 未到 ' or b[7].text ==' F ' or  b[7].text == u' 停修 ':
                continue
            update(grouped,b)
            c = str(b[3].text)
            c = c.split(" ")[0]
            takenCourses.append(c)

    for typ in undone:
        if undone[typ]:
            grouped[4]+=exp[typ]
        else:
            grouped[4][0] -= 2
    if grouped[4][0] < 0:
        grouped[4][0] = 0

    

    #return takenCourses=(ID), grouped=[[學分,指定選修],[學分,一般選修],[學分,通識],[學分,體育],[學分,實驗1,...],
    #                                   [學分,實驗1,...],[學分,第F群1,...],[學分,第G群1,...]]
    return takenCourses , grouped
def update(grp , b):
    if b[0].text[1:3] == u'通識':
        grp[2][0] -= int(b[6].text)
    elif b[0].text[1:3] == u'選修' and b[8].text == u' 可當指定選修 ' and grp[0][0]>0:
        grp[0][0] -= int(b[6].text)
    elif b[0].text[1:3] == u'選修':
        grp[1][0] -= int(b[6].text)
    if b[0].text[1:3] == u'體育':
        grp[3][0] -= int(b[6].text)

    if b[0].text[1:4] == u'必修F':
        grp[5][0] -= int(b[6].text)
    elif b[0].text[1:4] == u'必修G':
        grp[6][0] -= int(b[6].text)

    for name in grp:
        if name[0]<0:
            name[0]=0
def setflag(string,flag):
    if string == u'第A群':
        return 'A'
    if string == u'第B群':
        return 'B'
    if string == u'第C群':
        return 'C'
    if string == u'第D群':
        return 'D'
    if string == u'第E群':
        return 'E'
    if string == u'第F群':
        return 'F'
    if string == u'第G群':
        return 'G'
    if string == u'第H群':
        return ''    
    return flag

def addto(grp , a, flag, undone , exp):
    if flag == '':
        return
    b = a.findAll('td')
    if a.text[2] == u'第':
        ID = str(b[1].text)
        check = b[5].text
    else:
        ID = str(b[0].text)
        check = b[4].text
    if flag == 'A' or flag == 'B' or flag == 'C' or flag == 'D' or flag == 'E':
        exp[flag].append(ID)
        if check == 'V':
            undone[flag] = False
    if flag == 'F':
        if not check == 'V':
            grp[5].append(ID)
    if flag == 'G':
        if not check == 'V':
            grp[6].append(ID)


    


    
    
#Login("b01901143","s2264")
