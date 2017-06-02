# dbtools

These are set of tools and utilities developed for social media outreach, Telegram bots etc that we need in my community

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


## Running BotOrNot service


Get mashape and twitter keys/secrets as per https://github.com/IUNetSci/botometer-python

Now this can run very slowly so try to run as per usage given - botratings2.py useranalys0106.csv Opfilename endingAt startingfrom keyfile

        useranalysis0106.csv is the supplied file which has prelim user data

        opfilename is the name the script will write to

        endingAt at which row

        starting from which row.

        key-file has mashape and 4 twitter keys

keyfile should be a python file with following entries

````
# Your mashape_key generated when you add botometer api to default app
mashape_key = ""

# Your twitter account and app keys here
consumer_key=''
consumer_secret=''
access_token_key=''
access_token_secret=''
````


Now we can run this in chunks of 1000 as follows

````
        botrating.py useranalysis0106.csv first1000.csv keyfile 1000   1
        botrating.py useranalysis0106.csv second1000.csv keyfile 2000   1001
        botrating.py useranalysis0106.csv third1000.csv keyfile 3000   2001
        botrating.py useranalysis0106.csv fourth1000.csv keyfile 4000   3001
        ...
        botrating.py useranalysis0106.csv last1000.csv keyfile 10000   9001
````

Note it will be useful to redirect the stdout to a file so that in case things go wrong

you still have the output for the records processed which can be manually merged

````
botrating.py useranalysis0106.csv first1000.csv 1000   1 keyfile > first1000.log
````
