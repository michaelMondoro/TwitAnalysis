import tweepy
import yaml
import os
from requests.utils import unquote
from textblob import TextBlob

'''
# Class for processing and analyzing Tweets
'''
class TwitAnalyzer:
    def __init__(self):
        self.config = None
        self.api = self.init_twitter()
        self.trend_locations = self.get_trend_locations()

    # Calculate sample size to ensure accuracy
    # default margin of error = 3%
    # default confidence interval 95% (1.96)
    def sample_size(self, pop, z=1.96, err=.03):
        numerator = (z**2 * .25) / err**2
        denominator = 1 + (z**2 * .25) / (err**2 * pop)
        return round(numerator/denominator,2)

    # Initialize configuration and twitter API connection
    def init_twitter(self):
        if not os.path.isfile('.config'):
            print("[ ERROR ]: Could not find '.config' file in the current directory")
        with open('.config') as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)
            
        # Initialize twitter connection
        auth = tweepy.OAuthHandler(self.config['CONSUMER_KEY'],self.config['CONSUMER_SECRET'])
        auth.set_access_token(self.config['ACCESS_TOKEN'],self.config['ACCESS_TOKEN_SECRET'])
         
        api = tweepy.API(auth,wait_on_rate_limit=True)
        return api 

    # Get map of available trend locations
    def get_trend_locations(self):
        trend_locations = {}
        trends = self.api.available_trends()

        for trend in trends:
            trend_locations[trend['name']] = {  'woeid': trend['woeid'], 
                                                'parent': trend['parentid']}

        return trend_locations

    # Get trends from given location
    def get_trends(self, woeid):
        trend_info = []
        trends = self.api.get_place_trends(woeid)[0]
        trend_date = trends['created_at']
        for trend in trends['trends']:
            trend_info.append(trend)
            # if trend['tweet_volume'] and trend not in trend_info:
            #     trend_info.append(trend)

        return sorted(trend_info, key=lambda trend: trend['tweet_volume'] if trend['tweet_volume'] is not None else -1, reverse=True)


    # Check if tweet is a retweet
    def is_retweet(self, tweet):
        return tweet.retweeted 

    # Get tweet id
    def tweet_id(self, tweet):
        return tweet.id 

    # Get favorite count of tweet
    def favorite_count(self, tweet):
        return tweet.favorite_count

    # Get number of times this tweet has been retweeted
    def retweet_count(self, tweet):
        return tweet.retweet_count

    # Get tweet source url if it exists
    def tweet_url(self, tweet):
        return f"https://twitter.com/twitter/statuses/{tweet.id}"
    
    # Get location of tweets author if it exists
    def tweet_location(self, tweet):
        if len(tweet.author.location) > 0:
            return tweet.author.location
        return None

    # Get author's follower count
    def follower_count(self, tweet):
        return tweet.author.followers_count

    # Get the url associated with the given tweet
    def get_url(self, tweet):
        return f"https://twitter.com/twitter/statuses/{tweet.id}"

    # Get text associated with the given tweet
    def get_text(self, status):
        if hasattr(status, 'full_text'):
            return status.full_text
        else:
            return status.text

    # Get sentiment of tweet
    # TODO: update to account for sentiment levels? Tuning of the actual sentiment gathered?
    def get_sentiment(self, tweet):
        blob = TextBlob(self.get_text(tweet))
        return blob.polarity

    # Scrape tweets related to specified topic 
    # NOTE: THIS FILTERS RETWEETS
    def get_topic_data(self, topic, max_tweets):
        results = self.api.search_tweets(q=f"{topic} -filter:retweets", result_type='recent',tweet_mode='extended', count=100)
        data = list(results)
        max_id = results.max_id

        while len(data) <= max_tweets:
            print(len(data))
            results = self.api.search_tweets(q=f"{topic} -filter:retweets", result_type='recent',tweet_mode='extended', count=100, max_id=max_id)
            if len(results) == 0:
                print(f"Ran out of Tweets matching search . . . [ {len(data)} ]")
                break
            data += list(results)
            max_id = results.max_id-1

        return data

