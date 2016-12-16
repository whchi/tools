#!/usr/bin/sh

top5ipFile='top5trim.log'

#check top 5 access ip
echo '===========top5 ip============='
awk '{print $1}' $1 |sort|uniq -c |sort -nr|head -5
awk '{print $1}' $1 |sort|uniq -c |sort -nr|head -5 > 'top5.log'

#put trim result into file
cat top5.log|sed -e 's/^[[:space:]]*//'| cut -d ' ' -f 2,4,6,8,10 > $top5ipFile

exec < $top5ipFile
while read line
do
    echo '======================================'$line'=========================================='
    echo '[top 5 request uri]'
    grep "$line" $1|awk '{print $7}'|sort|uniq -c|sort -nr|head -5
    echo '[All request method]'
    grep "$line" $1|awk '{print $6}'|cut -d'"' -f2|sort|uniq -c|sort -nr
    echo '[All status]'
    grep "$line" $1|awk '{print $9}'|sort|uniq -c|sort -nr
done
