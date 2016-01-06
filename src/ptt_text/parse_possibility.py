#!/usr/bin/python
# -*- coding: utf8 -*-
import os
import glob
import cPickle as pickle
from collections import defaultdict

adv_dict = dict()
nega_list = []
posi_list = []
posi_spe_list = []

out = open("output.txt",'w+')

def parse_index():
	f = open("possibility_word.txt", "rb")
	for line in f:
		if line[:6] == "weight":
			weight = float(line[7:11])
			advs = line.split(" ")
			for adv in advs[1:]:
				adv_dict[adv] = weight
		if line[:5] == "p_adj":
			#adjs = line.split(" ")
			#for adj in adjs[1:]:
			posi_list.append("簽")

		if line[:5] == "n_adj":
			adjs = line.split(" ")
			for adj in adjs[1:]:
				nega_list.append(adj)
		if line[:8] == "p_behind":
			adjs = line.split(" ")
			for adj in adjs[1:]:
				posi_spe_list.append(adj)

		

def get_loading_sum(dictionary):
	for item in dictionary:
		total_score = 0.
		for score in dictionary[item]:
			total_score += score / len(dictionary[item])
		dictionary[item] = total_score
	return dictionary

def parse_loading(filename):
	class_teacher = dict()
	teachers = dict()
	classes = dict()
	class_teacher = defaultdict(lambda: [], class_teacher)
	teachers = defaultdict(lambda: [], teachers)
	classes = defaultdict(lambda: [], classes)
	for filename in glob.glob('%s' % filename):
		with open(filename, 'r') as fh:
			#print '\n'+filename
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
			
			start_parsing = False
			for line in fh:
				if start_parsing:
					
					
					#Negative
					for key in nega_list:
						indice = []
						index = line.find(key,0)
						indice.append(index)
						while not index==-1:
							index = line.find(key,index+1)
							indice.append(index)
						indice.remove(-1)
						for index in indice:
							pos = -1
							match = False
							for adv in adv_dict:
								if adv in line[index-13: index]:
									match = True
									pos *= float(adv_dict[adv])
							if match and not line[index:index+6] == "簽到":
								teachers[T].append(pos)
								classes[C].append(pos)
								class_teacher[(C, T)].append(pos)
					
					#Positive
					for key in posi_list:
						indice = []
						index = line.find(key,0)
						indice.append(index)
						while not index==-1:
							index = line.find(key,index+1)
							indice.append(index)
						indice.remove(-1)
						for index in indice:
							pos = 1
							match = False
							for adv in adv_dict:
								if adv in line[index-12: index]:
									match = True
									pos *= float(adv_dict[adv])
							for spe in posi_spe_list:
								if spe in line[index:index+24]:
									teachers[T].append(1)
									classes[C].append(1)
									class_teacher[(C, T)].append(1)
							if match and not line[index:index+6] == "簽到":
								
								teachers[T].append(pos)
								classes[C].append(pos)
								class_teacher[(C, T)].append(pos)
					
						
				if "其他" in line and "其他非營利用途" not in line and "其他條件" not in line:
					start_parsing = True
	teachers = dict(get_loading_sum(teachers))
	classes = dict(get_loading_sum(classes))
	class_teacher = dict(get_loading_sum(class_teacher))
	return teachers, classes, class_teacher

parse_index()
t, c, ct = parse_loading("NTUcourse/*.txt")
#for i in t:
#	if t[i] > 0:
#		print i, t[i]
#print type(t)
pickle.dump(t, open("teachers_possibility.pkl", "wb"))
pickle.dump(c, open("classes_possibility.pkl", "wb"))
pickle.dump(ct, open("class_teacher_possibility.pkl", "wb"))
