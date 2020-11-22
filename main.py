import pulp
import sys
from nfl.fanduel import Fanduel as NFLFanduel

while True:
	print()
	# enter the parameters
	optimizer = Nfl(
              sport="NFL"
              num_lineups=150,
							overlap=4,
							variance=30,
							solver=pulp.GLPK_CMD(msg=0),
							players_filepath = 'nfl/inputs/players.csv',
							defense_filepath = 'nfl/inputs/defense.csv',
							output_filepath = 'nfl/outputs/fanduel_output_{}.csv'.format(sys.argv[1]))
	# create the indicators used to set the constraints to be used by the formula
	optimizer.create_indicators()
	# generate the lineups with the formula and the indicators
	lineups = optimizer.generate_lineups(formula=optimizer.type_1)
	# fill the lineups with player names - send in the positions indicator
	filled_lineups = optimizer.fill_lineups(lineups)
	# save the lineups
	optimizer.save_file(optimizer.header, filled_lineups, show_proj=True)
	break