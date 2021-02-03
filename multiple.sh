#!/bin/sh
overlaps=(3 4 5 6)
player_limits=(10 25 50 100)
team_limits=(3 4 5 6)
for overlap in "${overlaps[@]}"
do
  for player_limit in "${player_limits[@]}"
  do
    for team_limit in "${team_limits[@]}"
    do
      ./run.sh $1 $2 $3 $overlap $player_limit $team_limit $4
    done
  done
done