# -*- coding: utf-8 -*-
import tweepy
import sys
from datetime import datetime
import config
from services import mongodb_api, tweepy_api

twitter = tweepy_api()
db_collection = mongodb_api()
document = config.MONGO_LOG_DOCUMENT
db = mongodb_api.document
search_term = "*"

for tweet in tweepy.Cursor(
    twitter.search,
    q=search_term,
    lang=config.SEARCH_LANGUAGE,
    count=config.NO_OF_RECORDS_TO_CRAWL,
    result_type = config.RESULT_TYPE
    ).items(config.NO_OF_RECORDS_TO_CRAWL):
    now = datetime.today().now()
    try:
        friend_request_sent = False
        tweet_fav = False
        tweet_reTweet = False
        fav_error = None
        retweet_error = None
        friend_request_sent_error = None
        if tweet.in_reply_to_screen_name is None and tweet.user.friends_count>=config.MIN_FRIENDS_COUNT_FOR_RETWEET :
            if config.FAVOURITE:
                try:
                    tweet.favorite()
                    tweet_fav= True
                except tweepy.TweepError as e:
                    fav_error = e.reason
            
            if config.RE_TWEET:
                try:
                    tweet.retweet()
                    tweet_reTweet = True
                except tweepy.TweepError as e:
                    retweet_error = e.reason       
            if config.FRIENDSHIP:  
                try:
                    twitter.create_friendship(tweet.user.id)
                    friend_request_sent = True
                except tweepy.TweepError as e:
                    friend_request_sent_error = e.reason          
            if friend_request_sent == tweet_fav == tweet_reTweet == True:
                status = "Success"
            elif friend_request_sent == tweet_fav == tweet_reTweet == False:
                status = "Failed"
            else:
                status = "Partial"
            post_data = {
                'status': status,
                'tweet_id':tweet.id,
                'favorite':tweet_fav,
                'retweet':tweet_reTweet,
                'followed':friend_request_sent,
                'timestamp': datetime.today().now()
            }
            if status == "Failed" or status == "Partial":
                if tweet_fav == False:
                    post_data['fav_error'] = fav_error
                if tweet_reTweet == False:
                    post_data['retweet_error'] = retweet_error
                if tweet_fav == False:
                    post_data['friend_request_sent_error'] = friend_request_sent_error
            else:
                None                           
            db.insert_one(post_data)                 
        else:
            if config.FAVOURITE:
                tweet.favorite()
                tweet_fav= True
                if tweet_fav == True:
                    try:
                        post_data = {
                            'status': 'Success',
                            'favorite':tweet_fav,
                            'timestamp': datetime.today().now()
                        }
                        db.insert_one(post_data)      
                    except tweepy.TweepError as e:
                        post_data = {
                            'status': 'Failed',
                            'message':e.reason,
                            'timestamp': datetime.today().now()
                        }
                    db.insert_one(post_data)      
    except tweepy.TweepError as e:
        post_data = {
            'status': 'Failed',
            'message':e.reason,
            'timestamp': datetime.today().now()
        }
        db.insert_one(post_data)      