import sys
import csv
import pulp
import copy
import pandas as pd
from tqdm import tqdm

class LineupGenerator:
	def __init__(self, sport, num_lineups, overlap, player_limit, solver, players_file, defenses_file, output_file):
		self.num_lineups = num_lineups
		self.overlap = overlap
		self.player_limit = player_limit
		self.solver = solver
		self.players = self.load(players_file)
		self.num_players = len(self.players.index)
    self.players_teams = []
    if sport is 'NFL':
		  self.positions = {'QB':[], 'WR':[], 'RB':[], 'TE':[]}
      self.defenses = self.load(defenses_file)
      self.num_defenses = len(self.defenses.index)
      self.defenses_teams = []
    elif sport is 'NHL':
      self.positions = {'C':[], 'W':[], 'D':[]}
      self.goalies = self.load(goalies_file)
      self.num_goalies = len(self.goalies.index)
      self.goalies_teams = []
		  self.goalies_opponents = []
		self.output_file = output_file
		self.num_teams = None
		self.actuals = True if 'Actual FP' in self.players_df else False

	def load(self, filepath):
		try:
			data = pd.read_csv(filepath)
		except IOError:
			sys.exit('INVALID FILEPATH: {}'.format(filepath))
		return data

	def save_file(self, header, filled_lineups, show_proj=False):
		header_copy = copy.deepcopy(header)
		output_projection_path = self.output_filepath.split('.')[0] + '_proj.csv'
		if self.actuals:
			lineups_for_upload = [lineup[:-2] for lineup in filled_lineups]
			header_copy.extend(('PROJ', 'ACTUAL'))
		else:
			lineups_for_upload = [lineup[:-1] for lineup in filled_lineups]
			header_copy.extend(('PROJ'))
		if show_proj == False:
			with open(self.output_filepath, 'w') as f:
					writer = csv.writer(f)
					writer.writerow(header)
					writer.writerows(lineups_for_upload)
		elif show_proj == True:
			with open(output_projection_path, 'w') as f:
					writer = csv.writer(f)
					writer.writerow(header_copy)
					writer.writerows(filled_lineups)

	def create_indicators(self):
		teams = list(set(self.players_df['Team'].values))
		self.num_teams = len(teams)

		# positions used to show what position each player is
		for pos in self.players_df.loc[:, 'Pos']:
			for key in self.positions:
				self.positions[key].append(1 if key in pos else 0)

		# players_teams which teams each player is on
		for player_team in self.players_df.loc[:, 'Team']:
			self.players_teams.append([1 if player_team == team else 0 for team in teams])

    # goalies_opponents indicates which players are not on same team as goalie
    if sport is 'NHL':
      for player_opp in self.skaters_df.loc[:, 'opp']:
			  self.goalies_opponents.append([1 if player_opp == team else 0 for team in self.goalies_df.loc[:, 'team']])

	def generate_lineups(self, formula):
		lineups = []
		for _ in tqdm(range(self.num_lineups)):
			lineup = formula(lineups)
			if lineup:
				lineups.append(lineup)
			else:
				break
		return lineups
