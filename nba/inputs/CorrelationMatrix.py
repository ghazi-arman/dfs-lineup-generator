import os
import sys
import csv
import pandas as pd

directory = "./{}/".format(sys.argv[1])
sub_directories = [f.path for f in os.scandir(directory) if f.is_dir()]
players = {}

for dir in sub_directories:
  with open(dir+"/players.csv",'rt') as f:
    data = csv.reader(f)
    for row in data:
      # if row is the header skip
      if row[0] == 'Player':
        continue
      else:
        name = row[0]
        if name in players:
          scores = players[name]
          scores[dir] = row[28]
          players[name] = scores
        else:
          scores = {}
          scores[dir] = row[28]
          players[name] = scores

scores_table = pd.DataFrame(columns=(players.keys()))
for dir in sub_directories:
  scores = []
  for key in players.keys():
    if dir in players[key] and players[key][dir] != "":
      scores.append(float(players[key][dir]))
    else:
      scores.append(0.0)
  scores_table.loc[dir] = scores

with open(directory+"correlation.csv", mode='w') as file:
  writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  players_names = [*players]
  players_names.insert(0, "Name")
  writer.writerow(players_names)
  for player_one in players.keys():
    correlation = []
    correlation.append(player_one)
    for player_two in players.keys():
      correlation.append(str(scores_table[player_one].corr(scores_table[player_two])))
    writer.writerow(correlation)