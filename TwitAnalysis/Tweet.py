import json 
from . import TwitAnalyzer

class Tweet:
    def __init__(self, analyzer, status):
        self.analyzer = analyzer
        self.date = status.created_at.ctime()
        self.author = { "name":status.author.name, "screen_name":status.author.screen_name }
        self.text = status.full_text
        if hasattr(status, "retweeted_status"):
            self.retweet = Tweet(analyzer, status.retweeted_status)
        else:
            self.retweet = None
        self.hashtags = [i['text'] for i in status.entities['hashtags']]
        self.mentions = [{'screen_name': i['screen_name'], 'name': i['name'], 'id': i['id']} for i in status.entities['user_mentions']]
        self.id = status.id
        self.likes = status.favorite_count
        self.retweets = status.retweet_count
        self.url = self.analyzer.get_url(status)


    def to_json(self):
        return {
            "author" : self.author,
            "text" : self.text,
            "date" : self.date,
            "retweet" : self.retweet,
            "hashtags" : self.hashtags,
            "likes" : self.likes,
            "retweets" : self.retweets,
            "url" : self.url,
            "id" : self.id
        }
