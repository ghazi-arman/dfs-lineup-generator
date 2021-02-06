import os
import sys
import csv

directory = '{}/outputs/{}'.format(sys.argv[1], sys.argv[2])
top_scores=[]
for filename in os.listdir(directory):
  # if we want to limit output files by certain parameters (date, player_limit, overlap, etc.)
  if (len(sys.argv) >= 5):
    contains_queries = True
    queries = sys.argv[4].split(",")
    for query in queries:
      if query not in filename:
        contains_queries = False
  if (len(sys.argv) <= 4 or contains_queries): 
    # iterate through each output file and take top X scores
    with open('{}/outputs/{}/{}'.format(sys.argv[1], sys.argv[2], filename),'rt') as f:
      data = csv.reader(f)
      scores=[]
      for row in data:
        if row[0] == 'PG' or row[0] == 'C' or row[0] == 'QB':
          continue
        scores.append((float(row[10]), filename))
    scores.sort(reverse = True)
    top_scores += scores[:int(sys.argv[3])]

top_scores.sort(reverse = True)
print(top_scores)
    
