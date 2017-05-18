from gensim import corpora, models, similarities
import Constants
from nltk.tokenize import word_tokenize
import csv

tweets = []
file = open(Constants.FULL_DATA_FOLDER_PATH + "dataset.txt", 'r')
lines = file.readlines()
for line in lines:
    words = word_tokenize(line)
    tweets.append(words)

# create dictionary (index of each element)
dictionary = corpora.Dictionary(tweets)
dictionary.save('/tmp/tweets.dict') # store the dictionary, for future reference

# compile corpus (vectors number of times each elements appears)
raw_corpus = [dictionary.doc2bow(t) for t in tweets]
corpora.MmCorpus.serialize('/tmp/tweets.mm', raw_corpus) # store to disk

# STEP 2 : similarity between corpuses
dictionary = corpora.Dictionary.load('/tmp/tweets.dict')
corpus = corpora.MmCorpus('/tmp/tweets.mm')
print(corpus)
lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=25, update_every=1, chunksize=10000, passes=2, alpha= 0.005)
topics = lda.print_topics(25)
for topic in topics:
    print(topic)


fin = csv.reader(open(Constants.FULL_DATA_FOLDER_PATH + "real_full_data.csv", encoding="utf8"))
all_lines = [l for l in fin]
all_text = list()

for line in all_lines:
    all_text.append(line[4])


print("--------------------------------------------------")
examples = []
for i in range(25):
    group = []
    examples.append(group)

topic_dist = lda.get_document_topics(corpus)
for index in range(len(topic_dist)):
    tweet = topic_dist[index]
    h_pr = -1
    h_tp = 0
    for topic in tweet:
        topic_number = topic[0]
        pr = topic[1]
        if pr > h_pr:
            h_pr = pr
            h_tp = topic_number

    examples[h_tp].append(all_text[index])

counter = 0
for i in range(len(examples)):
    counter = 0
    print("Topic ", (i+1), ":", sep="")
    for j in range(2):
        counter = j+1
        print(counter, ". ", examples[i][j], sep="")


for i in range(len(examples)):
    group = examples[i]
    print("Topic", (i + 1), ":", len(group))

for i in range(len(examples)):
    file = open(Constants.LDA_EXAMPLES_FOLDER_PATH + str(i) + ".txt", 'w')
    for line in examples[i]:
        print(line, file=file)
    file.close()


