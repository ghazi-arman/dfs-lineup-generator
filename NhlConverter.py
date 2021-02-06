import csv
import sys
import datetime
import re
import os.path

with open('./nhl/inputs/{}/{}/players.csv'.format(sys.argv[1], sys.argv[2]), 'w+') as file:
  writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  writer.writerow(["Player Name", "Pos", "Salary", "Team", "Opp", "Line", "Proj FP", "Actual FP"])
  if os.path.exists('./nhl/inputs/{}/{}/players_dfn.csv'.format(sys.argv[1], sys.argv[2])):
    with open('./nhl/inputs/{}/{}/players_dfn.csv'.format(sys.argv[1], sys.argv[2]),'rt')as f:
      data = csv.reader(f)
      count = 4
      for row in data:
        if(count == 4):
          count += 1
          continue

        if row[8] == 'L1':
          line = 1
        elif row[8] == 'L2':
          line = 2
        elif row[8] == 'L3':
          line = 3
        elif row[8] in ('D1', 'D2') and row[9] in ('P1', 'P2'):
          line = count
        else:
          count += 1
          continue

        opponent = row[6].replace('@', '')
        
        writer.writerow([row[0], row[3], row[4], row[5], opponent, line, row[22], row[24]])
        count += 1

with open('./nhl/inputs/{}/{}/goalies.csv'.format(sys.argv[1], sys.argv[2]), 'w+') as file:
  writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  writer.writerow(["Player Name", "Salary", "Team", "Opp", "Proj FP", "Actual FP"])
  if os.path.exists('./nhl/inputs/{}/{}/players_dfn.csv'.format(sys.argv[1], sys.argv[2])):
    with open('./nhl/inputs/{}/{}/goalies_dfn.csv'.format(sys.argv[1], sys.argv[2]),'rt')as f:
      data = csv.reader(f)
      count = 0
      for row in data:
        if(count == 0):
          count += 1
          continue
        
        if(row[20] == 'NaN'):
          row[20] = 0
        opponent = row[6].replace('@', '')
        writer.writerow([row[0], row[4], row[5], opponent, row[20], row[22]])
        count += 1
