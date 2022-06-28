from voting_bodies import VotingBodies

from typing import List


class Vote:
	"""
	A single vote.
	"""

	def __init__(self, voting_body: VotingBodies, yeas: List[str], nays: List[str], t: int):
		"""
		Initialises a new policy preference.

		Parameters
		----------
		voting_body : VotingBodies
			The corresponding voting body.
		yeas : List[str]
			The IDs of the representatives that voted for the bill.
		nays : List[str]
			The IDs of the representatives that voted against the bill.
		t : int
			The current time step.
		"""

		# Base parameters
		self.voting_body: VotingBodies = voting_body
		self.yeas: List[str] = yeas
		self.nays: List[str] = nays
		self.time_of_vote: int = t

		# Checks whether the vote has passed
		self.passed: bool = self.check_if_passed()

	def check_if_passed(self) -> bool:
		"""
		Checks if a vote has passed the respective voting body.

		Returns
		-------
		passed : bool
			Whether the vote has passed.
		"""

		if self.voting_body == VotingBodies.HOUSE:
			return len(self.yeas) >= 218
		else:
			return len(self.yeas) >= 51
