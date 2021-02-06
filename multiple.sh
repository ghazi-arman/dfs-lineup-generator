#!/bin/sh
overlaps=(3 4 5 6)
player_limits=(50 150)
team_limits=(3 4)
if [ $1 = "NFL" ] || [ $1 = "nfl" ]; then
  stacks=()
fi
if [ $1 = "NHL" ] || [ $1 = "nhl" ]; then
  stacks=("3-2-2")
fi
if [ $1 = "NBA" ] || [ $1 = "nba" ]; then
  stacks=("PG-SG" "PG-(SG-SF-PF)" "PG-(SG-SF-PF)-(SG-SF-PF)" "PG-SG+PG-SG" "PG-(SG-SF-PF)+PG-(SG-SF-PF)" "PG-(SG-SF-PF)-(SG-SF-PF)+PG-(SG-SF-PF)-(SG-SF-PF)")
fi
for overlap in "${overlaps[@]}"
do
  for player_limit in "${player_limits[@]}"
  do
    for team_limit in "${team_limits[@]}"
    do
      for stack in "${stacks[@]}"
      do
        if [ ! -e "$1"/outputs/"$2"/output_"$3"_overlap_"$overlap"_playerlimit_"$player_limit"_numteams_"$team_limit"_stack_"$stack"_proj.csv ]; then
          ./run.sh $1 $2 $3 $overlap $player_limit $team_limit $stack
        fi
      done
    done
  done
done