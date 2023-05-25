[![Generic badge](https://img.shields.io/badge/Licence-MIT-blue.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Maintained-yes-green.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Python-3.10.6-yellow.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/TwitAnalysis-1.0.22-red.svg)](https://pypi.org/project/TwitAnalysis/)

## Purpose
Every individual user on Twitter has a customized, personal experience and only views a tiny portion of the actual conversations, content and opinions that are put out on the platform. The purpose of this project is to provide tools to allow people to use Twitter data to obtain a more holistic perspective of the social network landscape. The TwitAnalysis modules allow for the live processing of Tweet streams as well as processing mass amounts of posted content related to certain topics, trends or users. This allows for analysis of a much larger sample size of Twitter data, allowing us to estimate the impact/reach of Twitter content. Basically, this means that we can go beyond just seeing what our friends are thinking/saying on the platform, and see the opinions of Twitter at large.

## Scope
The scope of the project is limited by a number of different factors which we will attempt to document to allow for transparency. While not necessarily all inclusive, hopefully this can serve as a foundation for Twitter analysis, and a starting point for more targeted projects in the future.

## Functionality
Currently the project is split into two main modules. The `TwitLive` module is used for streaming/processing live Twitter data. The `TwitProcess` module is used for processing bulk Twitter data.

**TwitLive** Example
```python
from TwitAnalysis import *
from time import sleep

live = TwitLive()

# Process and display trend analysis
live.TopTrendAnalysis("United States",2,False, 30)
live.trends_summary()

# Stream tweets based on search
stream = live.SearchAnalysis("healthcare",False)
sleep(10)
stream.disconnect()

live.search_summary(stream)

```

![tweets](https://user-images.githubusercontent.com/38412172/210646662-c83fcbfc-68e6-422e-a47e-a81fa1227d3a.png)

**TwitProcess** Example
```python
from TwitAnalysis import *

# Initialize new process object with a specific query
p = TwitProcess("Python Programming")
# Search/Process Tweets
p.bulk_analysis(700)

# Display stats for search results
print("Stats for query: 'Python Programming'")
print(f"Sentiment: {p.overall_sentiment()}")
print(f"Retweets: {p.retweets}")
print(f"Tweets: {p.reg_tweets}")
print(f"Impact: {p.impact}")

```
```
#==== OUTPUT ====#
Stats for query: 'Python Programming'
Sentiment: -0.366
Retweets: 485
Tweets: 282
Impact: 6,228,425
```


-----

**Twitter Documentation**

https://developer.twitter.com/en/docs/tutorials/building-high-quality-filters

**Research**

https://www.sciencedirect.com/science/article/pii/S0268401218306005
https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-018-0178-0
