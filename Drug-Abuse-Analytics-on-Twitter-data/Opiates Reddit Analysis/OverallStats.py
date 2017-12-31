import os
import csv

directory = os.listdir('/home/gauravbg/SBU-fall-17/CSE-524/Praw_Reddit_Data_Extractor/output')
os.chdir('/home/gauravbg/SBU-fall-17/CSE-524/Praw_Reddit_Data_Extractor/output')
submissions_count = 0
comments_count = 0
files_count = 0
all_posts = []
users = set()
for file in directory:
    files_count+= 1
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            users.add(row[3])
            if row[1] == 'S':
                submissions_count += 1
                all_posts.append(row)
            elif row[1] == 'C':
                comments_count += 1

posts_file_path = '/home/gauravbg/SBU-fall-17/CSE-524/Praw_Reddit_Data_Extractor/posts.csv'
with open(posts_file_path, 'w') as posts_file:
   writer = csv.writer(posts_file)
   writer.writerows(all_posts)

print("Stats: ", comments_count, " : ", submissions_count, " : ", files_count, " : ", len(users))


