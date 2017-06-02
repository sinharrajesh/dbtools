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
This will dump all possible information that altmetric has about a google+ post on standard output


all the above three are CSV files delimited by $


## Altmetric data directory

This is a running directory which stores data as gathered from several scripts 

usually they will be marked with altmetric[gplus][date].csv 

## google-plus-analysis

Best to run and read the following script as shown

````
./mainscript.sh DDMM 
````

This will search for all 4 patterns in Google Plus and dump them in DDMM/gpost${dt}.csv file 

It will also create altmetrics updated data in altmetric/data/altmetricgplus[users|posts|full]$dt.csv files for that date


Note that you will need to add config.py file with API_KEY=BlahBlah from google+ API console to make it work


## Twitter analysis directory

This is a running directory which stores data as gathered from several scripts

Usually we will need to gather incremental data for a specific date since a last tweet

find the last tweet from DDMM directory which is the last by finding the file LASTTWEET in that

then run the genincr.sh script as follows

````
./genincr.sh DDMM LASTTWEETID
````

It will do many things like follows
* Create a directory DDMM 
* create a file  altmetrictweets${dt}.csv in dbtools/altmetric/data/ directory
* create a file  altmetrictweetuserss${dt}.csv in dbtools/altmetric/data/ directory
* creats a file  tweets_${dt} in DDMM directory - These are incremental tweets since the last tweet
* creates  file  usersctivity_${dt} in DDMM directory - these are incremental user stats since the last tweet

Once done we need to add these incremental stuff to consolidated files kept in data/cons directory

Find the last alltweetsDDMM.csv which can be used and then cat the new tweets underneath it

````
cat oalltweets{oldDDMM].csv tweets_DDMM.csv > alltweetsDDMM.csv
````

Similarly you cat the users 

````
cd cons
cat allusers{oldDDMM}.csv useractivity_DDMM.csv > /tmp/allusersDDMM.csv
./userincr.py /tmp/allusersDDMM.csv > allusersDDMM.csv
````

Once done we run some pivot table stats on this to get some data out. The way to do that is from twitter-analysis directory

````
./appendpanda.py allusersDDMM.csv alltweetsDDMM.csv > cons/useractivityDDMM.csv
````

If you wish you can use the script called botratings2.py to run bot or not against it - but it is slow

