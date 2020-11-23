import csv
import sys

with open('./nba/inputs/players.csv', mode='w') as file:
  writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  writer.writerow(["Player Name", "Pos", "Salary", "Team", "Proj FP", "Actual FP"])
  with open('./nba/inputs/{}/{}/players.csv'.format(sys.argv[1], sys.argv[2]),'rt')as f:
    data = csv.reader(f)
    count = 0
    for row in data:
      name = row[0].lower().replace(" jr.", "").replace(".", "")
      # if row is the header, player is injured, or has a projection lower than 1 skip player
      if row[0] == 'Player' or row[26] != 'Y' or float(row[20]) < 1:
        continue
      else:
        # projection =  projected value
        projection =  row[20]
        writer.writerow([row[0], row[1], row[6], row[2], row[20], row[28]])