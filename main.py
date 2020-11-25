import pulp
import sys
from Nfl import Nfl
from Nhl import Nhl
from Nba import Nba

while True:
	print()
	if sys.argv[1] == 'NFL':
		generator = Nfl(
			sport = "NFL",
			num_lineups = 150,
			overlap = 4,
			player_limit = 10,
			solver = pulp.GLPK_CMD(msg=0),
			players_file = 'nfl/inputs/players.csv',
			defenses_goalies_file = 'nfl/inputs/defense.csv',
			output_file = 'nfl/outputs/{}/output_{}.csv'.format(sys.argv[2], sys.argv[3])
		)
	if sys.argv[1] == 'NHL':
		generator = Nhl(
			sport = "NHL",
			num_lineups = 150,
			overlap = 5,
			player_limit = 10,
			solver = pulp.GLPK_CMD(msg=0),
			players_file = 'nhl/inputs/players.csv',
			defenses_goalies_file = 'nhl/inputs/goalies.csv',
			output_file = 'nhl/outputs/{}/output_{}.csv'.format(sys.argv[2], sys.argv[3])
		)
	if sys.argv[1] == 'NBA':
		generator = Nba(
			sport = "NBA",
			num_lineups = 150,
			overlap = 5,
			player_limit = 150,
			solver = pulp.GLPK_CMD(msg=0),
			players_file = 'nba/inputs/players.csv',
			defenses_goalies_file = None,
			output_file = 'nba/outputs/{}/output_{}.csv'.format(sys.argv[2], sys.argv[3])
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