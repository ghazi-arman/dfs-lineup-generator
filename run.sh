#!/bin/sh
clear
echo $1 $2 $3
if [ $1 = "NFL" ]; then
  python3 NflConverter.py $2 $3
fi
if [ $1 = "NHL" ]; then
  python3 NhlConverter.py $2 $3
fi
python3 main.py $1 $2 $3