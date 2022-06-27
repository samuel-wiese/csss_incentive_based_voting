import numpy as np
import csv
import os


class Senate:
	"""
	The Senate.
	"""

	def __init__(self, year: int, t_max: int):
		"""
		Initialises the Senate.

		Parameters
		----------
		year : int
			The current year.
		t_max : int
			The number of years we are running the simulation for.
		"""

		self.year: int = year


		n_senate = 100


		# TODO: add a data-fetching method

