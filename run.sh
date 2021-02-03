#!/bin/sh
clear
echo $1 $2 $3 
echo "overlap" $4
echo "player limit" $5
echo "teams limit" $6
echo "stack" $7
if [ $1 = "NFL" ]; then
  python3 NflConverter.py $2 $3
fi
if [ $1 = "NHL" ]; then
  python3 NhlConverter.py $2 $3
fi
if [ $1 = "NBA" ]; then
  python3 NbaConverter.py $2 $3
fi
python3 main.py $1 $2 $3 $4 $5 $6 $7