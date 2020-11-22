#!/bin/sh
clear
python3 NflConverter.py $1 $2
echo $1 $2
python3 main.py $1 $2