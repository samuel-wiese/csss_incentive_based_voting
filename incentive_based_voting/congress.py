from house import House
from senate import Senate


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

		self.house = House(year, t_max)
		self.senate = Senate(year, t_max)
