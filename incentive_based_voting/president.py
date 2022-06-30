from __future__ import annotations

import numpy as np

from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
	from parties import Parties
	from bill import Bill


class President:
	"""
	The president.
	"""

	def __init__(self, party: Parties):
		"""
		Initialises the president.

		TODO: Elections are missing.

		Parameters
		----------
		party : Party
			The party of the President.
		"""

		self.party: Parties = party

	def vote_for_bills(self, bills: List[Bill]):
		"""
		The president votes on a bunch of bills.

		Parameters
		----------
		bills : List[Bill]
			A list of bills.
		"""

		for bill in bills:
			if self.vote_for_bill(bill):
				bill.passed_president = True
				bill.passed = True

	def vote_for_bill(self, bill: Bill) -> bool:
		"""
		The president votes on a bill.

		Parameters
		----------
		bill : Bill
			The bill in question.

		Returns
		-------
		vote : Vote
			The resulting vote.
		"""

		# The president decides at random, but is more likely to vote for a bill, if the sponsor is from their party
		if self.party == bill.sponsor.party:
			return np.random.random() > 0.1
		else:
			return np.random.random() > 0.9
