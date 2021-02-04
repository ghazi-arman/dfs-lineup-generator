import os
import sys
import csv

directory = '{}/outputs/{}'.format(sys.argv[1], sys.argv[2])
top_scores=[]
for filename in os.listdir(directory):
  if (len(sys.argv) <= 4 or sys.argv[4] in filename): 
    with open('{}/outputs/{}/{}'.format(sys.argv[1], sys.argv[2], filename),'rt') as f:
      data = csv.reader(f)
      scores=[]
      for row in data:
        if row[0] == 'PG':
          continue
        scores.append((float(row[10]), filename))
    scores.sort(reverse = True)
    top_scores += scores[:int(sys.argv[3])]

top_scores.sort(reverse = True)
print(top_scores)
    
