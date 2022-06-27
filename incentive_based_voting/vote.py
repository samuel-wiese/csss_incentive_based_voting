from typing import List


class Vote:
	"""
	A single vote.
	"""

	def __init__(self, body: str, yeas: List[str], nays: List[str], t: int):
		"""
		Initialises a new policy preference.

		Parameters
		----------
		body : str
			The voting body.
		yeas : List[str]
			The IDs of the representatives that voted for the bill.
		nays : List[str]
			The IDs of the representatives that voted against the bill.
		t : int
			The current time step.
		"""

		# Base parameters
		self.body: str = body
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

		if self.body == "house":
			return len(self.yeas) >= 218
		elif self.body == "senate":
			return len(self.yeas) >= 51
		else:
			assert 0
