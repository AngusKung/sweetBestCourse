#!/usr/bin/python
# -*- coding: utf8 -*-
import os
import glob
import cPickle as pickle
from collections import defaultdict

adv_dict = dict()
nega_list = []
posi_list = []
nega_spe_list = []
posi_spe_list = []

def parse_index():
	f = open("index_word.txt", "rb")
	for line in f:
		if line[:6] == "weight":
			weight = float(line[7:10])
			advs = line.split(" ")
			for adv in advs[1:]:
				adv_dict[adv] = weight
		if line[:5] == "p_adj":
			adjs = line.split(" ")
			for adj in adjs[1:]:
				posi_list.append(adj)
		if line[:5] == "p_adv":
			advs = line.split(" ")
			for adv in advs[1:]:
				posi_spe_list.append(adv)
		if line[:5] == "n_adj":
			adjs = line.split(" ")
			for adj in adjs[1:]:
				nega_list.append(adj)
		if line[:5] == "n_adv":
			advs = line.split(" ")
			for adv in advs[1:]:
				nega_spe_list.append(adv)

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
				if "私心推薦" in line:
					start_parsing = True
				if start_parsing:
					'''Negative'''
					for key in nega_list:
						if key in line:
							for adv in adv_dict:
								if adv in line[line.index(key)-12: line.index(key)]:
									teachers[T].append(-float(adv_dict[adv]))
									classes[C].append(-float(adv_dict[adv]))
									class_teacher[(C, T)].append(-float(adv_dict[adv]))
					for key in nega_spe_list:
						if key in line:
							teachers[T].append(-0.5)
							classes[C].append(-0.5)
							class_teacher[(C, T)].append(-0.5)
					'''Positive'''
					for key in posi_list:
						if key in line:
							for adv in adv_dict:
								if adv in line[line.index(key)-12: line.index(key)]:
									teachers[T].append(float(adv_dict[adv]))
									classes[C].append(float(adv_dict[adv]))
									class_teacher[(C, T)].append(float(adv_dict[adv]))
					for key in posi_spe_list:
						if key in line:
							teachers[T].append(0.5)
							classes[C].append(0.5)
							class_teacher[(C, T)].append(0.5)
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
pickle.dump(t, open("teachers_loading.pkl", "wb"))
pickle.dump(c, open("classes_loading.pkl", "wb"))
pickle.dump(ct, open("class_teacher_loading.pkl", "wb"))
