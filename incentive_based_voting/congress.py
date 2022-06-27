import numpy as np

from house import House
from senate import Senate
from bill import Bill

from house_representative import HouseRepresentative
from senate_representative import SenateRepresentative
from coalition import Coalition

from typing import List, Union
from copy import deepcopy


class Congress:
	"""
	The congress.
	"""

	def __init__(self, year: int, t_max: int):
		"""
		Initialises a new congress.

		Parameters
		----------
		year : int
			The current year.
		t_max : int
			The number of years we are running the simulation for.
		"""

		# Voting bodies
		self.house = House(year, t_max)
		self.senate = Senate(year, t_max)

		# Bills by year
		self.bills_by_year: List[List[Bill]] = []

	def generate_some_bills(self, n_bills: int, t: int) -> None:
		"""
		Generates bills at random.

		Parameters
		----------
		n_bills : int
			The number of bills we are generating each month.
		t : int
			The current time step.
		"""

		# Choose sponsors at random
		sponsor_ids = np.random.choice(range(len(self.house.representatives) + len(self.house.coalitions)
											 + len(self.senate.representatives) + len(self.senate.coalitions)), n_bills)
		sponsors: List[Union[HouseRepresentative, SenateRepresentative, Coalition]] = []
		for sponsor_id in sponsor_ids:
			if sponsor_id < len(self.house.representatives):
				sponsors.append(self.house.representatives[sponsor_id])
			elif sponsor_id < len(self.house.representatives) + len(self.house.coalitions):
				sponsors.append(self.house.coalitions[sponsor_id])
			elif sponsor_id < len(self.house.representatives) + len(self.house.coalitions)\
					+ len(self.senate.representatives):
				sponsors.append(self.senate.representatives[sponsor_id])
			else:
				sponsors.append(self.senate.coalitions[sponsor_id])

		# Generates corresponding bills
		bills = []
		for i in range(n_bills):
			bill = Bill(sponsors[i], t)
			bills.append(bill)
		self.bills_by_year.append(bills)

	def attempt_passing_bills(self, t: int) -> None:
		"""
		Bills are sent through congress.

		Parameters
		----------
		t : int
			The current time step.
		"""

		# House
		votes = []
		for bill in self.bills_by_year[-1]:
			vote = self.house.vote(bill, t)
			bill.passed_house = vote.passed
			votes.append(vote)
		self.house.votes_by_year.append(deepcopy(votes))

		# Senate
		votes = []
		for bill in self.bills_by_year[-1]:
			if bill.passed_house:
				vote = self.senate.vote(bill, t)
				bill.passed_senate = vote.passed
				votes.append(vote)
		self.senate.votes_by_year.append(deepcopy(votes))
