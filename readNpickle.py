#!/usr/bin/python
# -*- coding: utf8 -*-

import cPickle
import csv
import pdb
import jieba
import gensim
import numpy

import Course
import State

jieba.set_dictionary('jieba/extra_dict/dict.txt.big')
model = gensim.models.Word2Vec.load("data/wiki.zh.text.model")

sweety_list = "data/sweety_list.csv"
NTUcourse = "data/NTUcourse_stars.pkl"
EEComment = "data/EE_comment_stars.pkl"
Courses = "data/Courses.pkl"

TEACHER = "data/teachers_loading.pkl"
CLASSES = "data/classes_loading.pkl"
TEACHER_CLASS = "data/class_teacher_loading.pkl"
with open(TEACHER,'rb') as fh:
	teacher_load = cPickle.load(fh)
with open(CLASSES,'rb') as fh:
	class_load = cPickle.load(fh)
with open(TEACHER_CLASS,'rb') as fh:
	teacher_class_load = cPickle.load(fh)
teacher_recc = cPickle.load(open("data/teachers_recc.pkl"))
class_recc   = cPickle.load(open("data/classes_recc.pkl"))
teacher_class_recc = cPickle.load(open("data/class_teacher_recc.pkl"))

fh = open(NTUcourse,'rb')
teacher_stars,class_stars,teacher_classes,class_teachers = cPickle.load(fh)
fh = open(EEComment,'rb')
t_stars,c_stars,teacher_classes,class_teachers = cPickle.load(fh)
teacher_stars.update(t_stars)
class_stars.update(c_stars)

with open(sweety_list, 'rb') as fh:
	courses = []
	general_courses = []
	PE_courses = []
	data = csv.reader(fh, delimiter=',')
	for line in data:
		#=====reduce duplicated courses=====
		flag=0
		for c in courses:
			if line[0]==c.name and line[1]==c.teacher:
				flag =1
		if flag==1:
			continue
		#==========
		newC = Course.Course(line[0],line[1],[l for l in line[5].split(' ') if l != '']\
							,line[2],[int(s) for s in line[8:]],line[4])
		#----- to cut the word and append vector -----
		words = jieba.cut(line[0].strip())
		vectors = []
		for word in words:
			print word
			if word not in model or word ==u'一' or word ==u'二' or word ==u'三' or word ==u'四' or word ==u'上' or word ==u'下' or word ==u'導論' or word ==u'概論' or word ==u'通論' or word ==u'與' or word ==u'實務' or word ==u'原理' or word ==u'學':
				print "Not in consideration:",word
				continue
			vectors.append(model[word])
		newC.setWordVectors(vectors)

		if line[0] in class_load:
			newC.setClassLoad(((-class_load[line[0]])+1.0)*5.0)
			if newC.class_load <= 5:
				print newC
				print newC.class_load
		#default = 0.0
		if line[1] in teacher_load:
			newC.setTeacherLoad(((-teacher_load[line[1]])+1.0)*5.0)
			#print line[1],":",newC.teacher_load
		#default = 0.0
		if line[0] in class_recc:
			newC.setClassRecc(class_recc[line[0]]*2.5+2.5)
		if line[1] in teacher_recc:
			newC.setTeacherRecc(teacher_recc[line[1]]*2.5+2.5)	
		if line[0] in class_stars:
			newC.setClassStars( class_stars[line[0]] )
		else:
			newC.setClassStars(4.49725061046)
		if line[1] in teacher_stars:
			newC.setTeacherStars( teacher_stars[line[1]] )
		else:
			newC.setTeacherStars(4.30677054049)
		if 'PE' in newC.ID:
			PE_courses.append(newC)
			continue
		general = line[7].split('A')
		if len(general)>1:
			try:
				general_num = int(general[1][0])
				if general_num in range(1,9):
					newC.setCategory(general_num)
					general_courses.append(newC)
					general_num_2 = int(general[1][1])
					if general_num_2 in range(1,9):
						newC.setCategory(general_num_2)
						continue
			except:
				pass
		courses.append(newC)
fh.close()
fh = open(Courses,'wb')
saved_params = courses,general_courses,PE_courses
cPickle.dump(saved_params,fh)
fh.close()