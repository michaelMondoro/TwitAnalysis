[![Generic badge](https://img.shields.io/badge/Licence-MIT-blue.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Maintained-yes-green.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Python-3.10.6-yellow.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/TwitAnalysis-1.0.15-red.svg)](https://test.pypi.org/project/TwitAnalysis/)

## Purpose
Every individual user on Twitter has a customized, personal experience and only views a tiny portion of the actual conversations, content and opinions that are put out on the platform. The purpose of this project is to provide tools to allow people to use Twitter data to obtain a more holistic perspective of the social network landscape. The TwitAnalysis modules allow for the live processing of Tweet streams as well as processing mass amounts of posted content related to certain topics, trends or users. This allows for analysis of a much larger sample size of Twitter data, allowing us to estimate the impact/reach of Twitter content. Basically, this means that we can go beyond just seeing what our friends are thinking/saying on the platform, and see the opinions of Twitter at large.

## Scope
The scope of the project is limited by a number of different factors which we will attempt to document to allow for transparency. While not necessarily all inclusive, hopefully this can serve as a foundation for Twitter analysis, and a starting point for more targeted projects in the future.

## Functionality
Currently the project is split into two main modules. The `TwitLive` module is used for streaming/processing live Twitter data. The `TwitProcess` module is used for processing bulk Twitter data.


```python
from TwitLive import TwitLive

# Make sure to have your keys/tokens defined in your '.config' file. See example file for details
live = TwitLive(a)
live.TrendAnalysis("United States", 3, False)

```

![tweets](https://user-images.githubusercontent.com/38412172/197245058-916f99d9-5c0d-437d-80e3-158a8e3af039.png)
