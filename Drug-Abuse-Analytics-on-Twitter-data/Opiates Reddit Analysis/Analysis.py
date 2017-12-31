import csv
import os
import datetime
from nltk import TweetTokenizer
import pickle
import time

DATA_FOLDER = "output"
STATS_PICKLE_FILE = "stats.obj"
CONTENT_FILE = "data.txt"
ID_COL = 0
TYPE_COL = 1
PARENT_COL = 2
AUTHOR_COL = 3
SCORE_COL = 4
TIME_COL = 5
CONTENT_COL = 6
TITLE_COL = 7
URL_COL = 8


class Stats:

    def __init__(self):
        self.posts_per_day = dict()
        self.posts_per_user = dict()
        self.comments_per_user = dict()
        self.posts_len = list()
        self.comments_len = list()
        self.posts_score = list()
        self.comments_score = list()
        self.posts_time = list()
        self.comments_time = list()
        self.comments_per_post = list()
        self.parent_dict = dict()
        self.title_len = list()




def readData(data_path):
    start_time = time.time()
    directory = os.listdir(data_path)
    os.chdir(data_path)
    stats = Stats()
    tokenizer = TweetTokenizer()
    write_file_path = os.path.join(os.path.dirname(os.getcwd()), CONTENT_FILE)
    write_file = open(write_file_path, "w")
    for file in directory:
        tokens = file.split("-")
        year = tokens[0]
        month = tokens[1]
        with open(file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                full_time = row[TIME_COL]
                post_date = full_time.split()[0]
                stats.posts_per_day[post_date] = stats.posts_per_day.get(post_date, 0) + 1
                user = row[AUTHOR_COL]
                content_len = len(tokenizer.tokenize(row[CONTENT_COL]))
                score = row[SCORE_COL]
                stats.parent_dict[row[ID_COL]] = row[PARENT_COL]
                write_file.write(row[CONTENT_COL])
                write_file.write("\n")
                if row[TYPE_COL] == "S":
                    stats.posts_per_user[user] = stats.posts_per_user.get(user, 0) + 1
                    stats.posts_len.append(content_len)
                    stats.posts_score.append(score)
                    stats.posts_time.append(full_time)
                    stats.title_len.append(row[TITLE_COL])

                elif row[TYPE_COL] == "C":
                    stats.comments_per_user[user] = stats.comments_per_user.get(user, 0) + 1
                    stats.comments_len.append(content_len)
                    stats.comments_score.append(score)
                    stats.comments_time.append(full_time)
    pickle_path = os.path.join(os.path.dirname(os.getcwd()), STATS_PICKLE_FILE)
    f_handler = open(pickle_path, 'wb')
    pickle.dump(stats, f_handler, pickle.HIGHEST_PROTOCOL)
    f_handler.close()
    write_file.close()
    total_time = (time.time()-start_time)/60

    print("Time Taken to create Stats File = ", '{0:.2f}'.format(total_time) + " minutes")
    os.chdir(os.path.dirname(os.getcwd()))
    return stats



def getAvgPostsPerday(stats):
    return 0
    # return sum(stats.posts_per_day.values())/len(stats.posts_per_day.values())


if __name__ == "__main__":

    # stats = readData(DATA_FOLDER)
    stats = None
    f_handler = open(STATS_PICKLE_FILE, 'rb')
    stats = pickle.load(f_handler)
    f_handler.close()

    #---------------------------------------------------------------------
    print(stats.posts_len)
    print("Average Posts per day = ", getAvgPostsPerday(stats))



