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
        TwitAnalyzer : analyzer 
            Analyzer used for making calls to Twitter api

            If an analyzer is not provided, a new one will be created

        """
        if analyzer == None:
            self.analyzer = TwitAnalyzer(config_path=config_path)
        else:
            self.analyzer = analyzer

        # Latest search stream
        self.search_stream = None
        # List of latest trends processed
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
            number of seconds to stream 
        """
        spin = PixelSpinner(text)
        for i in range(secs*4):
            spin.next()
            sleep(.25)
        spin.finish()

    def SearchAnalysis(self, query, display):
        """ Process live twitter search data

        Parameters
        ----------
        string : query
            search query to stream live data
        boolean : display 
            boolean to indicate whether or not to display live stream output to the console
        """

        print(f"Starting stream based on search : [ {colored(query,'magenta')} ]")
        # Start stream and print status
        stream, thread = self.stream(query, None, display)

        self.search_stream = stream
        return stream


    def TopTrendAnalysis(self, location, num_trends, display, time):
        """ Process top trends on Twitter

        Parameters
        ----------
        string : location
            location for which to analyze trends from
        int : num_trends
            number of trends to analyze
        boolean : display 
            boolean to indicate whether or not to display live stream output to the console
        int : time 
            time (in seconds) to spend gathering live data for each trend

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
                self.progress(f" {i+1}/{num_trends} [ {colored(trend['name'],'magenta')} ] - Volume: {trend['tweet_volume']:,} ", time)
            else:
                print(f" {i+1}/{num_trends} [ {trend['name']} ] - Volume: {trend['tweet_volume']:,}")
                sleep(time)
            

            # Disconnect stream and wait for thread to finish
            streem.disconnect()
            thread.join()

            self.trend_streams.append(streem)

        


    def search_summary(self, search_stream=None):
        """ Generate summary of search analysis

        """
        if search_stream != None and not isinstance(search_stream, TwitStream):
            print('Invalid parameter . . .')
            return 

        if search_stream == None:
            search_stream = self.search_stream
            if self.search_stream == None:
                print('No search to summarize . . .')
                return 

        # Create results table
        table = PrettyTable(['Search', 'Total Tweets', 'Sentiment % (+/-)', 'Regular Tweets', 'Retweets', 'Unique Retweets', 'twt/min', '% Retweets', '% Unique Retweets'])
        table.set_style(SINGLE_BORDER)
        table.align = 'l'

        sentiment = search_stream.get_sentiment()
        table.add_row([search_stream.name, search_stream.tweets, sentiment, search_stream.reg_tweets, search_stream.retweets, search_stream.get_unique_retweets(), search_stream.tweets*2, search_stream.get_perc_retweets(), search_stream.get_perc_unique_retweets()])
        
        print(f"Summary for search [ {colored(search_stream.name,'magenta')} ]")
        print(table)

    def trends_summary(self):
        """ Generate summary of top trend analysis

        """

        if self.trend_streams == []:
            print('No trends to summarize . . .')
            return

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

            sentiment = trend.get_sentiment()
            table.add_row([trend.name, trend.tweets, sentiment, trend.reg_tweets, trend.retweets, trend.get_unique_retweets(), trend.tweets*2, trend.get_perc_retweets(), trend.get_perc_unique_retweets()])


        table.add_row(['Summary', total_tweets, '', total_reg_tweets, total_retweets, total_unique_retweets, round(total_tweets/(len(self.trend_streams)/2)), round((total_retweets/total_tweets)*100,2), round((total_unique_retweets/total_retweets)* 100,2)])    

        print("\n")
        print(f"Summary of top {len(self.trend_streams)} trends from [ {colored(self.trend_location,'magenta')} ]")
        print(table)
        print(f"\nProcessed {round((total_tweets/total_volume)*100,4)}% of total volume - [ {total_tweets:,} tweets ]")
        print(f"[{total_reg_tweets} regular ] [ {total_retweets} retweets ] [ {total_unique_retweets} unique retweets ]")
        print("\n")



