# dbtools

** Dayalbagh Tools and scripts **
These are set of tools and utilities developed for social media outreach, Telegram bots etc that we need in Dayalbagh as tech infusion.

__ Altmetric Readers __

There are two scripts which read and dump data on stdout for tweeter and google plus for a given altmetric articled id

twitter.py altmetric_article_id > tweet.csv   

This will put data in tweet.csv with twitter handles:Name of the tweeter

gplus.py altmetric_article_id > gplus.csv   

This will put data in tweet.csv with either +Gplus Id or  Name of person at the google plus home page

__ About the code base __
[SocialNW.py](https://github.com/sinharrajesh/dbtools/SocialNW.py) has AltmetricBase class which does all the grunt work. Has a template pattern based pipeline method

[twitter.py](https://github.com/sinharrajesh/dbtools/twitter.py) overrides findPosters and can be run from command line for twitter analysis

[gplus.py](https://github.com/sinharrajesh/dbtools/gplus.py) overrides findPosters and can be run from command line for google plus analysis



__ Tweet data analysis __
Pattern-1 http://www.tandfonline.com/doi/abs/10.1080/03081079.2017.1308361        19     tweetdata/abs_data.json

Pattern-2 http://www.tandfonline.com/doi/full/10.1080/03081079.2017.1308361    13493     tweetdata/full_data.json

Pattern-3 10.1080/03081079.2017.1308361                                        14382     tweetdata/10_data.json

Pattern-4 http://dx.doi.org/10.1080/03081079.2017.1308361                       8723     tweetdata/10_data.json


Intersections
p1 intersect p2 = Null
p1 intersect p3 = Null
p1 intersect p4 = Null
p2 intersect p3 = 10709
p2 intersect p4 = 26
p3 intersect p4 = 25
unique across all 4 = 14382


__ Tweeter's status and follower counts __
