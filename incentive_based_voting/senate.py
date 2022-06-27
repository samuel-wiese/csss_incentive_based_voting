import numpy as np
import csv
import os

from senate_representative import SenateRepresentative
from party import Party


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
		self.t_max: int = t_max

		# Representatives
		self.representatives = []

		# Take data
		senate_data = []
		f = open(os.path.dirname(__file__) + "/data/senate.csv", "r")
		for line in csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
			senate_data.append(line)
		senate_data = np.array(senate_data)
		year_ind = np.where(senate_data[:, 0] == str(year))
		start_line, end_line = np.min(year_ind), np.max(year_ind)
		for rep_id, line in enumerate(senate_data[start_line:end_line + 1]):

			# Create new House representatives
			state = line[2]
			name = line[10]
			if line[11] == "DEMOCRAT":
				party = Party.DEMOCRAT
			elif line[11] == "REPUBLICAN":
				party = Party.REPUBLICAN
			else:
				party = Party.OTHER
			representative = SenateRepresentative("HR" + str(rep_id), state, name, party, 0, self.t_max)
			self.representatives.append(representative)
