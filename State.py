#!/usr/bin/python
# -*- coding: utf8 -*-

import Course
import pdb
import random
import numpy as np
from operator import itemgetter

class State:
  def __init__( self, prevState = None ):
    if prevState != None :
      self.taken = prevState.taken #set of course taken (type = Course)
      self.free = prevState.free	#set of free time slot
      self.credit = prevState.credit
      #[shibi,shishuan,shuanshow,general,PE]
      self.distrib = prevState.distrib
      self.rule_out = prevState.rule_out
      self.personDepart = prevState.personDepart
      self.depart_courses = prevState.depart_courses
      self.non_depart_courses = prevState.non_depart_courses
      self.general_courses = prevState.general_courses
      self.PE_courses = prevState.PE_courses
      self.loading = prevState.loading
      self.loading_limit = prevState.loading_limit
      self.sweetW = prevState.sweetW
      self.loadW = prevState.loadW
      """
      Mon  Tues Wed  Thur Fri  Sat  Sun
      A0   B0   C0   D0   E0   F0   G0
      .    .    .    .    .    .    .
      .    .    .    .    .    .    .
      .    .    .    .    .    .    .
      A5   B5   C5   D5   E5   F5   G5
      .    .    .    .    .    .    .
      .    .    .    .    .    .    .
      .    .    .    .    .    .    .
      A14  B14  C14  D14  E14  F14  G14
      """
    else:
      self.taken = []
      self.free = set()
      self.credit = 0
      dayList = ['A','B','C','D','E','F','G']
      for day in dayList:
        for i in range(0,15):
          self.free.add(day+str(i))
      self.distrib = [[],[0],0,0,0,0]
      self.rule_out = set()
      self.personDepart = "None"
      self.depart_courses = self.non_depart_courses = self.general_courses = self.PE_courses = []
      self.loading = 0.0
      self.loading_limit = 125.0
      self.sweetW = 1.0
      self.loadW = 1.0

  def __eq__( self , other ):
  	return self.taken == other.taken

  def __str__( self ):
    a = ""
    dayList = ['A','B','C','D','E','F','G']
    for i in range(0,15):
      for day in dayList:
        if day+str(i) not in self.free:
          a += day+str(i)+"  "
          if i<10: a += " "
        else : 
          a += "□    "
      a += "\n"
    a += "                           " + str(self.credit) + "學分"
    return a


  def __hash__( self ):
    return hash(self.taken)

  def canTake( self , course ):
    for time in course.getTime():
      if time not in self.free:
        return False
    if course.credit == 0 or course in self.rule_out or course in self.taken:
      return False
    return True

  def generateSuccessor( self , course):
    if course.credit == 0 or course in self.rule_out or course in self.taken:
      raise Exception("Cannot take course "+str(course))
    if not self.canTake(course):
      raise Exception("Cannot take course "+str(course))
    state = State(self)
    for time in course.getTime():
      state.free.remove(time)
    state.taken.append(course)
    state.credit += course.credit
    state.loading += course.class_load
    return state

  def clearCourses(self):
    for course in self.taken:
      for time in course.getTime():
        self.free.add(time)
      self.credit -= course.credit
      self.loading -= course.class_load
      self.taken.remove(course)
    print self.free
    print self.credit
    print self.loading
    print self.taken

  def setPersonDepart( self,department ):
    self.personDepart = department

  def setPersonDistrib( self, distrib):
    self.distrib = distrib
    #[必修,[複選必修],系選修,一般選修,通識,體育]

  def setCategorizedCourses( self, depart_courses, non_depart_courses, general_courses, PE_courses):
    self.depart_courses = depart_courses
    self.non_depart_courses = non_depart_courses
    self.general_courses = general_courses
    self.PE_courses = PE_courses

  def setLoading( self, loading ):
    self.loading = loading

  def setLoadingLimit( self, loading_limit ):
    self.loading_limit = loading_limit

  def setSweetW( self, sweetW):
    self.sweetW = sweetW

  def setLoadW( self, loadW):
    self.loadW = loadW

  def setCustomDistrib( self, dis2, dis3, dis4, dis5):
    self.distrib[2] = dis2
    self.distrib[3] = dis3
    self.distrib[4] = dis4
    self.distrib[5] = dis5

  def greedySearch( self ):
    toSelect = []
    result_state = None
    #必修 ,always first
    result = self.maxBishow(self.distrib[0])
    if result:
      result_state = self.generateSuccessor(result[1])
      return result_state
    #[複選必修]
    result1 = self.maxFushuanBishow(self.distrib[1])
    print "複選必修:"
    if result1:
      toSelect.append(result1)
      course1 = result1[1]
      print result1[0],course1
    else:
      course1 = Course.Course("name", "teacher" , (0,0) , 0, [0], 'CC0000')
      print "empty"
    #系選修
    result2 = self.maxDepartSelective(self.distrib[2])
    print "系選修:"
    if result2:
      toSelect.append(result2)
      course2 = result2[1]
      print result2[0],course2
    else:
      course2 = Course.Course("name", "teacher" , (0,0) , 0, [0], 'CC0000')
      print "empty"
    #一般選修
    result3 = self.maxSelective(self.distrib[3])
    print "一般選修:"
    if result3:
      toSelect.append(result3)
      course3 = result3[1]
      print result3[0],course3
    else:
      course3 = Course.Course("name", "teacher" , (0,0) , 0, [0], 'CC0000')
      print "empty"
    #通識
    result4 = self.maxGeneral(self.distrib[4])
    print "通識:"
    if result4:
      toSelect.append(result4)
      course4 = result4[1]
      print result4[0],course4
    else:
      course4 = Course.Course("name", "teacher" , (0,0) , 0, [0], 'CC0000')
      print "empty"
    #體育
    result5 = self.maxPE(self.distrib[5])
    print "體育:"
    if result5:
      toSelect.append(result5)
      course5 = result5[1]
      print result5[0],course5
    else:
      course5 = Course.Course("name", "teacher" , (0,0) , 0, [0], 'CC0000')
      print "empty"

    if not toSelect:
      print "Nothing in toSelect"
      return None
    else:
      course = max(toSelect,key=itemgetter(0))[1]
      if course == course1:
        for single in self.distrib[1]:
          if course1 in single:
            self.distrib[1].remove(single)
      elif course == course2:
        self.distrib[2] -= course2.credit
        #self.depart_courses.remove(course)
      elif course == course3:
        self.distrib[3] -= course3.credit
        #self.non_depart_courses.remove(course)
      elif course == course4:
        self.distrib[4] -= course4.credit
        #self.general_courses.remove(course)
      elif course == course5:
        self.distrib[5] -= course5.credit
        #self.PE_courses.remove(course)
      result_state = self.generateSuccessor(course)
      return result_state

  def maxBishow( self, selectList ):
    if not self.distrib[0]:
      return None
    return self.maxScore(selectList,10)

  def maxFushuanBishow( self, selectList ):
    if not self.distrib[1]:
      return None
    try:
      return max([self.maxScore(courses,10) for courses in self.distrib[1]],key=itemgetter(0))
    except:
      return None
    # 10 is a null number, for guaranteed permission

  def maxDepartSelective( self, remain_credit):
    if remain_credit==0:
      return None
    departSelective = [c for c in self.depart_courses if ord(c.ID[2])>=4]
    return self.maxScore(departSelective,remain_credit)

  def maxSelective( self, remain_credit):
    if remain_credit==0:
      return None
    course = self.maxScore(self.non_depart_courses,remain_credit)
    '''
    if course[1].class_recc != None and (course[1].class_recc - 2) > random.uniform(0,5):
      self.non_depart_courses.remove(course[1])
    if course[1].teacher_recc != None and (course[1].teacher_recc - 2) > random.uniform(0,5):
      self.non_depart_courses.remove(course[1])
    '''
    return self.maxScore(self.non_depart_courses,remain_credit)

  def maxGeneral( self, remain_credit):
    if remain_credit==0:
      return None
    course = self.maxScore(self.general_courses,remain_credit)
    '''
    if course[1].class_recc != None and (course[1].class_recc - 2) > random.uniform(0,5):
      self.general_courses.remove(course[1])
    if course[1].teacher_recc != None and (course[1].teacher_recc - 2) > random.uniform(0,5):
      self.general_courses.remove(course[1])
    '''
    return self.maxScore(self.general_courses,remain_credit)

  def maxPE( self,remain_credit):
    if remain_credit==0:
      return None
    return self.maxScore(self.PE_courses,remain_credit)

  def maxScore( self, courses ,creditLimit):
    try:
      return max([( course.GPA*self.sweetW*course.favor+course.class_load*0.43*self.loadW*course.favor, course ) for course in courses \
                if (course.credit <= creditLimit and self.canTake(course) and self.loading+course.class_load <= self.loading_limit)],key=itemgetter(0))
    except:
      return None

  def transformID( self ):
    options = [selection[1:] for selection in self.distrib[1]]
    real_options = []
    for opt in options:
      temp_option = []
      for ID in opt:
        for course in self.depart_courses:
          if course.ID == ID:
            temp_option.append(course)
            self.depart_courses.remove(course)
            break
      real_options.append(temp_option)
    self.distrib[1] = real_options
    temp = []
    print "Bi show:"
    for ID in self.distrib[0]:
      for course in self.depart_courses:
        if course.ID == ID:
          print course
          temp.append(course)
          self.depart_courses.remove(course)
    self.distrib[0] = temp

  def findCourse( self, course_name, teacher):
    for course in self.depart_courses+self.non_depart_courses+self.general_courses+self.PE_courses:
      if course.name==course_name and course.teacher==teacher:
        print course
        return course
    return None

  def deleteCourse(self, course_name, teacher, time, cmd):
    #print course_name, teacher, time
    for c in self.taken:
      if c.name == course_name and c.teacher == teacher:
        if time in c.time or cmd:
          print "Delete:",course_name, teacher
          state = State(self)
          for time in c.getTime():
            state.free.add(time)
          state.taken.remove(c)
          state.credit -= c.credit
          state.loading -= c.class_load
          course = c
          if c in self.distrib[0]:
            self.distrib[0].remove(c)
          for sublist in self.distrib[1]:
            if c in sublist:
              sublist.remove(c)
          if c in state.depart_courses:
            state.depart_courses.remove(c)
          if c in state.non_depart_courses:
            state.non_depart_courses.remove(c)
          if c in state.general_courses:
            state.general_courses.remove(c)
          if c in state.PE_courses:
            state.PE_courses.remove(c)
          return state, c.time, course
    return None, None, None

  def pureDelete(self, course):
    for time in c.getTime():
      self.free.add(time)
    self.taken.remove(course)
    self.credit -= course.credit
    self.loading -= course.class_load

  def likeCourse(self, course):
    maxdot = 0
    print " ========= You may also like ========"
    for c in self.depart_courses+self.non_depart_courses+self.general_courses+self.PE_courses:
      average_dot = 0
      count = 0
      for vectorA in course.word_vectors:
        dot = 0
        for vectorB in c.word_vectors:
          dot = np.dot(vectorA,vectorB)
          if dot > maxdot:
            maxdot = dot
          average_dot+=dot
          count+=1
      if count != 0:
        average_dot /= float(count)
        if average_dot >5.0:
          print c
          c.favor+=(0.2*average_dot)

  def dislikeCourse(self, course):
    maxdot = 0
    print " ========= You may also dislike ========"
    for c in self.depart_courses+self.non_depart_courses+self.general_courses+self.PE_courses:
      average_dot = 0
      count = 0
      for vectorA in course.word_vectors:
        dot = 0
        for vectorB in c.word_vectors:
          dot = np.dot(vectorA,vectorB)
          if dot > maxdot:
            maxdot = dot
          average_dot+=dot
          count+=1
      if count != 0:
        average_dot /= float(count)
        if average_dot >5.0:
          print c
          if c.favor<(0.2*average_dot):
            c.favor = 0.0
          else:
            c.favor-=(0.2*average_dot)



    