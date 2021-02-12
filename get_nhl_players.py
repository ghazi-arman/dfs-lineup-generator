import os
import sys
import csv

with open('nhl/inputs/{}/{}/players.csv'.format(sys.argv[1], sys.argv[2]),'rt') as f:
  data = csv.reader(f)
  players = []
  for row in data:
    if row[0] == 'C':
      continue
    if row[3] == sys.argv[3] and row[5] == sys.argv[4]:
      players.append(row[0])
print(players)
    