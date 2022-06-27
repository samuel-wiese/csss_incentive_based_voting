class Vote:
	"""
	A single vote.
	"""

	def __init__(self, political_position: float, popularity: float, voting_time: int):
		"""
		Initialises a new vote.
		"""

		self.political_position: float = political_position
		self.popularity: float = popularity
		self.voting_time: int = voting_time


# TODO: write a mechanism to create votes at random
