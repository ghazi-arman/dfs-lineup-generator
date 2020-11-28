import pulp
from LineupGenerator import LineupGenerator

class Nhl(LineupGenerator):
	def __init__(self, sport, num_lineups, overlap, player_limit, solver, correlation_file, players_file, defenses_goalies_file, output_file):
		super().__init__(sport, num_lineups, overlap, player_limit, solver, correlation_file, players_file, defenses_goalies_file, output_file)
		self.salary_cap = 55000
		self.header = ['C', 'C', 'W', 'W', 'W', 'W', 'D', 'D', 'G']

	def generate(self, lineups):
		prob = pulp.LpProblem('NHL', pulp.LpMaximize)

		players_lineup = [pulp.LpVariable("player_{}".format(i+1), cat="Binary") for i in range(self.num_players)]
		goalies_lineup = [pulp.LpVariable("goalie_{}".format(i+1), cat="Binary") for i in range(self.num_goalies)]
		
		# sets player and defense limits for each lineup
		prob += (pulp.lpSum(players_lineup[i] for i in range(self.num_players)) == 8)
		prob += (pulp.lpSum(goalies_lineup[i] for i in range(self.num_goalies)) == 1)

		# sets positional limits for each lineup
		prob += (pulp.lpSum(self.positions['C'][i]*players_lineup[i] for i in range(self.num_players)) == 2)
		prob += (pulp.lpSum(self.positions['W'][i]*players_lineup[i] for i in range(self.num_players)) == 4)
		prob += (pulp.lpSum(self.positions['D'][i]*players_lineup[i] for i in range(self.num_players)) == 2)

		# sets max salary
		prob += ((pulp.lpSum(self.players.loc[i, 'Salary']*players_lineup[i] for i in range(self.num_players)) +
			pulp.lpSum(self.goalies.loc[i, 'Salary']*goalies_lineup[i] for i in range(self.num_goalies))) <= self.salary_cap)

		# used_team variable used to keep track of which teams used for each lineup
		used_team = [pulp.LpVariable("u{}".format(i+1), cat="Binary") for i in range(self.num_teams)]
		used_team_players = [pulp.LpVariable("us{}".format(i+1), cat="Binary") for i in range(self.num_teams)]
		for i in range(self.num_teams):
			prob += (used_team[i] <= (pulp.lpSum(self.players_teams[k][i]*players_lineup[k] for k in range(self.num_players)) +
				pulp.lpSum(self.goalies_teams[k][i]*goalies_lineup[k] for k in range(self.num_goalies))))
			
			# ensures that there are no more than 4 players and goalies from a single team
			prob += ((pulp.lpSum(self.players_teams[k][i]*players_lineup[k] for k in range(self.num_players)) +
				pulp.lpSum(self.goalies_teams[k][i]*goalies_lineup[k] for k in range(self.num_goalies))) <= 4*used_team[i])
			
			prob += (used_team_players[i] <= (pulp.lpSum(self.players_teams[k][i]*players_lineup[k] for k in range(self.num_players))))
			# ensures that there are no more than 4 players from a single team
			prob += (pulp.lpSum(self.players_teams[k][i]*players_lineup[k] for k in range(self.num_players)) <= 4*used_team_players[i])
		
		# only 3 teams can be used when generating a lineup
		prob += (pulp.lpSum(used_team_players[i] for i in range(self.num_teams)) == 3)

		# no goalies against players constraint
		for i in range(self.num_goalies):
			prob += (6*goalies_lineup[i] + pulp.lpSum(self.goalies_opponents[k][i]*players_lineup[k] for k in range(self.num_players)) <= 6)

		# must have at least one complete line in each lineup
		line_stack_3 = [pulp.LpVariable("ls3{}".format(i+1), cat="Binary") for i in range(self.num_lines)]
		for i in range(self.num_lines):
			prob += (3*line_stack_3[i] <= pulp.lpSum(self.team_lines[k][i]*players_lineup[k] for k in range(self.num_players)))
		prob += (pulp.lpSum(line_stack_3[i] for i in range(self.num_lines)) >= 1)
		
		# must have at least 2 lines with at least 2 players
		line_stack_2 = [pulp.LpVariable("ls2{}".format(i+1), cat="Binary") for i in range(self.num_lines)]
		for i in range(self.num_lines):
			prob += (2*line_stack_2[i] <= pulp.lpSum(self.team_lines[k][i]*players_lineup[k] for k in range(self.num_players)))
		prob += (pulp.lpSum(line_stack_2[i] for i in range(self.num_lines)) >= 2)

		# each new lineup can't have more than the overlap variable number of combinations of players in any previous lineups
		for i in range(len(lineups)):
			prob += ((pulp.lpSum(lineups[i][k]*players_lineup[k] for k in range(self.num_players)) +
						pulp.lpSum(lineups[i][self.num_players+k]*goalies_lineup[k] for k in range(self.num_goalies))) <= self.overlap)

		# can't use the same player or defense more times than set by player_limit variable
		for i in range(self.num_players):
			prob += ((pulp.lpSum(lineups[k][i]*players_lineup[i] for k in range(len(lineups)))) <= self.player_limit)
		
		#add the objective
		prob += pulp.lpSum((pulp.lpSum(self.players.loc[i, 'Proj FP']*players_lineup[i] for i in range(self.num_players)) +
							pulp.lpSum(self.goalies.loc[i, 'Proj FP']*goalies_lineup[i] for i in range(self.num_goalies))))

		#solve the problem
		status = prob.solve(self.solver)

		#check if the optimizer found an optimal solution
		if status != pulp.LpStatusOptimal:
			print('Only {} feasible lineups produced'.format(len(lineups)), '\n')
			return None

		# Puts the output of one lineup into a format that will be used later
		lineup_copy = []
		for i in range(self.num_players):
			if players_lineup[i].varValue == 1:
				lineup_copy.append(1)
			else:
				lineup_copy.append(0)
		for i in range(self.num_goalies):
			if goalies_lineup[i].varValue == 1:
				lineup_copy.append(1)
			else:
				lineup_copy.append(0)
		return lineup_copy

	def fill_lineups(self, lineups):
		filled_lineups = []
		for lineup in lineups:
			a_lineup = ["", "", "", "", "", "", "", "", ""]
			players_lineup = lineup[:self.num_players]
			goalies_lineup = lineup[-1*self.num_goalies:]
			total_proj = 0
			if self.actuals:
				total_actual = 0
			for num, player in enumerate(players_lineup):
				if player == 1:
					if self.positions['C'][num] == 1:
						if a_lineup[0] == "":
							a_lineup[0] = self.players.loc[num, 'Player Name']
						elif a_lineup[1] == "":
							a_lineup[1] = self.players.loc[num, 'Player Name']
					elif self.positions['W'][num] == 1:
						if a_lineup[2] == "":
							a_lineup[2] = self.players.loc[num, 'Player Name']
						elif a_lineup[3] == "":
							a_lineup[3] = self.players.loc[num, 'Player Name']
						elif a_lineup[4] == "":
							a_lineup[4] = self.players.loc[num, 'Player Name']
						elif a_lineup[5] == "":
							a_lineup[5] = self.players.loc[num, 'Player Name']
					elif self.positions['D'][num] == 1:
						if a_lineup[6] == "":
							a_lineup[6] = self.players.loc[num, 'Player Name']
						elif a_lineup[7] == "":
							a_lineup[7] = self.players.loc[num, 'Player Name']
					total_proj += self.players.loc[num, 'Proj FP']
					if self.actuals:
						total_actual += self.players.loc[num, 'Actual FP']
			for num, goalie in enumerate(goalies_lineup):
				if goalie == 1:
					if a_lineup[8] == "":
						a_lineup[8] = self.goalies.loc[num, 'Player Name']
					total_proj += self.goalies.loc[num, 'Proj FP']
					if self.actuals:
						total_actual += self.goalies.loc[num, 'Actual FP']
			a_lineup.append(round(total_proj, 2))
			if self.actuals:
				a_lineup.append(round(total_actual, 2))
			filled_lineups.append(a_lineup)
		return filled_lineups
