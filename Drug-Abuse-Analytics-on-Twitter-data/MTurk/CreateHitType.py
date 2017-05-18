'''
Created on Feb 25, 2017

@author: Gaurav BG
'''
from boto.mturk.connection import MTurkConnection
from boto.mturk.qualification import Qualifications, Requirement, LocaleRequirement
from boto.mturk.question import QuestionContent, Question, QuestionForm, Overview, AnswerSpecification, SelectionAnswer, FormattedContent, FreeTextAnswer


ACCESS_ID ="DUMMY_FOR_GITHUB"
SECRET_KEY = "DUMMY_FOR_GITHUB"
HOST = 'mechanicalturk.sandbox.amazonaws.com'

mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)
 
title = "Classify Tweets related to Marijuana"
description = ("Read the Tweets and mark each of them as marijuana related or not. Select not sure if unsure")
keywords = "Marijuana, Classify, Drugs, Weed, Annotation"
operation = "Marijuana Tweet Classification"
reward = 0.05
duration = 60 * 60 * 3

qualifications = Qualifications()
master_req = Requirement(
                    qualification_type_id="2ARFPLSP75KLA8M8DH1HTEQVJT3SY6",
                    comparator='Exists')
assignment_approval_req = Requirement(
                    qualification_type_id="000000000000000000L0",
                    comparator='GreaterThan',
                    integer_value= 90)
adult_req = Requirement(qualification_type_id= '00000000000000000060',
                        comparator= 'EqualTo',
                        integer_value= 1, 
                        required_to_preview= True)  
locale_req = LocaleRequirement(comparator='EqualTo', locale= "US")

# qualifications.add(master_req)
# qualifications.add(assignment_approval_req)
qualifications.add(adult_req)
qualifications.add(locale_req)
    
response = mtc.register_hit_type(title, description, reward, duration, qual_req=qualifications)

print(response[0].HITTypeId)