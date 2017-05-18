'''
Created on Feb 25, 2017

@author: Gaurav BG
'''

class TweetInfo:
    def __init__(self, ts, createdTime, tweetId, text, keyword, uId, scName, retweetCount, favCount, friendCount, loc, geotag):
        self.ts = ts
        self.createdTime = createdTime
        self.tweetId = tweetId
        self.text = text
        self.keyword = keyword 
        self.uId = uId
        self.scName = scName
        self.retweetCount = retweetCount
        self.favCount = favCount
        self.friendCount = friendCount
        self.loc = loc
        self.geotag = geotag