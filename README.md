# Yakshi Kutty
A simple python based multilingual twitter bot that will search trending tweets in a particular language and will fav, retweet and send follow requests.
This bot is expected to run round the clock with some periods of sleep and naps (based on the config file). We will store the results of the program in MongoDb, which can create some cool charts for visualising our data. 
![Alt text](https://github.com/sreejithmuralidharan/yakshi_kutty/blob/master/mongodb_example.png "MongoDb example")
For the simplicity, we will only include process data (i.e. any information about users or tweets won't be saved in the database). You can easily save the tweet info to the database with few lines of codes. I will try to include that in a future version.

## Requirements
- Python3
- tweepy
- dnspython
- pymongo
- git 

## Installation
+ install required libraries

	```bash
	  pip install tweepy
	```
	```bash
	  pip install dnspython
	```
	```bash
	  pip install pymongo
	```
	```bash
	  sudo apt get-install git
	```
  
+ Clone this repo

	```bash
	  git clone https://github.com/sreejithmuralidharan/yakshi_kutty.git
	```

+ Update Config file

+ Run
	```bash
	  python twitter_crawler.py
	```
