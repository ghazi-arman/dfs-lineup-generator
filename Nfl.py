import pulp
from LineupGenerator import LineupGenerator

class Nfl(LineupGenerator):
	def __init__(self, sport, num_lineups, overlap, player_limit, solver, players_file, defenses_file, output_file):
		super().__init__(sport, num_lineups, overlap, player_limit, solver, players_file, defenses_file, output_file)
		self.salary_cap = 55000
		self.header = ['QB', 'WR', 'WR', 'WR', 'RB', 'RB', 'TE', 'FLEX', 'DEF']

	def generate(self, lineups):
		prob = pulp.LpProblem('NFL', pulp.LpMaximize)

		players_lineup = [pulp.LpVariable("player_{}".format(i+1), cat="Binary") for i in range(self.num_players)]
		defenses_lineup = [pulp.LpVariable("defenses_{}".format(i+1), cat="Binary") for i in range(self.num_defenses)]
		
		# sets player and defense limits for each lineup
		prob += (pulp.lpSum(players_lineup[i] for i in range(self.num_players)) == 8)
		prob += (pulp.lpSum(defenses_lineup[i] for i in range(self.num_defenses)) == 1)

		# sets positional limits for each lineup
		prob += (pulp.lpSum(self.positions['QB'][i]*players_lineup[i] for i in range(self.num_players)) == 1)
		prob += (pulp.lpSum(self.positions['RB'][i]*players_lineup[i] for i in range(self.num_players)) >= 2)
		prob += (pulp.lpSum(self.positions['WR'][i]*players_lineup[i] for i in range(self.num_players)) >= 3)
		prob += (pulp.lpSum(self.positions['TE'][i]*players_lineup[i] for i in range(self.num_players)) >= 1)
		prob += (pulp.lpSum(self.positions['RB'][i]*players_lineup[i] for i in range(self.num_players))
			+ pulp.lpSum(self.positions['WR'][i]*players_lineup[i] for i in range(self.num_players))
			+ pulp.lpSum(self.positions['TE'][i]*players_lineup[i] for i in range(self.num_players)) == 7)

		# sets max salary
		prob += ((pulp.lpSum(self.players.loc[i, 'Salary']*players_lineup[i] for i in range(self.num_players)) +
			pulp.lpSum(self.defenses.loc[i, 'Salary']*defenses_lineup[i] for i in range(self.num_defenses))) <= self.salary_cap)
		
    # used_team variable used to keep track of which teams used for each lineup
		used_team = [pulp.LpVariable("u{}".format(i+1), cat="Binary") for i in range(self.num_teams)]
		for i in range(self.num_teams):
			prob += (used_team[i] <= (pulp.lpSum(self.players_teams[k][i]*players_lineup[k] for k in range(self.num_players))))
      # ensures each lineup has a qb and wr from the same team
			prob += (2*pulp.lpSum(self.players_teams[k][i]*self.positions['QB'][k]*players_lineup[k] for k in range(self.num_players))
				<= pulp.lpSum(self.players_teams[k][i]*self.positions['WR'][k]*players_lineup[k] for k in range(self.num_players)))
			prob += (pulp.lpSum(self.players_teams[k][i]*players_lineup[k] for k in range(self.num_players)) <= 4*used_team[i])
		# ensures that the lineup contains at least 6 unique teams
		prob += (pulp.lpSum(used_team[i] for i in range(self.num_teams)) >= 6)

		# each new lineup can't have more than the overlap variable number of combinations of players in any previous lineups
		for i in range(len(lineups)):
			prob += ((pulp.lpSum(lineups[i][k]*players_lineup[k] for k in range(self.num_players)) +
						pulp.lpSum(lineups[i][self.num_players+k]*defenses_lineup[k] for k in range(self.num_defenses))) <= self.overlap)

		# can't use the same player or defense more times than set by player_limit variable
		for i in range(self.num_players):
			prob += ((pulp.lpSum(lineups[k][i]*players_lineup[i] for k in range(len(lineups)))) <= self.player_limit)
		for i in range(self.num_defenses):
			prob += ((pulp.lpSum(lineups[k][self.num_players+i]*defenses_lineup[i] for k in range(len(lineups)))) <= self.player_limit)

		# create lineups with the highest projected fantasy points
		prob += pulp.lpSum((pulp.lpSum(self.players.loc[i, 'Proj FP']*players_lineup[i] for i in range(self.num_players)) +
			pulp.lpSum(self.defenses.loc[i, 'Proj FP']*defenses_lineup[i] for i in range(self.num_defenses))))

		status = prob.solve(self.solver)

		if status != pulp.LpStatusOptimal:
			print('Only {} feasible lineups produced'.format(len(lineups)), '\n')
			return None

		lineup_copy = []
		for i in range(self.num_players):
			if players_lineup[i].varValue >= 0.9 and players_lineup[i].varValue <= 1.1:
				lineup_copy.append(1)
			else:
				lineup_copy.append(0)
		for i in range(self.num_defenses):
			if defenses_lineup[i].varValue >= 0.9 and defenses_lineup[i].varValue <= 1.1:
				lineup_copy.append(1)
			else:
				lineup_copy.append(0)
		return lineup_copy

	def fill_lineups(self, lineups):
		filled_lineups = []
		for lineup in lineups:
			a_lineup = ["", "", "", "", "", "", "", "", ""]
			players_lineup = lineup[:self.num_players]
			defenses_lineup = lineup[-1*self.num_defenses:]
			total_proj = 0
			if self.actuals:
				total_actual = 0
			for num, player in enumerate(players_lineup):
				if player > 0.9 and player < 1.1:
					if self.positions['QB'][num] == 1:
						if a_lineup[0] == "":
							a_lineup[0] = self.players.loc[num, 'Player Name'] + self.players.loc[num, 'Team']
					elif self.positions['WR'][num] == 1:
						if a_lineup[1] == "":
							a_lineup[1] = self.players.loc[num, 'Player Name'] + self.players.loc[num, 'Team']
						elif a_lineup[2] == "":
							a_lineup[2] = self.players.loc[num, 'Player Name'] + self.players.loc[num, 'Team']
						elif a_lineup[3] == "":
							a_lineup[3] = self.players.loc[num, 'Player Name'] + self.players.loc[num, 'Team']
						elif a_lineup[7] == "":
							a_lineup[7] = self.players.loc[num, 'Player Name'] + self.players.loc[num, 'Team']
					elif self.positions['RB'][num] == 1:
						if a_lineup[4] == "":
							a_lineup[4] = self.players.loc[num, 'Player Name'] + self.players.loc[num, 'Team']
						elif a_lineup[5] == "":
							a_lineup[5] = self.players.loc[num, 'Player Name'] + self.players.loc[num, 'Team']
						elif a_lineup[5] == "":
							a_lineup[5] = self.players.loc[num, 'Player Name'] + self.players.loc[num, 'Team']
						elif a_lineup[7] == "":
							a_lineup[7] = self.players.loc[num, 'Player Name'] + self.players.loc[num, 'Team']
					elif self.positions['TE'][num] == 1:
						if a_lineup[6] == "":
							a_lineup[6] = self.players.loc[num, 'Player Name'] + self.players.loc[num, 'Team']
						elif a_lineup[7] == "":
							a_lineup[7] = self.players.loc[num, 'Player Name'] + self.players.loc[num, 'Team']
					total_proj += self.players.loc[num, 'Proj FP']
					if self.actuals:
						total_actual += self.players.loc[num, 'Actual FP']
			for num, defense in enumerate(defenses_lineup):
				if defense > 0.9 and defense < 1.1:
					if a_lineup[8] == "":
						a_lineup[8] = self.defenses.loc[num, 'Player Name']
					total_proj += self.defenses.loc[num, 'Proj FP']
					if self.actuals:
						total_actual += self.defenses.loc[num, 'Actual FP']
			a_lineup.append(round(total_proj, 2))
			if self.actuals:
				a_lineup.append(round(total_actual, 2))
			filled_lineups.append(a_lineup)
		return filled_lineups
