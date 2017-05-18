#Create the model
#Document Topic distribution (K-dimensional vector)
#create mapping for each topic
#Kmeans Sampling and cluster into k topics


from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import math
import Constants
import numpy as np
import csv

def printScores(true_pos, true_neg, false_pos, false_neg):

    print("--------------------------------------------------------------")
    precision = true_pos / float(true_pos + false_pos)
    print("Precision: ", precision)

    recall = true_pos / float(true_pos + false_neg)
    print("Recall: ", precision)

    f1_score = 2* ((precision * recall) / float(precision + recall))
    print("F1 Score: ", f1_score)




if __name__ == '__main__':

    CLUSTER_SIZE = 25
    topicDistributionFilename = Constants.MODEL_FOLDER_PATH + "k" + str(CLUSTER_SIZE) + ".pz_d"
    with open(topicDistributionFilename) as topicDistFile:
        topicDistLines = topicDistFile.readlines()
    topicDistFile.close()

    data=list()
    no_items = False
    counter = 0
    total_missed  = 0
    missed_indexes = list()
    for line in topicDistLines:
        sub_list = list()
        tokens = line.split()
        no_items = False
        for each in tokens:
            val = float(each)
            if math.isnan(val):
                missed_indexes.append(counter)
                total_missed = total_missed + 1
                no_items = True
                break
            sub_list.append(float(val))
        if no_items is False:
            data.append(sub_list)
        counter = counter + 1

    print("Total missed:", total_missed)

    # tpcs = list()
    # pps = list()
    # for i in range(10, 41):
    #     km = KMeans(n_clusters=i, max_iter=1000)
    #     km.fit(data)
    #     tpcs.append(i)
    #     pps.append(math.fabs(km.score(data)))
    #
    # plt.plot(tpcs, pps)
    # plt.ylabel('KMeans Error Score')
    # plt.xlabel('Topic Count')
    # plt.show()

    fin = csv.reader(open(Constants.FULL_DATA_FOLDER_PATH + "real_full_data.csv", encoding="utf8"))
    all_lines = [l for l in fin]
    all_text = list()

    for line in all_lines:
        all_text.append(line[4])

    # stripped_lines = [v for i, v in enumerate(missed_indexes) if i not in frozenset(all_text)]
    # print(len(stripped_lines))

    km = KMeans(n_clusters=CLUSTER_SIZE, max_iter=1000)
    km.fit(data)

    groups = []
    originalTexts = []
    for i in range(CLUSTER_SIZE):
        group = []
        newGroup = []
        groups.append(group)
        originalTexts.append(newGroup)

    TOPIC_NUMBER = 0

    for index in range(len(data)):
        groups[km.labels_[index]].append(data[index])
        x = sum(i < index for i in missed_indexes)
        originalTexts[km.labels_[index]].append(all_text[index - x])
        # print(all_text[index - x])

    for i in range(len(originalTexts)):
        file = open(Constants.EXAMPLES_FOLDER_PATH + str(i) +".txt", 'w')
        for line in originalTexts[i]:
            print(line)
            print(line, file=file)
        file.close()

    for i in range(len(groups)):
        group = groups[i]
        print("Topic", (i+1), ":", len(group))













