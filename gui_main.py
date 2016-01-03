#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os   
import collections
import Tkinter as tkinter
from tktable import *
from initial import *
from login import *
from util import *
import State
import Course
from operator import itemgetter
import pdb

class GUI:
    def __init__(self):
        self.bi_show = []
        self.fu_shuan_bi_show = []
        self.class_time = []
        self.current_state = []
        self.courses, self.general_courses, self.PE_courses = readCoursePickle()
        self.EmptyState = State.State()
        self.InitialState = State.State()
        self.nextState = self.InitialState.copy()
        self.total_score = 1
        
    def test_cmd(self, event):
        if event.i == 0:
            return '%i, %i' % (event.r, event.c)
        else:
            return 'set'

    def browsecmd(self, event):
        print("event:", event.__dict__)
        print("curselection:", self.test.curselection())
        print("active cell index:", self.test.index('active'))
        print("active:", self.test.index('active', 'row'))
        print("anchor:", self.test.index('anchor', 'row'))
        b_index = self.test.index('active')
        course_name = self.var[b_index]
        for i in range(len(self.current_state)):
            if course_name == self.current_state[i][0]:
                self.current_state.pop(i)
                break
        for x in range(0,6):
            for y in range(0,15):
                index = "%i,%i" % (y, x)
                try:
                    if course_name == self.var[index]:
                        self.var[index] = ""
                except:
                    pass
        
    def initVar(self):
        self.root = tkinter.Tk()
        self.var = ArrayVar(self.root)
        for y in range(-1, 15):
            index = "%i,%i" % (y, -1)
            self.var[index] = index
            if y == -1:
                self.var[index] = ""
            elif 0 <= y <= 10:
                self.var[index] = y
            else:
                self.var[index] = chr(54+y)
        for x in range(-1,6):
            index = "%i,%i" % (-1, x)
            self.var[index] = index
            if x == -1:  self.var[index] = ""
            elif x == 0: self.var[index] = "ㄧ"
            elif x == 1: self.var[index] = "二"
            elif x == 2: self.var[index] = "三"
            elif x == 3: self.var[index] = "四"
            elif x == 4: self.var[index] = "五"
            elif x == 5: self.var[index] = "六"

    def clearVar(self):
        for y in range(0, 15):
            for x in range(0, 6):
                index = "%i,%i" % (y, x)
                self.var[index] = ""
           
    def loginMethod(self):
        print "Logging..."
        self.bi_show, self.fu_shuan_bi_show = Initial(self.user_field.get(), self.grade_field.get())
        self.takenCourses,toGraduate_unorderd = Login(self.user_field.get(), self.pswd_field.get())
        self.InitialState.setPersonDepart("EE")
        exceptions = ['EE4049']
        self.ruleOutTaken(exceptions) #rule out the taken classes
        # --- customize courses ---
        self.depart_courses = []
        self.non_depart_courses = []
        for course in self.courses:
            if self.InitialState.personDepart in course.ID and len(course.ID)==6:
                self.depart_courses.append(course)
            else:
                self.non_depart_courses.append(course)
        self.InitialState.setCategorizedCourses(self.depart_courses,self.non_depart_courses,self.general_courses,self.PE_courses)
        del self.depart_courses, self.non_depart_courses, self.general_courses, self.PE_courses, self.courses
        # --- deal with personal toGraduate ---
        self.toGraduate = [0]#必修
        self.toGraduate.append(toGraduate_unorderd[4:])
        self.toGraduate.append(toGraduate_unorderd[0][0])#系上選修
        self.toGraduate.append(toGraduate_unorderd[1][0])
        self.toGraduate.append(toGraduate_unorderd[2][0])
        self.toGraduate.append(toGraduate_unorderd[3][0])
        self.InitialState.setLoadingLimit(50.0)
        self.InitialState.setPersonDistrib(self.toGraduate)
        self.InitialState.transformID()
        self.nextState = self.InitialState.copy()
        self.nextState.setLoadingLimit(self.load_scale.get()) 
        #print self.toGraduate
        #self.bi_show.append(self.fu_shuan_bi_show[0])通識
        #self.to_show = [course for course in self.bi_show if course not in self.takenCourses]
        #self.updateBishow2Table(self.to_show)
        
    def updateBishow2Table(self, bi_show):
        sweety_dict = readSweetyCsv()
        for item in bi_show:
            for time in sweety_dict[item][0][4].split(" ")[ :-1]:
                self.current_state.append(sweety_dict[item])
                self.updateTable([time, item])

    def updateTable(self, time):
        #time[0] = time, time[0][1] = class time, time[0][0] = weekdays
        #time[1] = course name
        index = "%i,%i" % (int(time[0][1]), (int(ord(time[0][0])-65)))
        value = time[1]
        self.var[index] = time[1]
        
    def loadMethod(self):
        '''
        course = (name,teache)
        if self.nextState.canTake(course):
        self.nextState.generateSuccessor(course)
        try:
            self.toGraduate.append(str(self.load_field.get()).upper())
            print "Course %s loaded" % str(self.load_field.get()).upper()
        except:
            print "Please loggin first!"
        '''

    def searchMethod(self):
        self.credit_limit = self.credit_scale.get()
        self.nextState = self.InitialState.copy()
        self.clearVar()
        self.nextState.setLoadingLimit(self.load_scale.get())
        courseCount = 0
        while(self.nextState.credit <= self.credit_limit):
            trialState = self.nextState.greedySearch()
            if not trialState:
                print "Fininshed optimzed greedy!"
                print courseCount,"courses added !!!"
                print "Course taken:"
                for t in self.nextState.taken:
                    print t
                break
            else:
                courseCount += 1
                self.nextState = trialState
        for c in self.nextState.taken:
            for t in c.time:
                index = "%i,%i" % (int(t[1]), (int(ord(t[0])-65)))
                self.var[index] = c.name
        print "Loading =",self.nextState.loading, "while loading_limit =",self.nextState.loading_limit

    def updateScore(self):
        self.total_score = int(self.shibi_spin.get()) + int(self.shish_spin.get()) + \
                           int(self.shush_spin.get()) + int(self.tonsh_spin.get()) + int(self.sport_spin.get())
        self.shibi_spin.config(to=(40-self.total_score))
        self.shish_spin.config(to=(40-self.total_score))
        self.shush_spin.config(to=(40-self.total_score))
        self.tonsh_spin.config(to=(40-self.total_score))
        self.sport_spin.config(to=(40-self.total_score))
        if self.total_score >= 20:
            self.shibi_spin.config(to=self.shibi_spin.get())
            self.shish_spin.config(to=self.shish_spin.get())
            self.shush_spin.config(to=self.shush_spin.get())
            self.tonsh_spin.config(to=self.tonsh_spin.get())
            self.sport_spin.config(to=self.sport_spin.get())
        self.score_label.config(text="能力點數：%i" % (20-self.total_score))
        print self.total_score

    def ruleOutTaken(self,exceptions):
        flag=0
        for taken in self.takenCourses:
            if taken in exceptions: #add exceptions here
                continue
            for c in self.courses:
                if taken==c.ID:
                    print c
                    self.courses.remove(c)
                    flag=1
            for c in self.general_courses:
                if taken==c.ID:
                    print c
                    self.general_courses.remove(c)
                    flag=1
            for c in self.PE_courses:
                if taken==c.ID:
                    print c
                    self.PE_courses.remove(c)
                    flag=1
            if flag!=1:
                print "!!! Can't find:",taken

    def createTable(self):
        self.user_label = tkinter.Label(self.root, text="帳號：")
        self.user_label.grid(row=0, column=0)
        self.user_field = tkinter.Entry(self.root, width=15)
        self.user_field.grid(row=0, column=1, columnspan=3)
    
        self.pswd_label = tkinter.Label(self.root, text="密碼：")
        self.pswd_label.grid(row=1, column=0)
        self.pswd_field = tkinter.Entry(self.root, width=15, show="*")
        self.pswd_field.grid(row=1, column=1, columnspan=3)

        self.grade_label = tkinter.Label(self.root, text="年級：")
        self.grade_label.grid(row=2, column=0)
        self.grade_field = tkinter.Entry(self.root, width=15)
        self.grade_field.grid(row=2, column=1, columnspan=3)

        self.load_label = tkinter.Label(self.root, text="帶入課號：")
        self.load_label.grid(row=3, column=0)
        self.load_field = tkinter.Entry(self.root, width=20)
        self.load_field.grid(row=3, column=1, columnspan=3)
        self.load_button = tkinter.Button(self.root, text="帶入", command=self.loadMethod)
        self.load_button.grid(row=3, column=4)

        self.shibi_label = tkinter.Label(self.root, text="系必")
        self.shibi_label.grid(row=4, column=0)
        self.shibi_spin = tkinter.Spinbox(self.root, from_=0, to=self.total_score, command=self.updateScore, width=4)
        self.shibi_spin.grid(row=5, column=0)

        self.shish_label = tkinter.Label(self.root, text="系選")
        self.shish_label.grid(row=4, column=1)
        self.shish_spin = tkinter.Spinbox(self.root, from_=0, to=self.total_score, command=self.updateScore, width=4)
        self.shish_spin.grid(row=5, column=1)

        self.shush_label = tkinter.Label(self.root, text="選修")
        self.shush_label.grid(row=4, column=2)
        self.shush_spin = tkinter.Spinbox(self.root, from_=0, to=self.total_score, command=self.updateScore, width=4)
        self.shush_spin.grid(row=5, column=2)

        self.tonsh_label = tkinter.Label(self.root, text="通識")
        self.tonsh_label.grid(row=4, column=3)
        self.tonsh_spin = tkinter.Spinbox(self.root, from_=0, to=self.total_score, command=self.updateScore, width=4)
        self.tonsh_spin.grid(row=5, column=3)

        self.sport_label = tkinter.Label(self.root, text="體育")
        self.sport_label.grid(row=4, column=4)
        self.sport_spin  = tkinter.Spinbox(self.root, from_=0, to=self.total_score, command=self.updateScore, width=4)
        self.sport_spin.grid(row=5, column=4)
        
        self.sweet_scale  = tkinter.Scale(self.root, label="甜度", from_=5, to=0)
        self.sweet_scale.grid(row=6, column = 0)
        self.sweet_scale.set(5)
        self.load_scale   = tkinter.Scale(self.root, label="重度", from_=310, to=0, variable=5)
        self.load_scale.grid(row=6, column = 1)
        self.load_scale.set(125)
        self.credit_scale = tkinter.Scale(self.root, label="學分", from_=31, to=0)
        self.credit_scale.grid(row=6, column = 4)
        self.credit_scale.set(25)

        self.score_label = tkinter.Label(self.root, text="能力點數：%i" % (21-self.total_score))
        self.score_label.grid(row=7, column=0, columnspan=2)
        
        self.search_button = tkinter.Button(self.root, text="搜尋最佳課程", command=self.searchMethod)
        self.search_button["width"] = 20
        self.search_button.grid(row=7, column=2, columnspan=3)
        
        self.login_button = tkinter.Button(self.root, text="登入", command=self.loginMethod)
        self.login_button.grid(row=8, column=1)
    
        self.quit_button = tkinter.Button(self.root, text="離開", command=self.root.destroy)
        self.quit_button.grid(row=8, column=3)
    

        self.test = Table(self.root,
                     rows=16,
                     cols=7,
                     state='disabled',
                     width=20,
                     height=100,
                     rowheight=2,
                     colwidth=15,
                     titlerows=1,
                     titlecols=1,
                     roworigin=-1,
                     colorigin=-1,
                     selectmode='browse',
                     #selecttype='row',
                     rowstretch='unset',
                     colstretch='last',
                     browsecmd=self.browsecmd,
                     flashmode='on',
                     variable=self.var,
                     usecommand=0,
                     command=self.test_cmd)
        self.test.grid(row=0, column=5, rowspan=20)
        self.test.tag_configure('sel', background='yellow')
        self.test.tag_configure('active', background='blue')
        self.test.tag_configure('title', anchor='w', bg='red', relief='sunken')
        self.root.mainloop()

gui = GUI()
gui.initVar()
gui.createTable()
