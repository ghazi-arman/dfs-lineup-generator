from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
import csv
import sys

bbref_name_map = {}
with open('./nba/inputs/{}/bbref.csv'.format(sys.argv[1]),'rt') as f:
  data = csv.reader(f)
  for row in data:
    if row[0] == 'Player Name':
      continue
    else:
      bbref_name_map[row[0]] = row[1]

for name in bbref_name_map.keys():
  print(name.replace(" ", "").replace(".", "").lower())
  client.regular_season_player_box_scores(
      player_identifier=bbref_name_map[name], 
      season_end_year=sys.argv[2],
      output_type=OutputType.CSV,
      output_file_path="./nba/inputs/{}/players/{}.csv".format(sys.argv[1], name.replace(" ", "").replace(".", "").lower())
  )