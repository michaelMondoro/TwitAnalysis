from . import TwitAnalyzer
from . import TwitStream

'''
Module for processing twitter data offline
'''
class TwitProcess:
    def __init__(self):
        self.analyzer = TwitAnalyzer()
    

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
            