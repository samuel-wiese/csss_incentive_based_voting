from __future__ import annotations

import numpy as np
import csv
import os

from voting_bodies import VotingBodies
from parties import Parties
from house_representative import HouseRepresentative
from senate_representative import SenateRepresentative
from vote import Vote

from typing import List, TYPE_CHECKING
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
		if self.voting_body == VotingBodies.HOUSE:
			self.representatives: List[HouseRepresentative] = []
			desc = "house"
		else:
			self.representatives: List[SenateRepresentative] = []
			desc = "senate"
		self.coalitions: List[Coalition] = []
		self.broken_coalitions: List[Coalition] = []

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
			else:
				state = line[2]
				district = None
				name = line[10]
				party_data = line[11]

			# Choose the party
			if party_data == "DEMOCRAT":
				party = Parties.DEMOCRATIC
			elif party_data == "REPUBLICAN":
				party = Parties.REPUBLICAN
			else:
				party = Parties.OTHER

			# Create the representative
			if self.voting_body == VotingBodies.HOUSE:
				representative = HouseRepresentative("HR_0_" + str(rep_id + 1), state, district, name, party, 0,
													 self.t_max)
			else:
				representative = SenateRepresentative("SR_0_" + str(rep_id + 1), state, name, party, 0, self.t_max)
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
