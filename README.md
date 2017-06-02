# dbtools

** Dayalbagh Tools and scripts **
These are set of tools and utilities developed for social media outreach, Telegram bots etc that we need in Dayalbagh as tech infusion.

## Altmetric directory

you can run variety of scripts from here

````
twitter.py <altmetricId> [user|tweet] 
````
This will dump either user handles or tweet ids on the standard output given a specific altmetric document id


````
gplus.py <altmetricId> [user|post] 
````
This will dump either user names/g+ ids or post urls on the standard output given a specific altmetric document id


````
gplusextended.py <altmetricId> post 
````
This will dump all possible information that altmetric has about a googple+ post on standard output


all the above three are CSV files delimited by $


## Altmetrc data directory

This is a running directory which stores data as gathered from several scripts 

usually they will be marked with altmetric[gplus][date].csv 

## google-plus-analysis

Best to run and read the following script as shown

````
./mainscript.sh DDMM 
````

This will search for all 4 patterns in Google Plus and dump them in DDMM/gpost${dt}.csv file 

It will also create altmetrics updated data in altmetric/data/altmetricgplus[users|posts|full]$dt.csv files for that date



