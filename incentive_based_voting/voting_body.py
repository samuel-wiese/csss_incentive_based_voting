from __future__ import annotations

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import csv
import os

from voting_bodies import VotingBodies
from parties import Parties
from house_representative import HouseRepresentative
from senate_representative import SenateRepresentative
from vote import Vote

from typing import List, Union, TYPE_CHECKING
if TYPE_CHECKING:
	from coalition import Coalition
	from party import Party
	from bill import Bill


class VotingBody:
	"""
	A voting body in the US congress.
	"""

	def __init__(self, year: int, t_max: int, voting_body: VotingBodies):
		"""
		Initialises the voting body.

		Parameters
		----------
		year : int
			The current year.
		t_max : int
			The number of years we are running the simulation for.
		voting_body : VotingBodies
			Which voting body we are initiating.
		"""

		# Base parameters
		self.year: int = year
		self.t_max: int = t_max
		self.voting_body: VotingBodies = voting_body

		# Votes by year
		self.votes_by_year: List[List[Vote]] = []

		# Representatives and coalitions
		self.representatives: List[Union[HouseRepresentative, SenateRepresentative]] = []
		if self.voting_body == VotingBodies.HOUSE:
			desc = "house"
		else:
			desc = "senate"
		self.coalitions: List[Coalition] = []
		self.broken_coalitions: List[Coalition] = []

		# Need to take votes into account
		current_district, current_votes, current_votes1, current_votes2 = None, None, None, None
		n_reps_by_state = {"AZ": 1}
		if self.voting_body == VotingBodies.HOUSE:
			current_votes = 0
			current_state = "AZ"
			current_district = "001"
		else:
			current_votes1, current_votes2 = 0, 0
			current_state = "AL"

		# Senate is painful to do, and I don't have time
		if self.voting_body == VotingBodies.HOUSE:

			# Take data and create new representatives
			senate_data = []
			f = open(os.path.dirname(__file__) + "/data/" + desc + ".csv", "r", encoding='Latin1')
			for line in csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
				senate_data.append(line)
			senate_data = np.array(senate_data)
			year_ind = np.where(senate_data[:, 0] == str(year))
			start_line, end_line = np.min(year_ind), np.max(year_ind)
			for rep_id, line in enumerate(senate_data[start_line:end_line + 1]):

				# Take data
				if self.voting_body == VotingBodies.HOUSE:
					state = line[2]
					district = line[7]
					name = line[11]
					party_data = line[12]
					votes = int(line[15])
				else:
					state = line[2]
					district = None
					name = line[10]
					party_data = line[11]
					votes = int(line[14])

				# Choose the party
				if party_data == "DEMOCRAT":
					party = Parties.DEMOCRATIC
				elif party_data == "REPUBLICAN":
					party = Parties.REPUBLICAN
				else:
					party = Parties.OTHER

				# Check votes
				if self.voting_body == VotingBodies.HOUSE:
					if district == current_district:
						if votes < current_votes:
							continue
						else:
							self.representatives = self.representatives[:-1]
							current_votes = votes
				else:
					if state == current_state:

						if state == "SD":
							pass

						if votes > current_votes1:
							if n_reps_by_state[state] > 2:
								self.representatives = self.representatives[:-2] + [self.representatives[-1]]
							current_votes1 = votes
						elif votes > current_votes2:
							if n_reps_by_state[state] > 2:
								self.representatives = self.representatives[:-1]
							current_votes2 = votes
						else:
							continue
					else:
						current_votes1 = votes
						current_votes2 = 0
						if state not in n_reps_by_state:
							n_reps_by_state[state] = 1
						else:
							pass

				# Create the representative
				if self.voting_body == VotingBodies.HOUSE:
					current_district = district
					representative = HouseRepresentative("HR_0_" + str(rep_id + 1), state, district, name, party, 0,
														 self.t_max)
				else:
					current_state = state
					n_reps_by_state += 1
					representative = SenateRepresentative("SR_0_" + str(rep_id + 1), state, name, party, 0, self.t_max)
				self.representatives.append(representative)

		# Whatever
		else:
			for i in range(57):
				representative = SenateRepresentative("SR_0_" + str(i + 1), "XX", "person", Parties.DEMOCRATIC,
													  0, self.t_max)
				self.representatives.append(representative)
			for i in range(41):
				representative = SenateRepresentative("SR_0_" + str(i + 58), "XX", "person", Parties.REPUBLICAN,
													  0, self.t_max)
				self.representatives.append(representative)
			for i in range(2):
				representative = SenateRepresentative("SR_0_" + str(i + 99), "XX", "person", Parties.OTHER,
													  0, self.t_max)
				self.representatives.append(representative)

	def vote(self, bill: Bill, democrats: Party, republicans: Party, otherparty: Party, t: int) -> Vote:
		"""
		The voting body makes a decision on a bill.

		Parameters
		----------
		bill : Bill
			The bill in question.
		democrats : Party
			The democratic party.
		republicans : Party
			The republican party.
		otherparty : Party
			The other party.
		t : int
			The current time step.

		Returns
		-------
		vote : Vote
			The resulting vote.
		"""

		yeas: List[str] = []
		nays: List[str] = []

		# Have all coalitions vote
		for coalition in self.coalitions:
			rep_ids = [r.id for r in coalition.representatives]
			if coalition.vote(bill, democrats, republicans, otherparty):
				yeas.extend(rep_ids)
			else:
				nays.extend(rep_ids)

		# Have all other representatives vote
		for representative in self.representatives:
			if representative.coalition is None:
				if representative.vote(bill, democrats, republicans, otherparty):
					yeas.append(representative.id)
				else:
					nays.append(representative.id)

		# Return the results
		return Vote(self.voting_body, yeas, nays, t)

	def plot_network(self) -> None:
		"""
		Plots the evolution of the network of representatives and their political preferences.
		"""

		# Plot the policy preferences and final coalitions
		graph = nx.Graph()
		for r1 in self.representatives:
			graph.add_node(r1.id, pos=(r1.policy_preference.libertarian, r1.policy_preference.progressive),
						   party=r1.party)

			if r1.coalition is not None:
				for r2 in r1.coalition.representatives:
					if not graph.has_edge(r2.id, r1.id) and r1 != r2:
						graph.add_edge(r1.id, r2.id)

		# Draw it
		pos = nx.get_node_attributes(graph, 'pos')
		rep_parties = nx.get_node_attributes(graph, "party")
		dem_nodes = [node for node in rep_parties if rep_parties[node] == Parties.DEMOCRATIC]
		rep_nodes = [node for node in rep_parties if rep_parties[node] == Parties.REPUBLICAN]
		rep_other = [node for node in rep_parties if rep_parties[node] == Parties.OTHER]
		f, ax = plt.subplots()
		nx.draw_networkx_nodes(graph, pos, dem_nodes, ax=ax, node_size=5, node_color="blue", label="Democrat")
		nx.draw_networkx_nodes(graph, pos, rep_nodes, ax=ax, node_size=5, node_color="red", label="Republican")
		nx.draw_networkx_nodes(graph, pos, rep_other, ax=ax, node_size=5, node_color="green", label="Other")

		# Add edges
		nx.draw_networkx_edges(graph, pos, edge_color="grey")

		# Make it look nice
		ax.set_xlabel("Libertarian", labelpad=5)
		ax.set_ylabel("Progressive", labelpad=5)
		ax.set_aspect(1.0)
		ax.set_xlim(0, 1)
		ax.set_ylim(0, 1)
		ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
		plt.axis('on')
		plt.axhline(y=0.5, c="k", linewidth=0.5)
		plt.axvline(x=0.5, c="k", linewidth=0.5)
		vb = "House" if self.voting_body == VotingBodies.HOUSE else "Senate"
		plt.title("The " + vb + " in 2010")
		plt.legend(loc=3)

		# Save it
		vb = "house" if self.voting_body == VotingBodies.HOUSE else "senate"
		f.savefig("networks/network_" + vb + ".pdf", dpi=300, tight_layout=True, bbox_inches='tight')
