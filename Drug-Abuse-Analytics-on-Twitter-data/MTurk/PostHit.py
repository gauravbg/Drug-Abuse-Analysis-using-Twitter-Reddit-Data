'''
Created on Feb 17, 2017

@author: Gaurav BG
'''
import csv
import sys 
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer
from fileinput import filename

sandbox_host = 'mechanicalturk.sandbox.amazonaws.com'
real_host = 'mechanicalturk.amazonaws.com'
 
ACCESS_ID ="DUMMY_FOR_GITHUB"
SECRET_KEY = "DUMMY_FOR_GITHUB"
HOST = sandbox_host


class TweetInfo:
    def __init__(self, tweetId, text, keyword, uId, scName):
        self.tweetId = tweetId
        self.text = text
        self.keyword = keyword 
        self.uId = uId
        self.scName = scName
    


def parseFile(fileName):
    
    f = open(fileName, encoding="latin-1")
    csv_f = csv.reader(f)

    allTweetInfos = []

    for row in csv_f:
        tweet = TweetInfo(tweetId= row[1], text= row[3], keyword= row[4], uId= row[5], scName= row[6])
            
        allTweetInfos.append(tweet)
        
    return allTweetInfos

 
    

if __name__ == '__main__':
    
    filePath = "C:/Users/gaura/Desktop/Course Material/Sem 2/Advanced Project (CSE-523)/Data/Marijuana_AMT_data/"
    inFileName = "cannabis.csv.csv"
    outFilename = "C:/Users/gaura/Desktop/Course Material/Sem 2/Advanced Project (CSE-523)/Data/HITs/hitIds.txt"
    out_file = open(outFilename, 'w')
    mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                          aws_secret_access_key=SECRET_KEY,
                          host=HOST)
    allTweetInfos = parseFile(filePath + inFileName) 
    title = "Classify these Tweets as marijuana related or not"
    description = ("Read the Tweets and mark each of them as marijuana related or not. Select not sure if unsure")
    keywords = "Marijuana, Classify, Drugs, Weed, Smoking, Study, Medical"
    hittype= "3LA9UWLSKBAE4HD14EHD90BL61WY18"
      
    ratings =[('Its related to Marijuana','1'),
             ('Not related to marijuana','-1'),
             ('Not Sure','0')]
    
    totalSize = 35 
    batchSize = 10
    batchCount = int(totalSize/batchSize) + 1
    startIndex = 1
    endIndex = 1 + batchSize
    
    out_file.write(str(filePath+inFileName))
    out_file.write('\n')
    for batchNum in range(batchCount):
        overview = Overview()
        overview.append_field('Title', 'Classify these Tweets as marijuana related or not')
        overview.append(FormattedContent("Select the appropriate answer from dropdown for each tweet"))
        question_form = QuestionForm()
        question_form.append(overview)
        qNumber = 1
        for index in range(startIndex, endIndex):
            tweet = allTweetInfos[index]
            qc1 = QuestionContent()
            tweetText = str(qNumber) + ") " + tweet.text
            qc1.append_field('Title',tweetText)
            fta1 = SelectionAnswer(min=1, max=1,style='radiobutton',
                              selections=ratings,
                              type='text',
                              other=False)
             
            q1 = Question(identifier=tweet.tweetId,
                      content=qc1,
                      answer_spec=AnswerSpecification(fta1),
                      is_required=True)
            question_form.append(q1)
            qNumber = qNumber + 1
        response = mtc.create_hit(hit_type=hittype,
                    questions=question_form,
                    max_assignments=3,
                    title=title,
                    description=description,
                    keywords=keywords)
        print("Batch: " + str(batchNum) + "-- " + str(response[0].HITId))
        out_file.write("Hit ID: " +str(response[0].HITId) + "\n")
        startIndex = endIndex
        increment = min(batchSize, totalSize - endIndex)
        endIndex = endIndex + increment
    out_file.write('--------------------------------------------------- \n')

    
