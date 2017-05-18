from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import Constants

import csv
import re

filenames = ["Alberta_Floods.csv", "Boston_Bombings.csv", "Oklahoma_Tornado.csv", "Queensland_Floods.csv", "Sandy_Hurricane.csv", "West_Texas_Explosion.csv"]
# [5189, 5648, 4827, 5414, 6138, 5246]
lemmatizer = WordNetLemmatizer()
all_lines = list()
counts = list()

for fn in filenames:
    fin = csv.reader(open(Constants.FULL_DATA_FOLDER_PATH + fn, encoding="utf8"))
    lines = [l for l in fin]
    counter = 0
    for line in lines:
        if line[2] == "on-topic":
            counter = counter+1
            all_lines.append(line)
    counts.append(counter)

stops = set(stopwords.words("english"))
stops.add("im")
stops.add("rt")

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

print("Counts:", counts)
output = []
for line in all_lines:
    # print("Before: ", line[4])
    filtered = filter_text(line[1])
    # print("After: ", filtered)
    output.append(filtered)


file = open(Constants.FULL_DATA_FOLDER_PATH + "dataset.txt", 'w')
for line in output:
    print(line, file=file)

file.close()

