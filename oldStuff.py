(nextState,score,class_stars,GPA,course) = max([(self.InitialState.generateSuccessor(course,self.credit_limit),\
                    (course.class_stars/5.0*3.66)+course.GPA,course.class_stars,course.GPA,course)\
                    for course in self.courses if self.InitialState.generateSuccessor(course,self.credit_limit) != None and course.credit<=category[0]],key=itemgetter(1))
        (nextState,score,class_stars,GPA,course) = max([(self.InitialState.generateSuccessor(course,self.credit_limit),\
                    (course.class_stars/5.0*3.66)+course.GPA,course.class_stars,course.GPA,course)\
                    for course in self.courses if self.InitialState.generateSuccessor(course,self.credit_limit) != None],key=itemgetter(1))
        print nextState.distrib, nextState.rule_out
        nextState.distrib = checkRuleOut(self.courses, course, nextState.distrib, nextState.rule_out)
        print nextState.distrib, nextState.rule_out
        while True:
            try:
                (nextState,score,class_stars,GPA,course) = max([(nextState.generateSuccessor(course,self.credit_limit),\
                        (course.class_stars/5.0*3.66)+course.GPA,course.class_stars,course.GPA,course)\
                        for course in self.courses if nextState.generateSuccessor(course,self.credit_limit) != None],key=itemgetter(1))
                print nextState.distrib, nextState.rule_out
                nextState.distrib = checkRuleOut(self.courses, course, nextState.distrib, nextState.rule_out)
                print nextState.distrib, nextState.rule_out
                for c in nextState.taken:
                    for t in c.time:
                        index = "%i,%i" % (int(t[1]), (int(ord(t[0])-65)))
                        self.var[index] = c.name
            except:
                print "Greedy finished!!!"
                break