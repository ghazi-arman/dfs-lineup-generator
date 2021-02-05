import pulp
from LineupGenerator import LineupGenerator

class Nba(LineupGenerator):
	def __init__(self, sport, num_lineups, overlap, player_limit, teams_limit, stack, solver, correlation_file, players_file, defenses_goalies_file, output_file):
		super().__init__(sport, num_lineups, overlap, player_limit, teams_limit, stack, solver, correlation_file, players_file, defenses_goalies_file, output_file)
		self.salary_cap = 55000
		self.header = ['PG', 'PG', 'SG', 'SG', 'SF', 'SF', 'PF', 'PF', 'C']

	def generate(self, lineups):
		prob = pulp.LpProblem('NBA', pulp.LpMaximize)

		players_lineup = [pulp.LpVariable("player_{}".format(i+1), cat="Binary") for i in range(self.num_players)]
		
		# sets player limits for each lineup
		prob += (pulp.lpSum(players_lineup[i] for i in range(self.num_players)) == 9)

		# sets positional limits for each lineup
		prob += (pulp.lpSum(self.positions['PG'][i]*players_lineup[i] for i in range(self.num_players)) == 2)
		prob += (pulp.lpSum(self.positions['SG'][i]*players_lineup[i] for i in range(self.num_players)) == 2)
		prob += (pulp.lpSum(self.positions['SF'][i]*players_lineup[i] for i in range(self.num_players)) == 2)
		prob += (pulp.lpSum(self.positions['PF'][i]*players_lineup[i] for i in range(self.num_players)) == 2)
		prob += (pulp.lpSum(self.positions['C'][i]*players_lineup[i] for i in range(self.num_players)) == 1)

		# sets max salary
		prob += (pulp.lpSum(self.players.loc[i, 'Salary']*players_lineup[i] for i in range(self.num_players)) <= self.salary_cap)
		
    # used_team variable used to keep track of which teams used for each lineup
		used_team = [pulp.LpVariable("u{}".format(i+1), cat="Binary") for i in range(self.num_teams)]
		for i in range(self.num_teams):
			prob += (used_team[i] <= (pulp.lpSum(self.players_teams[k][i]*players_lineup[k] for k in range(self.num_players))))

			# stacks SGs with another player from the same team
			if self.stack == "PG-SG":
				prob += (pulp.lpSum(self.players_teams[k][i]*self.positions['PG'][k]*players_lineup[k] for k in range(self.num_players))
					<= pulp.lpSum(self.players_teams[k][i]*self.positions['SG'][k]*players_lineup[k] for k in range(self.num_players)))
			elif self.stack == "PG-(SG-SF-PF)":
				prob += (pulp.lpSum(self.players_teams[k][i]*self.positions['PG'][k]*players_lineup[k] for k in range(self.num_players))
					<= (pulp.lpSum(self.players_teams[k][i]*self.positions['SG'][k]*players_lineup[k] for k in range(self.num_players))
					+ pulp.lpSum(self.players_teams[k][i]*self.positions['SF'][k]*players_lineup[k] for k in range(self.num_players))
					+ pulp.lpSum(self.players_teams[k][i]*self.positions['PF'][k]*players_lineup[k] for k in range(self.num_players))))
			elif self.stack == "PG-(SG-SF-PF)-(SG-SF-PF)":
				prob += (2*pulp.lpSum(self.players_teams[k][i]*self.positions['PG'][k]*players_lineup[k] for k in range(self.num_players))
					<= (pulp.lpSum(self.players_teams[k][i]*self.positions['SG'][k]*players_lineup[k] for k in range(self.num_players))
					+ pulp.lpSum(self.players_teams[k][i]*self.positions['SF'][k]*players_lineup[k] for k in range(self.num_players))
					+ pulp.lpSum(self.players_teams[k][i]*self.positions['PF'][k]*players_lineup[k] for k in range(self.num_players))))
			elif self.stack == "PG-SG+PG-SG":
				for j in range(self.num_teams):
					if i != j:
						prob += (pulp.lpSum(self.players_teams[k][i]*self.positions['PG'][k]*players_lineup[k] for k in range(self.num_players))
							<= pulp.lpSum(self.players_teams[k][i]*self.positions['SG'][k]*players_lineup[k] for k in range(self.num_players)))
						prob += (pulp.lpSum(self.players_teams[k][j]*self.positions['PG'][k]*players_lineup[k] for k in range(self.num_players))
							<= pulp.lpSum(self.players_teams[k][j]*self.positions['SG'][k]*players_lineup[k] for k in range(self.num_players)))
			elif self.stack == "PG-(SG-SF-PF)+PG-(SG-SF-PF)":
				for j in range(self.num_teams):
					if i != j:
						prob += (pulp.lpSum(self.players_teams[k][i]*self.positions['PG'][k]*players_lineup[k] for k in range(self.num_players))
							<= (pulp.lpSum(self.players_teams[k][i]*self.positions['SG'][k]*players_lineup[k] for k in range(self.num_players))
							+ pulp.lpSum(self.players_teams[k][i]*self.positions['SF'][k]*players_lineup[k] for k in range(self.num_players))
							+ pulp.lpSum(self.players_teams[k][i]*self.positions['PF'][k]*players_lineup[k] for k in range(self.num_players))))
						prob += (pulp.lpSum(self.players_teams[k][j]*self.positions['PG'][k]*players_lineup[k] for k in range(self.num_players))
							<= (pulp.lpSum(self.players_teams[k][j]*self.positions['SG'][k]*players_lineup[k] for k in range(self.num_players))
							+ pulp.lpSum(self.players_teams[k][j]*self.positions['SF'][k]*players_lineup[k] for k in range(self.num_players))
							+ pulp.lpSum(self.players_teams[k][j]*self.positions['PF'][k]*players_lineup[k] for k in range(self.num_players))))
			elif self.stack == "PG-(SG-SF-PF)-(SG-SF-PF)+PG-(SG-SF-PF)-(SG-SF-PF)":
				for j in range(self.num_teams):
					if i != j:
						prob += (2*pulp.lpSum(self.players_teams[k][i]*self.positions['PG'][k]*players_lineup[k] for k in range(self.num_players))
							<= (pulp.lpSum(self.players_teams[k][i]*self.positions['SG'][k]*players_lineup[k] for k in range(self.num_players))
							+ pulp.lpSum(self.players_teams[k][i]*self.positions['SF'][k]*players_lineup[k] for k in range(self.num_players))
							+ pulp.lpSum(self.players_teams[k][i]*self.positions['PF'][k]*players_lineup[k] for k in range(self.num_players))))
						prob += (2*pulp.lpSum(self.players_teams[k][j]*self.positions['PG'][k]*players_lineup[k] for k in range(self.num_players))
							<= (pulp.lpSum(self.players_teams[k][j]*self.positions['SG'][k]*players_lineup[k] for k in range(self.num_players))
							+ pulp.lpSum(self.players_teams[k][j]*self.positions['SF'][k]*players_lineup[k] for k in range(self.num_players))
							+ pulp.lpSum(self.players_teams[k][j]*self.positions['PF'][k]*players_lineup[k] for k in range(self.num_players))))
			
			prob += (pulp.lpSum(self.players_teams[k][i]*players_lineup[k] for k in range(self.num_players)) <= 4*used_team[i])
		# ensures that the lineup contains less than X unique teams
		prob += (pulp.lpSum(used_team[i] for i in range(self.num_teams)) == 5)
		
		# each new lineup can't have more than the overlap variable number of combinations of players in any previous lineups
		for i in range(len(lineups)):
			prob += (pulp.lpSum(lineups[i][k]*players_lineup[k] for k in range(self.num_players)) <= self.overlap)

		# can't use the same player more times than set by player_limit variable
		for i in range(self.num_players):
			prob += ((pulp.lpSum(lineups[k][i]*players_lineup[i] for k in range(len(lineups)))) <= self.player_limit)

		# create lineups with the highest projected fantasy points
		prob += pulp.lpSum(self.players.loc[i, 'Proj FP']*players_lineup[i] for i in range(self.num_players))

		status = prob.solve(self.solver)

		if status != pulp.LpStatusOptimal:
			print('Only {} feasible lineups produced'.format(len(lineups)), '\n')
			return None

		lineup_copy = []
		for i in range(self.num_players):
			if players_lineup[i].varValue == 1:
				lineup_copy.append(1)
			else:
				lineup_copy.append(0)
		return lineup_copy
		
	def fill_lineups(self, lineups):
		filled_lineups = []
		for lineup in lineups:
			a_lineup = ["", "", "", "", "", "", "", "", ""]
			players_lineup = lineup[:self.num_players]
			total_proj = 0
			if self.actuals:
				total_actual = 0
			for num, player in enumerate(players_lineup):
				if player == 1:
					if self.positions['PG'][num] == 1:
						if a_lineup[0] == "":
							a_lineup[0] = self.players.loc[num, 'Player Name'] + self.players.loc[num, 'Team']
						elif a_lineup[1] == "":
							a_lineup[1] = self.players.loc[num, 'Player Name'] + self.players.loc[num, 'Team']
					elif self.positions['SG'][num] == 1:
						if a_lineup[2] == "":
							a_lineup[2] = self.players.loc[num, 'Player Name'] + self.players.loc[num, 'Team']
						elif a_lineup[3] == "":
							a_lineup[3] = self.players.loc[num, 'Player Name'] + self.players.loc[num, 'Team']
					elif self.positions['SF'][num] == 1:
						if a_lineup[4] == "":
							a_lineup[4] = self.players.loc[num, 'Player Name'] + self.players.loc[num, 'Team']
						elif a_lineup[5] == "":
							a_lineup[5] = self.players.loc[num, 'Player Name'] + self.players.loc[num, 'Team']
					elif self.positions['PF'][num] == 1:
						if a_lineup[6] == "":
							a_lineup[6] = self.players.loc[num, 'Player Name'] + self.players.loc[num, 'Team']
						elif a_lineup[7] == "":
							a_lineup[7] = self.players.loc[num, 'Player Name'] + self.players.loc[num, 'Team']
					else:
						a_lineup[8] = self.players.loc[num, 'Player Name'] + self.players.loc[num, 'Team']
					total_proj += self.players.loc[num, 'Proj FP']
					if self.actuals:
						total_actual += self.players.loc[num, 'Actual FP']
			a_lineup.append(round(total_proj, 2))
			if self.actuals:
				a_lineup.append(round(total_actual, 2))
			filled_lineups.append(a_lineup)
		return filled_lineups
