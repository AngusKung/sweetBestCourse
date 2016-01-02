#!/usr/bin/python
# -*- coding: utf8 -*-

import csv
import cPickle

import Course
import State

Courses = "data/Courses.pkl"

def readLoadingPickle():
	TEACHER = "data/teachers_loading.pkl"
	CLASSES = "data/classes_loading.pkl"
	TEACHER_CLASS = "data/class_teacher_loading.pkl"
	with open(TEACHER,'rb') as fh:
		teacher = cPickle.load(fh)
	with open(CLASSES,'rb') as fh:
		classes = cPickle.load(fh)
	with open(TEACHER_CLASS,'rb') as fh:
		teacher_class = cPickle.load(fh)

	return teacher,classes,teacher_class

def readCoursePickle():
	with open(Courses,'rb') as fh:
		courses,general_courses,PE_courses = cPickle.load(fh)
	return courses,general_courses,PE_courses

#def classify(name):

def readSweetyCsv():
	sweety_dict = dict()
	with open ("Data/sweety_list.csv", 'r') as f :
		for line in f :
			info = line.split(',')
			course_name = info[0].decode('utf-8')
			#print course_name
			#teacher = info[1]
			#credit = info[2]
			#class_for = info[3]
			#class_num = info[4]
			#class_time= info[5]
			#people_num= info[6]
			#remark = info[7]
			#F = info[8]
			#Cm = info[9]
			#C  = info[10]
			#Cp = info[11]
			#Bm = info[12]
			#B  = info[13]
			#Bp = info[14]
			#Am = info[15]
			#A  = info[16]
			#Ap = info[17]
			if course_name not in sweety_dict:
				sweety_dict[course_name] = [info[1:]]
			else:
				sweety_dict[course_name].append(info[1:])
	return sweety_dict

def checkRuleOut( courses, course, distrib, rule_out):
	if "PE" in course.ID:
		if distrib[4] <= 1:
			distrib[4] = 0
			for c in courses:
				if c!= course and "PE" in c.ID:
					print c.name
					rule_out.add(c)
		else:
			distrib[4] -= 1
	return distrib
