import csv
import sys
import datetime
import re
import os.path

with open('./nba/inputs/{}/{}/players.csv'.format(sys.argv[1], sys.argv[2]), 'w+') as file:
  writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  writer.writerow(["Player Name", "Pos", "Salary", "Team", "Proj FP", "Actual FP"])

  if os.path.exists('./nba/inputs/{}/{}/players_cruncher.csv'.format(sys.argv[1], sys.argv[2])):
    with open('./nba/inputs/{}/{}/players_cruncher.csv'.format(sys.argv[1], sys.argv[2]), 'rt') as f:
      data = csv.reader(f)
      for row in data:
        # if row is the header, player is injured, or has a projection lower than 1 skip player
        if row[0] == 'Player' or row[26] != 'Y':
          continue
        # else:
        #   with open('./nba/inputs/{}/players/{}.csv'.format(sys.argv[1], row[0].replace(" ", "").replace(".", "").lower()),'rt') as fi:
        #     data = csv.reader(fi)
        #     games = 0
        #     points = 0
        #     assists = 0
        #     rebounds = 0
        #     steals = 0
        #     blocks = 0
        #     turnovers = 0
        #     for stat_row in data:
        #       if stat_row[0] == 'date':
        #         continue
        #       elif stat_row[0] < sys.argv[2]:
        #         games += 1
        #         points += float(stat_row[1])
        #         assists += float(stat_row[16])
        #         rebounds += float(stat_row[14]) + float(stat_row[15])
        #         steals += float(stat_row[17])
        #         blocks += float(stat_row[18])
        #         turnovers += float(stat_row[19])
        writer.writerow([row[0], row[1], row[6], row[2], row[20], row[28]])

  if os.path.exists('./nba/inputs/{}/{}/players_dfn.csv'.format(sys.argv[1], sys.argv[2])):
    with open('./nba/inputs/{}/{}/players_dfn.csv'.format(sys.argv[1], sys.argv[2]), 'rt') as f:
      data = csv.reader(f)
      for row in data:
        if row[0] == 'Player Name' or row[2] == 'O':
          continue
        # if row is the header, player is injured, or has a projection lower than 1 skip player
        # if row[0] == 'Player' or row[26] != 'Y':
        #   continue
        # else:
        #   with open('./nba/inputs/{}/players/{}.csv'.format(sys.argv[1], row[0].replace(" ", "").replace(".", "").lower()),'rt') as fi:
        #     data = csv.reader(fi)
        #     games = 0
        #     points = 0
        #     assists = 0
        #     rebounds = 0
        #     steals = 0
        #     blocks = 0
        #     turnovers = 0
        #     for stat_row in data:
        #       if stat_row[0] == 'date':
        #         continue
        #       elif stat_row[0] < sys.argv[2]:
        #         games += 1
        #         points += float(stat_row[1])
        #         assists += float(stat_row[16])
        #         rebounds += float(stat_row[14]) + float(stat_row[15])
        #         steals += float(stat_row[17])
        #         blocks += float(stat_row[18])
        #         turnovers += float(stat_row[19])
        writer.writerow([row[0], row[3], row[4], row[5], row[25], row[28]])