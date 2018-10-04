#!/bin/sh

ls -l logs/ |awk '{print $5 " " $8}' |sort -h
