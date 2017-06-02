#!/bin/bash
BASEPATHALT="/Users/a3126147/gitrepos/dbtools/altmetric/"
$pwd
p1_pat='http://www.tandfonline.com/doi/abs/10.1080/03081079.2017.1308361'
p2_pat='http://www.tandfonline.com/doi/full/10.1080/03081079.2017.1308361'
p3_pat='10.1080/03081079.2017.1308361'
p4_pat='http://dx.doi.org/10.1080/03081079.2017.1308361'

dt=$1
mkdir $dt
echo "grabbing tweets"
./dumpgpost.py $p1_pat > p1_${dt}
./dumpgpost.py $p2_pat > p2_${dt}
./dumpgpost.py $p3_pat > p3_${dt}
./dumpgpost.py $p4_pat > p4_${dt}

echo "sorting the posts"
for i in p1_${dt} p2_${dt} p3_${dt} p4_${dt}
do
    cat $i | sort -u > ${i}_id
done

echo "comparing"
for i in p1_${dt} p2_${dt} p3_${dt} p4_${dt}
do
    wc -l $i ${i}_id
done

echo "Generate common files"
cat p1_${dt}_id p2_${dt}_id p3_${dt}_id p4_${dt}_id | sort -u > g${dt}_fin

wc -l g${dt}_fin

cat g${dt}_fin | sed "s/u\'/\'/g" > gpost${dt}.tmp
echo "int output in gpost${dt}.tmp"

echo "finding google+ posts ids in altmetric as of date"
altfile=${BASEPATHALT}"data/altmetricgplus${dt}.csv"
./gplus.py 19547688 posts > $altfile
echo "Press to continue"
read

echo "finding google+ posts dumps in altmetric as of date"
altffile=${BASEPATHALT}"data/altmetricgplusfull${dt}.csv"
./gplusextended.py 19547688 posts > $altffile

echo "finding google+ users altmetric as of date"
altu=${BASEPATHALT}"data/altmetricgplususers${dt}.csv"
./gplus.py 19547688 user > $altu

echo "finding which google+ posts exist in altmetric"
./clarify.py $altfile gpost${dt}.tmp > gpost${dt}.csv

echo "final files in gpost${dt}.csv"
mv gpost${dt}.csv $dt
mv gpost${dt}.tmp $dt
mv g${dt}_fin $dt
for i in p1 p2 p3 p4
do
    mv ${i}_${dt} $dt
    mv ${i}_${dt}_id $dt
done

echo "** Look into $dt directory and gpost${dt}.csv file for all data***"
