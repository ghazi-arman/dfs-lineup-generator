import os
import sys
import csv

overlaps = [4, 5, 6, 7]
player_limits = [25, 50, 150]
team_limits = [2, 3]
stacks = ["3-2", "3-3", "2-2-2"]
dates = []
scores_map={}
with open('{}/inputs/{}/topscores.csv'.format(sys.argv[1], sys.argv[2]),'rt') as f:
    data = csv.reader(f)
    scores=[]
    for row in data:
      if row[0] == 'Date':
        continue
      dates.append(row[0])
      scores_map[row[0]] = [float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), int(row[8])]

winnings = []
for overlap in overlaps:
  for player_limit in player_limits:
    for team_limit in team_limits:
      for stack in stacks:
        balance = 0
        min_balance = 0
        for date in dates:
          filename = '{}/outputs/{}/output_{}_overlap_{}_playerlimit_{}_numteams_{}_stack_{}_proj.csv'.format(sys.argv[1], sys.argv[2], date, overlap, player_limit, team_limit, stack)
          if os.path.isfile(filename) and (len(sys.argv) < 4 or scores_map[date][7] in range(int(sys.argv[3]), int(sys.argv[4]) + 1)):
            balance -= 666
            top_scores = scores_map[date]
            with open(filename,'rt') as f:
              has_10000 = False
              has_3000 = False
              has_1500 = False
              has_750 = False
              has_500 = False
              has_300 = False
              data = csv.reader(f)
              scores=[]
              for row in data:
                if row[0] == 'PG' or row[0] == 'C' or row[0] == 'QB':
                  continue
                if(float(row[10]) > top_scores[0] and has_10000 == False):
                  balance += 10000
                  for i in range(1,6):
                    top_scores[i] = top_scores[i - 1]
                  has_10000 = True
                elif(float(row[10]) > top_scores[1] and has_3000 == False):
                  balance += 3000
                  for i in range(2,6):
                    top_scores[i] = top_scores[i - 1]
                  has_3000 = True
                elif(float(row[10]) > top_scores[2] and has_1500 == False):
                  balance += 1500
                  for i in range(3,6):
                    top_scores[i] = top_scores[i - 1]
                  has_1500 = True
                elif(float(row[10]) > top_scores[3] and has_750 == False):
                  balance += 750
                  for i in range(4,6):
                    top_scores[i] = top_scores[i - 1]
                  has_750 = True
                elif(float(row[10]) > top_scores[4] and has_500 == False):
                  balance += 500
                  top_scores[5] = top_scores[4]
                  has_500 = True
                elif(float(row[10]) > top_scores[5] and has_300 == False):
                  balance += 300
                  has_300 = True
                elif(float(row[10]) > top_scores[6]):
                  balance += 8
              min_balance = min(balance, min_balance)
        winnings.append((balance, min_balance, '{}, {}, {}, {}'.format(overlap, player_limit, team_limit, stack)))

winnings.sort(reverse = True)
print(winnings)

    
