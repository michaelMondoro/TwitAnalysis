import tweepy
from termcolor import cprint, colored
from textblob import TextBlob

'''
# Custom stream class for streaming live tweet data
# 
# live=True -> streamed tweets will be printed to the console
'''
class TwitStream(tweepy.Stream):
    def __init__(self, consumer_key, consumer_secret, acces_token, access_token_secret, live=True):
        super().__init__(consumer_key, consumer_secret, acces_token, access_token_secret)
        self.tweets = 0
        self.reg_tweets = 0
        self.retweets = 0
        self.is_live = live
        self.unique_retweets = []
        self.pos = 0
        self.neg = 0
        self.impact_raw = 0

    def get_perc_retweets(self):
        return round((self.retweets/self.tweets)*100,2)

    def get_perc_unique_retweets(self):
        if self.retweets == 0:
            return 0
        return round((self.get_unique_retweets()/self.retweets)*100,2)

    def get_unique_retweets(self):
        return len(self.unique_retweets)

    # Gets the sum of followers of the tweet's author as well as any users who retweeted
    def get_impact_raw(self, tweet):
        followers = tweet.author.followers_count
        for retweet in tweet.retweets():
            followers += retweet.author.followers_count

        self.impact_raw += followers

    def print_tweet(self, tweet, text, quoted_text, url, quote_url):
        # Print header for tweet or retweet
        if hasattr(tweet, 'retweeted_status'):
            print(f"{colored(tweet.author.name,'cyan')} retweeted {colored(tweet.retweeted_status.author.name,'yellow')}")

        else:
            print(f"{colored(tweet.author.name,'cyan')} tweeted")

        # Print location if there
        if tweet.author.location:
            print(f"[{colored(tweet.author.location,'magenta')}] --- [{colored(url,'red')}]")
        else:
            print(f"[{colored('***','magenta')}] --- [{colored(url,'red')}]")


        # Print tweet contents
        print(text)

        # Print quote if there
        if hasattr(tweet, 'quoted_status'):
            print(f"\n=====\n{colored(tweet.quoted_status.author.name,'yellow')} - [{colored(quote_url,'red')}]\n{colored(quoted_text,'blue')}\n=====")

        print("---\n\n")

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
    # TODO: update to account for varying levels of polarity
    def get_sentiment(self, tweet):
        blob = TextBlob(self.get_text(tweet))
        if blob.polarity > 0:
            self.pos += 1
        else:
            self.neg += 1

    def on_closed(self, response):
        pass

    def on_status(self, status):
        retweet_text = ""
        retweet_url = ""
        quoted_text = ""
        quote_url = ""

        self.get_sentiment(status)
        self.get_followers(status)
        
        # Get text from retweet
        if hasattr(status, 'retweeted_status'):
            retweet_url = self.get_url(status.retweeted_status)
            retweet_text = self.get_text(status.retweeted_status)
            if status.retweeted_status.id not in self.unique_retweets:
                self.unique_retweets.append(status.retweeted_status.id)

            self.retweets += 1
        else:
            self.reg_tweets += 1
        # Get text from quoted tweet
        if hasattr(status, 'quoted_status'):
            quote_url = self.get_url(status.quoted_status)
            quoted_text = self.get_text(status.quoted_status)

        # Get text from tweet
        url = self.get_url(status)
        text = self.get_text(status)

        if self.is_live:
            if hasattr(status, 'retweeted_status'):
                self.print_tweet(status, retweet_text, quoted_text, retweet_url, quote_url)
            else:
                self.print_tweet(status, text, quoted_text, url, quote_url)

        self.tweets += 1