import numpy as np
import csv
import os

from coalition import Coalition
from house_representative import HouseRepresentative
from senate_representative import SenateRepresentative
from party import Party
from bill import Bill
from vote import Vote

from typing import List


class VotingBody:
	"""
	A voting body in the US congress.
	"""

	# TODO: Keen to add an enum here.

	def __init__(self, year: int, t_max: int, body: str):
		"""
		Initialises the voting body.

		Parameters
		----------
		year : int
			The current year.
		t_max : int
			The number of years we are running the simulation for.
		body : str
			Which voting body we are initiating.
		"""

		# Base parameters
		self.year: int = year
		self.t_max: int = t_max
		self.body: str = body

		# Votes by year
		self.votes_by_year: List[List[Vote]] = []

		# Representatives and coalitions
		if self.body == "house":
			self.representatives: List[HouseRepresentative] = []
		elif self.body == "senate":
			self.representatives: List[SenateRepresentative] = []
		else:
			assert 0
		self.coalitions: List[Coalition] = []
		self.broken_coalitions: List[Coalition] = []

		# Take data and create new representatives
		senate_data = []
		f = open(os.path.dirname(__file__) + "/data/" + self.body + ".csv", "r")
		for line in csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
			senate_data.append(line)
		senate_data = np.array(senate_data)
		year_ind = np.where(senate_data[:, 0] == str(year))
		start_line, end_line = np.min(year_ind), np.max(year_ind)
		for rep_id, line in enumerate(senate_data[start_line:end_line + 1]):

			# Take data
			if self.body == "house":
				state = line[2]
				district = line[7]
				name = line[11]
				party_data = line[12]
			elif self.body == "senate":
				state = line[2]
				district = None
				name = line[10]
				party_data = line[11]
			else:
				assert 0

			# Choose the party
			if party_data == "DEMOCRAT":
				party = Party.DEMOCRAT
			elif party_data == "REPUBLICAN":
				party = Party.REPUBLICAN
			else:
				party = Party.OTHER

			# Create the representative
			if self.body == "house":
				representative = HouseRepresentative("HR_0_" + str(rep_id + 1), state, district, name, party, 0,
													 self.t_max)
			elif self.body == "senate":
				representative = SenateRepresentative("SR_0_" + str(rep_id + 1), state, name, party, 0, self.t_max)
			else:
				assert 0
			self.representatives.append(representative)

	def vote(self, bill: Bill, t: int) -> Vote:
		"""
		The voting body makes a decision on a bill.

		Parameters
		----------
		bill : Bill
			The bill in question.
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
			coalition_ids = [r.rep_id for r in coalition.representatives]
			if bill.policy_range.in_range(coalition.policy_preference_t[t]):
				yeas.extend(coalition_ids)
			else:
				nays.extend(coalition_ids)

		# Have all other representatives vote
		for representative in self.representatives:
			if representative.coalition is None:
				if bill.policy_range.in_range(representative.policy_preference_t[t]):
					yeas.append(representative.rep_id)
				else:
					nays.append(representative.rep_id)

		# Return the results
		return Vote(self.body, yeas, nays, t)
