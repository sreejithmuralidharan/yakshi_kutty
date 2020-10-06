from datetime import datetime
from services import tweepy_api, mongodb_api

twitter = tweepy_api()
db = mongodb_api()

quote = db.quotes.find_one( { 'last_used': None } )
print(quote)
if quote is not None:
    try:
        twitter.update_status(quote.get('text'))
        db.quotes.update_one(quote, { "$set": { "last_used": datetime.today().now() } })
        post_data = {
                        'status': 'Success',
                        'action':'Status Post',
                        'message': quote.get('text'),
                        'timestamp': datetime.today().now()
                    }
        db.yakshi_kutty.insert_one(post_data)

    except twitter.TweepError as e:
        post_data = {
                        'status': 'Failed',
                        'action':'Status Post',
                        'message': quote.get('text'),
                        'timestamp': datetime.today().now()
                    }
        db.yakshi_kutty.insert_one(post_data)
