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

with open('./nhl/outputs/{}/fanduel/fd_{}'.format(sys.argv[1], sys.argv[3]), 'w+') as file:
  writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  writer.writerow(['C', 'C', 'W', 'W', 'D', 'D', 'UTIL', 'UTIL', 'G'])
  with open('./nhl/outputs/{}/{}'.format(sys.argv[1], sys.argv[3]),'rt')as f:
    data = csv.reader(f)
    for row in data:
      if(row[0] == 'C'):
        continue
      
      writer.writerow([players[row[0][:row[0].index(',')]], players[row[1][:row[1].index(',')]], players[row[2][:row[2].index(',')]], players[row[3][:row[3].index(',')]], players[row[4][:row[4].index(',')]], players[row[5][:row[5].index(',')]], players[row[6][:row[6].index(',')]], players[row[7][:row[7].index(',')]], players[row[8][:row[8].index(',')]]])
      count += 1