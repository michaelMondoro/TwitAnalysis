from . import TwitAnalyzer
from . import TwitStream
from time import sleep
from progress.spinner import *
from prettytable import *
from termcolor import cprint, colored

"""
Module for processing live twitter data
"""

class TwitLive:

    def __init__(self, analyzer=None, config_path=None):
        """
        Class used for analyzing live Twitter data

        Parameters
        -------
        analyzer : TwitAnalyzer
            Analyzer used for making calls to Twitter api

            If an analyzer is not provided, a new one will be created

        """
        if analyzer == None:
            self.analyzer = TwitAnalyzer(config_path=config_path)
        else:
            self.analyzer = analyzer

        self.search_stream = None
        self.trend_streams = []
    
    def stream(self, query, volume, live):
        """ Create and start a live Tweet stream 

        Parameters
        ----------
        string : query
            Start stream based on the given string
        boolean : live
            Indicate whether or not live data is printed to the terminal

        Returns
        -------
        tuple: (stream, thread)
            Returns TwitStream object and Thread object

        Note
        ----
        Do not include the `self` parameter in the ``Parameters`` section.
        """
            
        twit_stream = TwitStream(self.analyzer.config['CONSUMER_KEY'],self.analyzer.config['CONSUMER_SECRET'],self.analyzer.config['ACCESS_TOKEN'],self.analyzer.config['ACCESS_TOKEN_SECRET'], query, volume, live=live)
        
        thread = twit_stream.filter(track=[query], stall_warnings=True, threaded=True)
        return twit_stream, thread

    # Display progress spinner for certain amount of seconds
    def progress(self, text, secs):
        """ Display progress bar in terminal

        Parameters
        ----------
        string : text
            text to display 
        int : secs
            number of seconds to use *NOTE* : function multiplies provided seconds by 4
        """
        spin = PixelSpinner(text)
        for i in range(secs*4):
            spin.next()
            sleep(.25)
        spin.finish()

    # Process live twitter search data
    def SearchAnalysis(self, query, display):
        """ Process live twitter search data

        Parameters
        ----------
        string : query
            search query to stream live data
        boolean : display 
            boolean to indicate whether or not to display live stream output to the console
        """

        # Start stream and print status
        streem, thread = self.stream(query, None, display)
        if not display:
            self.progress(f" Streaming search results for [ {colored(query,'magenta')} ] ", 30)
        else:
            print(f" [ {query} ] ")
            sleep(30)

        # Disconnect stream and wait for thread to finish
        streem.disconnect()
        thread.join()

        self.search_stream = streem

    def TrendAnalysis(self, location, num_trends, display):
        """ Process live twitter trend data

        Parameters
        ----------
        string : location
            location for which to analyze trends from
        int : num_trends
            number of trends to analyze
        boolean : display 
            boolean to indicate whether or not to display live stream output to the console
        """

        trends = self.analyzer.get_trends(self.analyzer.trend_locations[location]["woeid"])
        data={}
        self.trend_location = location

        if num_trends == 'all':
            num_trends = len(trends)

        print(f"Gathering data on top {num_trends} trends from [ {location} ]")
        for i, trend in enumerate(trends[:num_trends]):
            # Start stream and print status
            streem, thread = self.stream(trend['name'], trend['tweet_volume'], display)
            if not display:
                self.progress(f" {i+1}/{num_trends} [ {colored(trend['name'],'magenta')} ] - Volume: {trend['tweet_volume']:,} ", 30)
            else:
                print(f" {i+1}/{num_trends} [ {trend['name']} ] - Volume: {trend['tweet_volume']:,}")
                sleep(30)
            

            # Disconnect stream and wait for thread to finish
            streem.disconnect()
            thread.join()

            self.trend_streams.append(streem)

        


    def search_summary(self):
        # Create results table
        table = PrettyTable(['Search', 'Total Tweets', 'Sentiment % (+/-)', 'Regular Tweets', 'Retweets', 'Unique Retweets', 'twt/min', '% Retweets', '% Unique Retweets'])
        table.set_style(SINGLE_BORDER)
        table.align = 'l'

        sentiment = ( round(self.search_stream.pos/self.search_stream.tweets*100,2), round(self.search_stream.neg/self.search_stream.tweets*100,2) )
        table.add_row([self.search_stream.name, self.search_stream.tweets, sentiment, self.search_stream.reg_tweets, self.search_stream.retweets, self.search_stream.get_unique_retweets(), self.search_stream.tweets*2, self.search_stream.get_perc_retweets(), self.search_stream.get_perc_unique_retweets()])
        
        print(f"Summary for search [ {colored(self.search_stream.name,'magenta')} ]")
        print(table)

    def trends_summary(self):
        total_tweets = 0
        total_reg_tweets = 0
        total_retweets = 0
        total_unique_retweets = 0
        total_volume = 0


        # Create results table
        table = PrettyTable(['Trend', 'Total Tweets', 'Sentiment % (+/-)', 'Regular Tweets', 'Retweets', 'Unique Retweets', 'twt/min', '% Retweets', '% Unique Retweets'])
        table.set_style(SINGLE_BORDER)
        table.align = 'l'

        for trend in self.trend_streams:
            total_tweets += trend.tweets
            total_reg_tweets += trend.reg_tweets
            total_retweets += trend.retweets
            total_unique_retweets += trend.get_unique_retweets()
            total_volume += trend.volume

            sentiment = ( round(trend.pos/trend.tweets*100,2), round(trend.neg/trend.tweets*100,2) )
            table.add_row([trend.name, trend.tweets, sentiment, trend.reg_tweets, trend.retweets, trend.get_unique_retweets(), trend.tweets*2, trend.get_perc_retweets(), trend.get_perc_unique_retweets()])


        table.add_row(['Summary', total_tweets, '', total_reg_tweets, total_retweets, total_unique_retweets, round(total_tweets/(len(self.trend_streams)/2)), round((total_retweets/total_tweets)*100,2), round((total_unique_retweets/total_retweets)* 100,2)])    

        print("\n")
        print(f"Summary of top {len(self.trend_streams)} trends from [ {colored(self.trend_location,'magenta')} ]")
        print(table)
        print(f"\nProcessed {round((total_tweets/total_volume)*100,4)}% of total volume - [ {total_tweets:,} tweets ]")
        print(f"[{total_reg_tweets} regular ] [ {total_retweets} retweets ] [ {total_unique_retweets} unique retweets ]")
        print("\n")



