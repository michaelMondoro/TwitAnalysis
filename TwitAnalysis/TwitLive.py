# from . import TwitAnalyzer
# from . import TwitStream
from time import sleep
from progress.spinner import *
from prettytable import *
from termcolor import cprint, colored

"""
Module for processing live twitter data
"""

class TwitLive:

    def __init__(self, analyzer=None):
        """
        Class used for analyzing live Twitter data

        Parameters
        -------
        analyzer : TwitAnalyzer
            Analyzer used for making calls to Twitter api

            If an analyzer is not provided, a new one will be created

        """
        if analyzer == None:
            self.analyzer = TwitAnalyzer()
        else:
            self.analyzer = analyzer
            
    
    def stream(self, query, live):
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
            
        twit_stream = TwitStream(self.analyzer.config['CONSUMER_KEY'],self.analyzer.config['CONSUMER_SECRET'],self.analyzer.config['ACCESS_TOKEN'],self.analyzer.config['ACCESS_TOKEN_SECRET'], live=live)
        
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
        total_tweets = 0
        total_reg_tweets = 0
        total_retweets = 0
        total_unique_retweets = 0
        total_volume = 0

        if num_trends == 'all':
            num_trends = len(trends)

        print(f"Gathering data on top {num_trends} trends from [ {location} ]")
        for i, trend in enumerate(trends[:num_trends]):
            # Start stream and print status
            streem, thread = self.stream(trend['name'], display)
            if not display:
                self.progress(f" {i+1}/{num_trends} [ {colored(trend['name'],'magenta')} ] - Volume: {trend['tweet_volume']:,} ", 30)
            else:
                print(f" {i+1}/{num_trends} [ {trend['name']} ] - Volume: {trend['tweet_volume']:,}")
                sleep(30)
            

            # Disconnect stream and wait for thread to finish
            streem.disconnect()
            thread.join()

            total_tweets += streem.tweets
            total_reg_tweets += streem.reg_tweets
            total_retweets += streem.retweets
            total_unique_retweets += streem.get_unique_retweets()
            total_volume += trend['tweet_volume']
            
            data[trend['name']] = { 'tweets':streem.tweets,
                                    'reg_tweets':streem.reg_tweets,
                                    'retweets':streem.retweets, 
                                    'unique_retweets':streem.get_unique_retweets(),
                                    'perc_retweets':streem.get_perc_retweets(),
                                    'perc_unique_retweets':streem.get_perc_unique_retweets(),
                                    'sentiment':( round(streem.pos/streem.tweets*100,2), round(streem.neg/streem.tweets*100,2) ),
                                    'tw_p_min': streem.tweets*2}


        # Create results table
        table = PrettyTable(['Trend', 'Total Tweets', 'Sentiment % (+/-)', 'Regular Tweets', 'Retweets', 'Unique Retweets', 'twt/min', '% Retweets', '% Unique Retweets'])
        table.set_style(SINGLE_BORDER)
        table.align = 'l'

        for trend in data:
            table.add_row([trend, data[trend]['tweets'], data[trend]['sentiment'], data[trend]['reg_tweets'], data[trend]['retweets'], data[trend]['unique_retweets'], data[trend]['tw_p_min'], data[trend]['perc_retweets'], data[trend]['perc_unique_retweets']])
        table.add_row(['Summary', total_tweets, '', total_reg_tweets, total_retweets, total_unique_retweets, round(total_tweets/(num_trends/2)), round((total_retweets/total_tweets)*100,2), round((total_unique_retweets/total_retweets)* 100,2)])    

        print("\n")
        print(f"Summary of top {num_trends} trends from [ {colored(location,'magenta')} ]")
        print(table)
        print(f"\nProcessed {round((total_tweets/total_volume)*100,4)}% of total volume - [ {total_tweets:,} tweets ]")
        print(f"[{total_reg_tweets} regular ] [ {total_retweets} retweets ] [ {total_unique_retweets} unique retweets ]")
        print("\n")



    # Process live twitter search data
    def SearchAnalysis(self):
        """ Analyze live data based on search

        TODO
        ----

        """
        pass
