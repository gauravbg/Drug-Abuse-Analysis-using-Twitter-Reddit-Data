from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import Constants
import matplotlib.pyplot as plt

import csv
import re


USER_NAME_COL = 7
KEYWORD_COL = 5
usersDict = dict()
keywordDict = dict()
keywords = ["marijuana", "reefer", "weed", "cannabis", "hemp", "smoke", "ganja"]

lemmatizer = WordNetLemmatizer()
fin = csv.reader(open(Constants.FULL_DATA_FOLDER_PATH + "real_full_data.csv", encoding="utf8"))
all_lines = [l for l in fin]
print("Total tweets count:", len(all_lines))

stops = set(stopwords.words("english"))
stops.add("im")
stops.add("amp")
for each in keywords:
    stops.add(each)


def filter_text(text):
    filtered_text = ""
    words = word_tokenize(text)
    # words = text.split(" ")
    new_words = []
    for i in range(0,len(words)):
        words[i] = words[i].strip().lower()
        lemmatized_word = lemmatizer.lemmatize(words[i])
        words[i] = lemmatized_word
        if words[i].startswith('http') or words[i].startswith('@') or words[i] in stops:
            pass
        else:
            new_words.append(words[i])

    text = " ".join(new_words)
    #keep only informative characters
    filtered_text = re.sub('[^a-z|A-Z|\s]', '', text)
    filtered_text = filtered_text.strip()
    return filtered_text


output = []
for line in all_lines:
    if line[USER_NAME_COL] not in usersDict:
        usersDict[line[USER_NAME_COL]] = 1
    else:
        usersDict[line[USER_NAME_COL]] += 1

    if line[KEYWORD_COL] not in keywordDict:
        keywordDict[line[KEYWORD_COL]] = 1
    else:
        keywordDict[line[KEYWORD_COL]] += 1

    # print("Before: ", line[4])
    filtered = filter_text(line[4])
    # print("After: ", filtered)
    output.append(filtered)


file = open(Constants.FULL_DATA_FOLDER_PATH + "dataset.txt", 'w')
for line in output:
    print(line, file=file)

file.close()
print("Unique Users Count:", len(usersDict))
print("Keywords counts:", keywordDict)


