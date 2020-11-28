import csv
import sys
import datetime 

with open('./nba/inputs/players.csv', mode='w') as file:
  writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  writer.writerow(["Player Name", "Pos", "Salary", "Team", "Games", "Points", "Assists", "Rebounds", "Steals", "Blocks", "Turnovers", "Proj FP", "Actual FP"])
  with open('./nba/inputs/{}/{}/players_cruncher.csv'.format(sys.argv[1], sys.argv[2]),'rt') as f:
    data = csv.reader(f)
    own_projection_count = 0
    fc_projection_count = 0
    for row in data:
      # if row is the header, player is injured, or has a projection lower than 1 skip player
      if row[0] == 'Player' or row[26] != 'Y':
        continue
      else:
        with open('./nba/inputs/{}/players/{}.csv'.format(sys.argv[1], row[0].replace(" ", "").replace(".", "").lower()),'rt') as fi:
          data = csv.reader(fi)
          games = 0
          points = 0
          assists = 0
          rebounds = 0
          steals = 0
          blocks = 0
          turnovers = 0
          for stat_row in data:
            if stat_row[0] == 'date':
              continue
            elif stat_row[0] < sys.argv[2]:
              games += 1
              points += float(stat_row[1])
              assists += float(stat_row[16])
              rebounds += float(stat_row[14]) + float(stat_row[15])
              steals += float(stat_row[17])
              blocks += float(stat_row[18])
              turnovers += float(stat_row[19])
        
        projection =  float(row[20])
        # use fantasy cruncher projection if no games recorded  
        if games != 0:
          own_projection = (points + rebounds * 1.2 + assists * 1.5 + blocks * 3 + steals * 3 + turnovers * -1) / games
        else:
          own_projection = projection
        
        # counter to indicate which projection is closer to actual result
        if abs(projection - float(row[28])) <= abs(own_projection - float(row[28])):
          fc_projection_count += 1
        else:
          own_projection_count += 1
        
        writer.writerow([row[0], row[1], row[6], row[2], games, points, assists, rebounds, steals, blocks, turnovers, own_projection, row[28]])

print("FC:{}".format(fc_projection_count))
print("Own:{}".format(own_projection_count))
