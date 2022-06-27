from voting_body import VotingBody
from bill import Bill
from vote import Vote


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

		super().__init__(year, t_max, "house")

	def vote(self, bill: Bill, t: int) -> Vote:
		"""
		The House makes a decision on a bill.

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

		return super().vote(bill, t)
