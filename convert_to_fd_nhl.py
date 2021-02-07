import csv
import sys

with open('./nhl/inputs/{}/{}/fanduel.csv'.format(sys.argv[1], sys.argv[2]),'rt')as f:
  data = csv.reader(f)
  count = 0
  players = {}
  for row in data:
    if(count < 7):
      count += 1
      continue

    players[row[14]] = row[10]    
    count += 1

with open('./nhl/outputs/{}/fd_{}.csv'.format(sys.argv[1], sys.argv[3]), 'w+') as file:
  writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  writer.writerow(['C', 'C', 'W', 'W', 'D', 'D', 'UTIL', 'UTIL', 'G'])
  with open('./nhl/outputs/{}/{}'.format(sys.argv[1], sys.argv[3]),'rt')as f:
    data = csv.reader(f)
    for row in data:
      if(row[0] == 'C'):
        continue
      
      writer.writerow([players[row[0][:-3]], players[row[1][:-3]], players[row[2][:-3]], players[row[3][:-3]], players[row[4][:-3]], players[row[5][:-3]], players[row[6][:-3]], players[row[7][:-3]], players[row[8][:-3]]])
      count += 1