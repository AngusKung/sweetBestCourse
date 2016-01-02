#!/usr/bin/python
# -*- coding: utf8 -*-

import Course
import pdb
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
      self.distrib = [0,[0],0,0,0,0]
      self.rule_out = set()
      self.personDepart = "None"
      self.depart_courses = self.non_depart_courses = self.general_courses = self.PE_courses = []

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
    return state

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

  def greedySearch( self ):
    toSelect = []
    result_state = None
    # - TO DO -
    #必修
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
      return None
    else:
      course = max(toSelect,key=itemgetter(0))[1]
      if course == course1:
        for single in self.distrib[1]:
          if course1 in single:
            self.distrib[1].remove(single)
      elif course == course2:
        self.distrib[2] -= course2.credit
        self.depart_courses.remove(course)
      elif course == course3:
        self.distrib[3] -= course3.credit
        self.non_depart_courses.remove(course)
      elif course == course4:
        self.distrib[4] -= course4.credit
        self.general_courses.remove(course)
      elif course == course5:
        self.distrib[5] -= course5.credit
        self.PE_courses.remove(course)
      result_state = self.generateSuccessor(course)
      return result_state

  def maxFushuanBishow( self, selectList ):
    if not self.distrib[1]:
      return None
    return max([self.maxScore(courses,10) for courses in self.distrib[1]],key=itemgetter(0))
    # 5 is a null number, for guaranteed permission

  def maxDepartSelective( self, remain_credit):
    if remain_credit==0:
      return None
    departSelective = [c for c in self.depart_courses if ord(c.ID[2])>=4]
    return self.maxScore(departSelective,remain_credit)

  def maxSelective( self, remain_credit):
    if remain_credit==0:
      return None
    return self.maxScore(self.non_depart_courses,remain_credit)

  def maxGeneral( self, remain_credit):
    if remain_credit==0:
      return None
    return self.maxScore(self.general_courses,remain_credit)

  def maxPE( self,remain_credit):
    if remain_credit==0:
      return None
    return self.maxScore(self.PE_courses,remain_credit)

  def maxScore( self, courses ,creditLimit):
    return max([( (course.class_stars/5.0*3.66)+course.GPA+course.class_load, course ) for course in courses if (course.credit <= creditLimit and self.canTake(course))],key=itemgetter(0))

  def transformID( self ):
    options = [selection[1:] for selection in self.distrib[1]]
    print options
    real_options = []
    for opt in options:
      temp_option = []
      for ID in opt:
        for course in self.depart_courses:
          if course.ID == ID:
            temp_option.append(course)
            break
      real_options.append(temp_option)
    self.distrib[1] = real_options


