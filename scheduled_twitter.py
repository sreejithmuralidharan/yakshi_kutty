# -*- coding: utf-8 -*-
import tweepy
import time
import os
import json
from datetime import datetime
import csv
import pymongo
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(dir_path, 'config.json')

try:
    with open(config_file, 'r') as f:
        config = json.load(f)
    consumer_key = config["CONSUMER_KEY"]
    consumer_secret = config["CONSUMER_SECRET"]
    access_key = config["ACCESS_KEY"]
    access_secret = config["ACCESS_SECRET"]
    mongo_password = config["MONGO_PASSWORD"]
    search_language = config['SEARCH_LANGUAGE']
    bed_time = config['BED_TIME']
    sleep_hours = config['SLEEP_HOURS']
    nap_mins = config['NAP_MINS']
    min_friends_count_for_retweet = config['MIN_FRIENDS_COUNT_FOR_RETWEET']
except:
    sys.exit("Unable to load configuration file")   


def initiate_api():
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        return api
    except tweepy.TweepError as e:
        sys.exit(e.reason)

def connect_mongodb():
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        connection_url = "mongodb+srv://sreejith:"+ mongo_password +"@cluster0.74jps.mongodb.net/"
        client = pymongo.MongoClient(connection_url)
        db = client.Crawlikutty
        mongo_db = db.yakshi_kutty
        return mongo_db
    except:
        sys.exit("Unable to create connection to database")

twitter = initiate_api()
mongo_db = connect_mongodb()
search_term = "*"

for tweet in tweepy.Cursor(twitter.search, q=search_term, lang=search_language, count=1, result_type = 'recent').items(1):
    now = datetime.today().now()
    try:
        friend_request_sent = False
        tweet_fav = False
        tweet_reTweet = False
        fav_error = None
        retweet_error = None
        friend_request_sent_error = None
        if tweet.in_reply_to_screen_name is None and tweet.user.friends_count>=min_friends_count_for_retweet :
            try:
                tweet.favorite()
                tweet_fav= True
            except tweepy.TweepError as e:
                fav_error = e.reason
            try:
                tweet.retweet()
                tweet_reTweet = True
            except tweepy.TweepError as e:
                retweet_error = e.reason
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
            mongo_db.insert_one(post_data)                      
        else:
            tweet.favorite()
            tweet_fav= True
            if tweet_fav == True:
                try:
                    post_data = {
                        'status': 'Success',
                        'favorite':tweet_fav,
                        'timestamp': datetime.today().now()
                    }
                    mongo_db.insert_one(post_data)      
                except tweepy.TweepError as e:
                    post_data = {
                        'status': 'Failed',
                        'message':e.reason,
                        'timestamp': datetime.today().now()
                    }
                    mongo_db.insert_one(post_data)      
    except tweepy.TweepError as e:
        post_data = {
            'status': 'Failed',
            'message':e.reason,
            'timestamp': datetime.today().now()
        }
        mongo_db.insert_one(post_data)      
