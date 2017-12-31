import praw
import os
import csv
import time
import datetime
import calendar

CLIENT_SECRET = "I6d1SBvTLhkzCPCdc0ztH89yNas"
CLIENT_ID = "lY11fnanLA-yYQ"
USER_AGENT = "gauravbgopiates"
OPIATES_SUB_REDDIT = 'Opiates'
OUTPUT_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__)) + "/output/"


def getNext(y, m):
    if month == 12:
        return y+1, 1
    else:
        return y, m+1


if __name__ == "__main__":

    start_time = time.time()
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         user_agent=USER_AGENT)

    opiates_subR = reddit.subreddit(OPIATES_SUB_REDDIT)

    YEARS = [2014, 2015, 2016, 2017]
    MONTHS = [1,2,3,4,5,6,7,8,9,10,11,12]

    for year in YEARS:
        for month in MONTHS:
            START_PERIOD = datetime.date(year=year, month=month, day=1).strftime('%s')
            next_year, next_month = getNext(year, month)
            END_PERIOD = datetime.date(year=next_year, month=next_month, day=1).strftime('%s')
            DATA_FILE = str(year) + "-" + str(month) + ".csv"

            hot_opiates_subR =  opiates_subR.submissions(START_PERIOD, END_PERIOD)
            submission_count = 0
            comment_count = 0

            with open(OUTPUT_FOLDER_PATH + DATA_FILE, 'w') as out_file:
                wr = csv.writer(out_file, quoting=csv.QUOTE_ALL)
                row = ["ID", "TYPE", "PARENT", "AUTHOR", "SCORE", "CREATED_AT", "CONTENT", "TITLE", "CONTENT_URL"]
                wr.writerow(row)
                row =[]
                for submission in hot_opiates_subR:
                    if not submission.stickied:
                        row.append(submission.id)
                        row.append("S")
                        row.append("Opiates")
                        row.append(submission.author)
                        row.append(submission.score)
                        row.append(datetime.datetime.fromtimestamp(submission.created))
                        row.append(submission.selftext)
                        row.append(submission.title)
                        row.append(submission.url)
                        wr.writerow(row)
                        submission_count+=1
                        row = []
                        submission.comments.replace_more(limit=0)
                        comments = submission.comments.list()
                        for comment in comments:
                            try:
                                row.append(comment.id)
                                row.append("C")
                                row.append(comment.parent())
                                row.append(comment.author)
                                row.append(comment.score)
                                row.append(datetime.datetime.fromtimestamp(comment.created))
                                row.append(comment.body)
                                wr.writerow(row)
                                comment_count += 1
                                row = []
                            except AttributeError as err:
                                print(err)
                                pass

            out_file.close()
            end_time = time.time()
            total_time =  "{:.2f}".format((end_time-start_time)/60)
            print("Year: {year}, Month: {month}".format(year=year, month=month))
            print("Fetched {submissions} submissions  and {comments} comments in {time} minutes".format(submissions=submission_count, comments=comment_count, time=total_time))
            print("-"*50)