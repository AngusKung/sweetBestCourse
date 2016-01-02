#!/usr/bin/python
# -*- coding: utf8 -*-

class Course:
  def __init__( self, name , teacher , time , credit, sweet, ID):
    self.name = name
    self.teacher = teacher
    self.credit = int(credit) if credit!='' else 0
    self.sweet = sweet # FuShwenBiShow * (high num)
    self.time = set() # given a NULL time to indicate rule-out
    for item in time:
      self.time.add(item)
    # general, PE, BiShow, department selective, general selective
    self.ID = ID
    self.class_stars = None
    self.teacher_stars = None
    self.class_load = 0.0
    self.teacher_load = 0.0
    self.category = []
    if sum(self.sweet)==0:
      self.GPA = 3.66
    else:
      aver_sweet = 4.3*self.sweet[9] +4.0*self.sweet[8] +3.7*self.sweet[7] +3.3*self.sweet[6] \
                +3.0*self.sweet[5] +2.7*self.sweet[4] +2.3*self.sweet[3] +2.0*self.sweet[2] +1.7*self.sweet[1]
      self.GPA = aver_sweet/float(sum(self.sweet))

  def __eq__( self , other ):
  	return self.name == other.name and self.teacher == other.teacher and self.time == other.time 

  def __str__( self ):
    a = str(self.credit) + "學分_" + self.name + ": " + self.teacher + " "
    for item in sorted(self.time):
      a = a + "-" + item
    a = a + " " + self.ID + " " + str(self.category)
    return a

  def __hash__( self ):
    return hash(self.name+self.teacher)

  def getTime( self ):
    time_o = set(self.time)
    return time_o

  def getSweetlist( self ):
    return self.sweet

  def getFailratio( self ):
    if sum(self.sweet)==0:
      return 0
    else:
      # return __%
      return (self.sweet[0]/float(sum(self.sweet)))*100

  def setClassStars( self, stars ):
    self.class_stars = stars

  def setTeacherStars( self, stars ):
    self.teacher_stars = stars

  def setClassLoad( self, load ):
    self.class_load = load

  def setTeacherLoad( self, load ):
    self.teacher_load = load

  def setCategory( self, newCat ):
    self.category.append(newCat)
