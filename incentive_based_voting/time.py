from event import Event

from typing import List, Optional


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


def create_timeline(start_year: int, end_year: int) -> List[List[Event]]:
	"""
	Creates a list of events happening each month.

	Parameters
	----------
	start_year : int
		The start year.
	end_year : int
		The end year.

	Returns
	-------
	timeline: List[Event]
		The list of events for each year.
	"""

	# Create time
	time = Time(start_year)
	timeline = []
	for month in range(t_max):

		# New bills are introduced every month
		events = [Event.NEW_LEGISLATURE]

		# New poll results come every 3 months
		if month % 3 == 0:
			events.append(Event.NEW_POLLS)

		# New opinion formation happens every month
		events.append(Event.OPINION_FORMATION)

		# House election happens every 2 years
		if month % 24 == 0:
			events.append(Event.HOUSE_ELECTION)

		# Senate election happens every 6 years
		# TODO: I am aware that not all states have senate elections at the same time, but let's go with that for now.
		if month % 72 == 0:
			events.append(Event.SENATE_ELECTION)

		timeline.append(events)

	return timeline
