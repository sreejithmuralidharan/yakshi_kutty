# -*- coding: utf-8 -*-
import tweepy
import sys
import pymongo
import config

def tweepy_api():
    try:
        auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
        auth.set_access_token(config.ACCESS_KEY, config.ACCESS_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        return api
    except tweepy.TweepError as e:
        sys.exit(e.reason)


def mongodb_api():
    try:
        client = pymongo.MongoClient(config.MONGO_URL)
        collection = config.MONGO_DATABASE
        db = client.collection
        return db
    except:
        sys.exit("Unable to create connection to database")