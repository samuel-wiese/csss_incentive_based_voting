import numpy as np

from house_representative import HouseRepresentative
from senate_representative import SenateRepresentative
from coalition import Coalition
from policy_range import PolicyRange

from typing import Union


class Bill:
	"""
	A single bill that will be voted on.
	"""

	def __init__(self, sponsor: Union[HouseRepresentative, SenateRepresentative, Coalition], t: int):
		"""
		Initialises a new bill.

		Parameters
		----------
		sponsor : Union[HouseRepresentative, SenateRepresentative, Coalition]
			The sponsor of the bill.
		t: int
			The current time step.
		"""

		# The sponsor(s) of the bill
		self.sponsor: Union[HouseRepresentative, SenateRepresentative, Coalition] = sponsor

		# The popularity of the bill in the general population
		self.popularity: float = Bill.get_popularity_at_random()

		# The time of introduction
		self.voting_time: int = t

		# Picks the admissible policy range of the bill at random, based on the policy preference of the sponsor(s)
		self.policy_range: PolicyRange = PolicyRange.pick_policy_range_at_random(self.sponsor.policy_preference)

		# The outcome of the bill
		self.passed_house: bool = False
		self.passed_senate: bool = False
		self.passed_president: bool = False
		self.passed: bool = False

	@staticmethod
	def get_popularity_at_random() -> float:
		"""
		Chooses the popularity of a bill at random.

		TODO: I think this will be crucial.

		Returns
		-------
		popularity : float
			The popularity of the bill.
		"""

		return np.random.random()
