import pulp
import sys
from Nfl import Nfl
from Nhl import Nhl
from Nba import Nba

while True:
	print()
	if sys.argv[1].lower() == 'nfl':
		generator = Nfl(
			sport = "NFL",
			num_lineups = 150,
			overlap = int(sys.argv[4]),
			player_limit = int(sys.argv[5]),
			teams_limit = int(sys.argv[6]),
			stack = sys.argv[7],
			solver = pulp.GLPK_CMD(msg=0),
			correlation_file = 'nfl/inputs/{}/correlation.csv'.format(sys.argv[2]),
			players_file = 'nfl/inputs/{}/{}/players.csv'.format(sys.argv[2], sys.argv[3]),
			defenses_goalies_file = 'nfl/inputs/defense.csv',
			output_file = 'nfl/outputs/{}/output_{}_overlap_{}_playerlimit_{}_numteams_{}_stack_{}.csv'.format(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
		)
	if sys.argv[1].lower() == 'nhl':
		generator = Nhl(
			sport = "NHL",
			num_lineups = 150,
			overlap = int(sys.argv[4]),
			player_limit = int(sys.argv[5]),
			teams_limit = int(sys.argv[6]),
			stack = sys.argv[7],
			solver = pulp.GLPK_CMD(msg=0),
			correlation_file = 'nhl/inputs/{}/correlation.csv'.format(sys.argv[2]),
			players_file = 'nhl/inputs/{}/{}/players.csv'.format(sys.argv[2], sys.argv[3]),
			defenses_goalies_file = 'nhl/inputs/goalies.csv',
			output_file = 'nhl/outputs/{}/output_{}_overlap_{}_playerlimit_{}_numteams_{}_stack_{}.csv'.format(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
		)
	if sys.argv[1].lower() == 'nba':
		generator = Nba(
			sport = "NBA",
			num_lineups = 150,
			overlap = int(sys.argv[4]),
			player_limit = int(sys.argv[5]),
			teams_limit = int(sys.argv[6]),
			stack = sys.argv[7],
			solver = pulp.GLPK_CMD(msg=0),
			correlation_file = 'nba/inputs/{}/correlation.csv'.format(sys.argv[2]),
			players_file = 'nba/inputs/{}/{}/players.csv'.format(sys.argv[2], sys.argv[3]),
			defenses_goalies_file = None,
			output_file = 'nba/outputs/{}/output_{}_overlap_{}_playerlimit_{}_numteams_{}_stack_{}.csv'.format(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
		)
	# create the indicators used to set the constraints to be used by the formula
	generator.create_indicators()
	# generate the lineups with the formula and the indicators
	lineups = generator.generate_lineups(formula=generator.generate)
	# fill the lineups with player names - send in the positions indicator
	filled_lineups = generator.fill_lineups(lineups)
	# save the lineups
	generator.save_file(generator.header, filled_lineups, show_proj=True)
	break