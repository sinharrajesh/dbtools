#!/bin/bash
cons_dir=$HOME/gitrepos/DPWPOC2/python-twitter/consolidated

dt=$1
lastTweet=$2
endTweet=$3

echo "making $dt dir and changing to it"
mkdir $dt
cd $dt
echo "copying files across"
cp ../incrtweetwriter.py .
cp ../genincrid.py .
cp ../excelincr.py .
cp ../userincr.py .
cp ../appendpanda.py .
chmod +x *.py

p1_pat='http://www.tandfonline.com/doi/abs/10.1080/03081079.2017.1308361'
p2_pat='http://www.tandfonline.com/doi/full/10.1080/03081079.2017.1308361'
p3_pat='10.1080/03081079.2017.1308361'
p4_pat='http://dx.doi.org/10.1080/03081079.2017.1308361'


echo "grabbing tweets"
../grabincr.py $p1_pat $lastTweet $endTweet > p1_${dt}
echo "press enter to continue"
read x
../grabincr.py $p2_pat $lastTweet $endTweet> p2_${dt}
echo "press enter to continue"
read x
../grabincr.py $p3_pat $lastTweet $endTweet > p3_${dt}
echo "press enter to continue"
read x
../grabincr.py $p4_pat $lastTweet $endTweet > p4_${dt}
echo "press enter to continue"
read x

echo "soring the tweets"
for i in p1_${dt} p2_${dt} p3_${dt} p4_${dt}
do
    ./genincrid.py $i | sort > ${i}_id
done

echo "checking if there is a duplicate tweet"
for i in p1 p2 p3 p4
do
    cnt1=$(cat ${i}_${dt}_id | wc -l)
    cnt2=$(cat ${i}_${dt}_id | sort -u | wc -l)
    if [ ${cnt1} != ${cnt2} ]
    then
       echo "The two counts of outputs for $i do not match $cnt1 and $cnt2"
       read x
    else
       echo "There is no difference in counts of ids in $i"
       read x
    fi
done

echo "Generate common files"
comm -12 p1_${dt}_id p2_${dt}_id  > /tmp/p2common

comm -12 p1_${dt}_id p3_${dt}_id  > /tmp/p3common
comm -12 p2_${dt}_id p3_${dt}_id  >> /tmp/p3common

comm -12 p1_${dt}_id p4_${dt}_id  > /tmp/p4common
comm -12 p2_${dt}_id p4_${dt}_id  >> /tmp/p4common
comm -12 p3_${dt}_id p4_${dt}_id  >> /tmp/p4common

touch p1common
cp /tmp/p2common .
for i in p3 p4
do
   cat /tmp/${i}common | sort -u > ${i}common
done
wc -l p*common
echo "press enter to continue"
read x

echo "Generating upto date picture of altmetric tweet database"
altfile="altmetrictweets${dt}.dat"
/Users/a3126147/gitrepos/dbtools/twitter.py 19547688 tweet > $altfile
echo "written to $altfile"

echo "Gneerating uptp date picture of altmetric users database"
altu="altmetricusers${dt}.dat"
/Users/a3126147/gitrepos/dbtools/twitter.py 19547688 user > $altu
echo "written to $altu"

echo "Now printing things after checking common stuff"
opfile=tweets_${dt}.tmp
opfinfile=tweets_${dt}.csv
for i in p1 p2 p3 p4
do
    commfile=${i}common
    echo "firing for ${i}_${dt} with $commfile"
    ./excelincr.py ${i}_${dt} $commfile $altfile >> $opfile
    #read x
done
sort -n $opfile > $opfinfile
echo "final tweets in $opfinline file"

echo "Generating unique users now"
userfile=useractivity_${dt}.csv
./userincr.py $opfinfile > $userfile 
echo "unique users in $userfile"

ltfile="./LASTTWEET_${dt}"
x=`cat $opfinfile | tail -1 | awk -F'$' '{print $1}'`
echo $x >$ltfile
echo "LAST-TWEET no in $ltfile

#echo "Generating pivot table for useranalysis"
#useranalysis="useranalysis${dt}"
#./appendpanda.py $userfile $opfinline $useranalysis
#echo "output in $output"

#echo "Botometer readings not yet done but can be run later"

ecgo "Updated Altmetric tweets ids in $altfile"
echo "All Tweets in $opfinfile"
echo "All Users in $userfile"
echo "Useranalysis in $useranalysis"
