#!/bin/sh

ps -aefw |grep quitto_sub|awk '{print $2}'|xargs kill -9
ps -aefw |grep quitto_sub|awk '{print $2}'|xargs kill -9
rm -rf ./logs/*
