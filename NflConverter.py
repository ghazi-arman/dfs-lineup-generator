import csv
import sys

with open('./nfl/inputs/players.csv', mode='w') as file:
  writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  writer.writerow(["Player Name", "Pos", "Salary", "Team", "Projected Ownership", "Actual Ownership", "Proj FP", "Actual FP"])
  with open('./nfl/inputs/{}/players.csv'.format(sys.argv[1]),'rt')as f:
    data = csv.reader(f)
    count = 0
    for row in data:
      name = row[0].lower().replace(" jr.", "").replace(".", "")
      # if row is the header, player is injured, or has a projection lower than 1 skip player
      if row[2] == 'Inj' or row[2] == 'O' or row[2] == 'D' or float(row[33]) < 1:
        continue
      else:
        # projection =  projected value + value
        projection =  float(row[33]) + float(row[34])
        print (name + "=" + str(float(row[35]) - float(row[33])))
        writer.writerow([row[0], row[3], row[4], row[5], projected_ownership[name], actual_ownership[name], projection, row[35]])
      
with open('./nfl/inputs/defense.csv', mode='w') as file:
  writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  with open('./nfl/inputs/{}/defense.csv'.format(sys.argv[1]),'rt')as f:
    data = csv.reader(f)
    for row in data:
      writer.writerow(row)
