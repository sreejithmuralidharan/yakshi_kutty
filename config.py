{
  # Twitter Developer Account keys
    "CONSUMER_KEY" : "",
    "CONSUMER_SECRET" :"",
    "ACCESS_KEY" : "",
    "ACCESS_SECRET" : "",
    
    # Mongo Database password.
    "MONGO_PASSWORD":"",
    
    # Language
    #you can get the 2 digit code from here lhttps://sreejith.co.uk/iso-639-1-language-codes/
    "SEARCH_LANGUAGE":"ml",
    
    # Timer control
    # In order to avoid blacklisting, you need to add delays between calls. 
    # We have already added "wait_on_rate_limit=True, wait_on_rate_limit_notify=True" in the code but its a good practice to add these delays.
    
    "BED_TIME":20, #Program will go to sleep at specified hour. Alternatively you can schedule the call.
    "SLEEP_HOURS":6, #Once you hit the bed time, program will sleep for this much hours.
    "NAP_MINS":15, #Program will take a nap between this mins.
  
    # Quality Control
    # You can set a minmum number of followers required and program will only retweet and will send follow requests in the threshold is met.
    # Otherwise program will only like the tweet.
    
    "MIN_FRIENDS_COUNT_FOR_RETWEET":30
}