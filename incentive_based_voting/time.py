from typing import Optional


class Time:
	"""
	Representation of time in the model.
	"""

	def __init__(self, year: int, month: Optional[int] = None):
		"""
		Initialises time.

		Parameters
		----------
		year : int
			The year.
		month : int
			The month.
		"""

		self.year: int = year
		if month is None:
			self.month: int = 1
		else:
			self.month: int = month

	def __le__(self, other):
		"""
		Overloads the lesser-or-equal operator.

		Parameters
		----------
		other : Time
			Another time object.
		"""

		return (self.year < other.year) or (self.year == other.year and self.month <= other.month)

	def __ge__(self, other):
		"""
		Overloads the greater-or-equal operator.

		Parameters
		----------
		other : Time
			Another time object.
		"""

		return (self.year > other.year) or (self.year == other.year and self.month >= other.month)

	def inc(self) -> None:
		"""
		Moves one month forward.
		"""

		if self.month < 12:
			self.month += 1
		else:
			self.year += 1
			self.month = 1
