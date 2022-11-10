from . import TwitAnalyzer
from . import TwitStream
import redis

'''
Module for processing twitter data offline
'''
class TwitProcess:
    def __init__(self):
        self.analyzer = TwitAnalyzer()
        self.db = redis.Redis()
    

    # Get current data for topic
    def get_data(self, topic):
        return db.hgetall(f"topic:{topic}")

    # Process bulk twitter data related to specified query
    def BulkAnalysis(self, query):
        tweets = analyzer.api.search_tweets(query,count=100)
        for tweet in tweets:
            pass
            # TODO: Sentiment Processing 

            # TODO: Save query data to db
            # db.hset(f"topic:{query}","tweets",tweet.text)
            # db.hset(f"topic:{query}","likes",tweet.favorite_count)
            # db.expire(f"topic:{query}", TIMEOUT)


    # Build database of tweets related to specified topic
    def buildDB(self, query, max_tweets):
        tweet_db = redis.Redis(host='127.0.0.1', port=6379, db=1)
        data = self.analyzer.get_topic_data(query, max_tweets)

        for tweet in data:
            # Extract relevant Tweet data
            sentiment = self.analyzer.get_sentiment(tweet)
            text = self.analyzer.get_text(tweet)
            created_at = tweet.created_at.astimezone().strftime('%m/%d/%Y - %I:%M %p')
            author = tweet.author.name
            screen_name = tweet.author.screen_name
            retweet_count = tweet.retweet_count
            like_count = tweet.favorite_count

            # Store in DB
            tweet_db.hset(f"tweet:{tweet.id}","text",text)
            tweet_db.hset(f"tweet:{tweet.id}","created_at",created_at)
            tweet_db.hset(f"tweet:{tweet.id}","screen_name",screen_name)
            tweet_db.hset(f"tweet:{tweet.id}","author",author)
            tweet_db.hset(f"tweet:{tweet.id}","sentiment",sentiment)
            tweet_db.hset(f"tweet:{tweet.id}","retweets",retweet_count)
            tweet_db.hset(f"tweet:{tweet.id}","likes",like_count)
            