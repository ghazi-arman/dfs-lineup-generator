import pulp
import sys
from Nfl import Nfl

while True:
	print()
	# enter the parameters
	generator = Nfl(
		sport="NFL",
		num_lineups=5,
		overlap=4,
		player_limit=10,
		solver=pulp.GLPK_CMD(msg=0),
		players_file = 'nfl/inputs/players.csv',
		defenses_file = 'nfl/inputs/defense.csv',
		output_file = 'nfl/outputs/{}/fanduel_output_{}.csv'.format(sys.argv[1], sys.argv[2])
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