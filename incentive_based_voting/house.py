from __future__ import annotations

from voting_body import VotingBody
from voting_bodies import VotingBodies

from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from bill import Bill
	from vote import Vote
	from party import Party


class House(VotingBody):
	"""
	The House.
	"""

	def __init__(self, year: int, t_max: int):
		"""
		Initialises the House.

		Parameters
		----------
		year : int
			The current year.
		t_max : int
			The number of years we are running the simulation for.
		"""

		super().__init__(year, t_max, VotingBodies.HOUSE)

	def vote(self, bill: Bill, democrats: Party, republicans: Party, otherparty: Party, t: int) -> Vote:
		"""
		The House makes a decision on a bill.

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

		return super().vote(bill, democrats, republicans, otherparty, t)
