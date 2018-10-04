#!/bin/sh

ps -aefw |grep mosquitto.conf |awk '{print $2}' |xargs kill
