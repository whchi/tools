#!/bin/sh

cmd=/usr/local/bin/mosquitto_sub
host=127.0.0.1
topic=test
logfile=$(pwd)/logs/device.log
port=1883
for i in $(seq 1 $1);
do
   ${cmd} -h ${host} -t ${topic}/${i} -p ${port} -q $2 >> ${logfile}_${i} 2>&1 &
done
