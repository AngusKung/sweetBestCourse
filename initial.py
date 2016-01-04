#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
#http://140.112.161.31/NTUVoxCourse/index.php/uquery/cou?DPRNDPT=9010%20&QPYEAR=100&MSLGRD=3
def Initial(user, grade):
    #user = raw_input('student id:')
    #grade = raw_input('grade:')
    
    department = user[3:6]
    
    session1 = requests.session()
    grade_int = int(grade)
    bi_show = []
    fu_shuan_bi_show = []
    while grade_int > 0:
    
        url = "http://140.112.161.31/NTUVoxCourse/index.php/uquery/cou?DPRNDPT="
        url += department + "0%20&QPYEAR=100&MSLGRD=" + str(grade_int)
        
        res = session1.get(url)
        soup = bs(res.text, "html.parser")
        table = soup.select("tr")
        i=0 
        for row in table:
            i+=1
            if i<4:
                continue
            items = row.findAll("td")
            if not len(items) == 7:
                continue
            if items[4].text=='': 
                bi_show.append(items[0].text.split(' ')[0])
            else:
            	fu_shuan_bi_show.append(items[1].text)
        grade_int -= 1
    #print "\nbi show:"
    #for item in bi_show:
    #    print item
        
        
    #print "\nfu shuan bi show:"
    #for item in fu_shuan_bi_show:
    #    print item
    return bi_show, fu_shuan_bi_show  
#Initial("b01901143","3")
