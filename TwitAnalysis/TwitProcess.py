from . import TwitAnalyzer
from . import TwitStream
from textblob import TextBlob

'''
Module for processing twitter data offline
'''
class TwitProcess:
    def __init__(self, config_path=None):
        self.analyzer = TwitAnalyzer(config_path=config_path)
        self._reset()


    def _reset(self):
        self.tweets = []
        self.reg_tweets = 0
        self.retweets = 0 
        self.pos = 0
        self.neg = 0
        self.impact = 0

    # Process bulk twitter data related to specified query
    # max number of tweets processed at once is 100
    def BulkAnalysis(self, query, count):
        self._reset()
        count = min(count,100)
        results = self.analyzer.api.search_tweets(query,result_type='recent',tweet_mode='extended', count=count)
        self.tweets = list(results)

        while len(self.tweets) <= count:
            self.tweets += list(results)
            results = self.analyzer.api.search_tweets(query,count=count, result_type='recent',tweet_mode='extended', max_id=results.max_id)

        for tweet in self.tweets:
            if hasattr(tweet, 'retweeted_status'):
                self.retweets += 1
            else:
                self.reg_tweets += 1

            
            if self._calc_sentiment(tweet) == 1:
                self.pos += 1
            else:
                self.neg += 1

            self._get_impact_raw(tweet)


    def _get_text(self, tweet):
        return tweet.full_text
        # print(tweet)
        # if hasattr(tweet, 'extended_tweet'):
        #     return tweet.extended_tweet['full_text']
        # else:
        #     return tweet.text

    def _calc_sentiment(self, tweet):
        blob = TextBlob(self._get_text(tweet))
        if blob.polarity > 0:
            return 1 
        else:
            return -1

    def _get_impact_raw(self, tweet):
        followers = tweet.author.followers_count
        # for retweet in tweet.retweets():
        #     followers += retweet.author.followers_count
        self.impact += followers


    def get_sentiment(self):
        if self.pos == 0:
            return ( 0, round(self.neg/len(self.tweets)*100,2) )
        if self.neg == 0:
            return ( round(self.pos/len(self.tweets)*100,2), 0 )
        return ( round(self.pos/len(self.tweets)*100,2), round(self.neg/len(self.tweets)*100,2) )

