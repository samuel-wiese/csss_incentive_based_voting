import numpy as np
import os
import csv

from house_representative import HouseRepresentative
from party import Party


class House:
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

		self.year: int = year
		self.t_max: int = t_max

		# Representatives
		self.representatives = []

		# Take data
		house_data = []
		f = open(os.path.dirname(__file__) + "/data/house.csv", "r")
		for line in csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
			house_data.append(line)
		house_data = np.array(house_data)
		year_ind = np.where(house_data[:, 0] == str(year))
		start_line, end_line = np.min(year_ind), np.max(year_ind)
		for rep_id, line in enumerate(house_data[start_line:end_line + 1]):

			# Create new House representatives
			state = line[2]
			district = line[7]
			name = line[11]
			if line[12] == "DEMOCRAT":
				party = Party.DEMOCRAT
			elif line[12] == "REPUBLICAN":
				party = Party.REPUBLICAN
			else:
				party = Party.OTHER
			representative = HouseRepresentative("HR" + str(rep_id), state, district, name, party, 0, self.t_max)
			self.representatives.append(representative)
