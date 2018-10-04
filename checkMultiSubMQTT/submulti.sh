#!/bin/sh

cmd=/usr/local/bin/mosquitto_sub
host=127.0.0.1
topic=multi
logfile=$(pwd)/logs/mqttlog.log
port=1883
for i in $(seq 1 $1);
do
   ${cmd} -h ${host} -t ${topic} -p ${port} -q $2 >> ${logfile}_${i} 2>&1 &
done
