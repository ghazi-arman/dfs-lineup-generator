import os
import sys
import csv
import pandas as pd

score_rows = {
  "nba": 28,
  "nfl": 35,
  "nhl": 24
}
directory = "./{}/inputs/{}/".format(sys.argv[1].lower(), sys.argv[2])
sub_directories = [f.path for f in os.scandir(directory) if f.is_dir()]
players = {}

for dir in sub_directories:
  with open(dir+"/players.csv",'rt') as f:
    data = csv.reader(f)
    count = 0
    for row in data:
      if count == 0:
        count += 1
        continue
      else:
        name = row[0]
        if name in players:
          scores = players[name]
          scores[dir] = row[score_rows[sys.argv[1].lower()]]
          players[name] = scores
        else:
          scores = {}
          scores[dir] = row[score_rows[sys.argv[1].lower()]]
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

correlation_matrix = scores_table.corr()
correlation_matrix.to_csv(directory+"correlation.csv")