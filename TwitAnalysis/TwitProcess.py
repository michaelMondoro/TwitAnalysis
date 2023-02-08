from . import TwitAnalyzer
from . import TwitStream
from textblob import TextBlob

'''
Module for processing twitter data offline
'''
class TwitProcess:
    MAX_COUNT = 100
    def __init__(self, query, config_path=None):
        self.analyzer = TwitAnalyzer(config_path=config_path)
        self._reset()
        self.query = query
        self.max_id = None

    def set_query(self, query, reset=True):
        self.query = query
        if reset:
            self._reset()

    def _reset(self):
        self.tweets = []
        self.reg_tweets = 0
        self.retweets = 0 
        self.pos = 0
        self.neg = 0
        self.impact = 0
        self.max_id = None

    # Process bulk twitter data related to specified query
    # max number of tweets processed at once is 100
    def bulk_analysis(self, count):
        while len(self.tweets) < count:
            results = self.analyzer.api.search_tweets(self.query,count=min(TwitProcess.MAX_COUNT,count), result_type='recent',tweet_mode='extended', max_id=self.max_id)
            self.tweets += list(results)
            self.max_id = results.max_id

        for tweet in self.tweets:
            if hasattr(tweet, 'retweeted_status'):
                self.retweets += 1
            else:
                self.reg_tweets += 1

            
            if self.analyzer.get_sentiment(tweet) > 0:
                self.pos += 1
            else:
                self.neg += 1

            self.impact += self.analyzer.get_impact_raw(tweet)



    def overall_sentiment(self):
        return (self.pos-self.neg)/len(self.tweets)

