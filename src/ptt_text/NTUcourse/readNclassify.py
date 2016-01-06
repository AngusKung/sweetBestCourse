#!/usr/bin/python
# -*- coding: utf8 -*-

import cPickle
import glob
import os
import pdb

FILE_ROOT = "/bbs_crawler/BBS/fetched/"
FILE_DIRECT = "EE_comment/"

teacher_classes = dict()
teacher_stars = dict()
teacher_special = dict()
class_teachers = dict()
class_stars = dict()
class_special = dict()
to_add = []
keywords = []

def ParsePost(fh):
	flag = False
	judgement = False
	specialties = []
	for line in fh:
		#retain one sentence after STAR
		if line == '\n':
			continue
		for word in keywords:
			if word in line:
				if word not in specialties:
					specialties.append(word)
		if "評分方式" in line:
			print line
	if judgement == False:
		return -1,specialties
	else:
		return num,specialties

for filename in glob.glob('*.txt'):
	with open(filename, 'r') as fh:
		print '\n'+filename
		title = fh.readline()
		# prevent multiple []
		title = ''.join((title.split(']')[ len(title.split(']'))-1 ]).split('-')[:-2])
		if len(title.split(' ')[-3:-1]) != 2:
			continue
		T = title.split(' ')[-3:-1][0]
		C = title.split(' ')[-3:-1][1]
		if len(T)!=9 and len(C)==9:
			T,C = C,T
		elif len(T)!=9 and len(C)!=9:
			continue
		print T," ",C

		if T not in teacher_classes:
			teacher_classes[T]=[ [C,filename] ]
			teacher_stars[T]=0
			teacher_special[T]=[]
		else:
			teacher_classes[T].append([ C,filename ])
			print "Teacher Same:",len(teacher_classes[T])

		if C not in class_teachers:
			class_teachers[C]=[ [T,filename] ]
			class_stars[C]=0
			class_special[C]=[]
		else:
			class_teachers[C].append([ T,filename])
			print "Class Same:",len(class_teachers[C])

		to_add,specialties = ParsePost(fh)
		if to_add != -1:
			teacher_stars[T] = float(( ( (len(teacher_classes[T])-1)*teacher_stars[T])+(1*to_add) ) / len(teacher_classes[T]))
			class_stars[C] = float(( ((len(class_teachers[C])-1)*class_stars[C])+(1*to_add) ) /len(class_teachers[C]))
		if specialties != []:
			for specialty in specialties:
				print specialty
		print "Star:",teacher_stars[T],",",class_stars[C]

print "Key words:"
for word in keywords:
	print word
pdb.set_trace()
filehandler = open('NTUcourse_stars.pkl','wb')
saved_params = teacher_stars,class_stars,teacher_classes,class_teachers
cPickle.dump(saved_params, filehandler)
filehandler.close()