import tweepy
import yaml
import os
from requests.utils import unquote
from textblob import TextBlob

"""
Class for processing and analyzing Tweets
"""
class TwitAnalyzer:
    def __init__(self, config_path=None):
        """
        Class used for analyzing Twitter data

        Parameters
        ----------
        string : config_path 
            full path to config file used to connect to the Twitter API

            If no config_path is specified, the local directory is checked for a `.config` file

        """

        self.config = None
        self.api = self.init_twitter(config_path=config_path)
        self.trend_locations = self.get_trend_locations()


    def sample_size(self, pop, z=1.96, err=.03):
        """ Calculate sample size to ensure accuracy

        Parameters
        ----------
        int : pop
            population size
        float : z 
            confidence interval
        float : err
            margin of error

        Note
        ----
            default margin of error = 3%
            default confidence interval 95% (1.96)
        """

        numerator = (z**2 * .25) / err**2
        denominator = 1 + (z**2 * .25) / (err**2 * pop)
        return round(numerator/denominator,2)

    def init_twitter(self, config_path):
        """ Initialize configuration and twitter API connection

        Parameters
        ----------
        string : config_path 
            full path to config file used to connect to the Twitter API
        """

        if config_path == None:
            config_path = '.config'

        if not os.path.isfile(config_path):
            print(f"[ ERROR ]: Could not find '{config_path}' file")
        with open(config_path) as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)
            
        # Initialize twitter connection
        auth = tweepy.OAuthHandler(self.config['CONSUMER_KEY'],self.config['CONSUMER_SECRET'])
        auth.set_access_token(self.config['ACCESS_TOKEN'],self.config['ACCESS_TOKEN_SECRET'])
         
        api = tweepy.API(auth,wait_on_rate_limit=True)
        return api 

    def get_trend_locations(self):
        """ Get dicionary of available trend locations
        """
        trend_locations = {}
        trends = self.api.available_trends()

        for trend in trends:
            trend_locations[trend['name']] = {  'woeid': trend['woeid'], 
                                                'parent': trend['parentid']}

        return trend_locations

    def get_trends(self, woeid):
        """ Get trends from given location

        Parameters
        ----------
        int : woeid
            WOEID (Where On Earth IDentifier) for the desired location
        """

        trend_info = []
        trends = self.api.get_place_trends(woeid)[0]
        trend_date = trends['created_at']
        for trend in trends['trends']:
            trend_info.append(trend)
            # if trend['tweet_volume'] and trend not in trend_info:
            #     trend_info.append(trend)

        return sorted(trend_info, key=lambda trend: trend['tweet_volume'] if trend['tweet_volume'] is not None else -1, reverse=True)


    def is_retweet(self, tweet):
        """ Check if tweet is a retweet
        """
        return tweet.retweeted 

    def tweet_id(self, tweet):
        """ Get tweet id
        """
        return tweet.id 

    def favorite_count(self, tweet):
        """ Get favorite count of tweet
        """
        return tweet.favorite_count

    def retweet_count(self, tweet):
        """ Get number of times this tweet has been retweeted
        """
        return tweet.retweet_count
    
    def tweet_location(self, tweet):
        """ Get location of tweets author if it exists
        """
        if len(tweet.author.location) > 0:
            return tweet.author.location
        return None

    def follower_count(self, tweet):
        """ Get author's follower count
        """
        return tweet.author.followers_count

    def get_url(self, tweet):
        """ Get the url associated with the given tweet
        """
        return f"https://twitter.com/twitter/statuses/{tweet.id}"

    def get_text(self, tweet):
        """ Get text associated with the given tweet
        """
        if hasattr(tweet, 'full_text'):
            return tweet.full_text
        else:
            return tweet.text

    def get_sentiment(self, tweet):
        """ Get sentiment of tweet

            TODO: update to account for sentiment levels? Tuning of the actual sentiment gathered?
        """
        blob = TextBlob(self.get_text(tweet))
        return blob.polarity

    def get_impact_raw(self, tweet):
        """ Estimate the number of people reached by this tweet

            TODO: also incorporate followers of users who retweeted
        """
        return self.get_followers(tweet)

    def get_followers(self, tweet):
        """ Gets the number of followers the tweet's author has

        """
        return tweet.author.followers_count
        # for retweet in tweet.retweets():
        #     followers += retweet.author.followers_count

    def get_topic_data(self, topic, max_tweets):
        """ Scrape tweets related to specified topic 
        
        Parameters
        ----------
        string : topic
            topic to search for
        int : max_tweets
            number of tweets to process


        Returns
        -------
        list : data
            List of tweet objects related to the search 
        
        Note
        ----
        This method does NOT include retweets

        """
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

