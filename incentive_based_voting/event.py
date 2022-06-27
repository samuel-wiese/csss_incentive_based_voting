from enum import Enum


class Event(Enum):
	"""
	Events that may happen each year.
	"""

	NEW_LEGISLATURE: 1
	NEW_POLLS: 2
	OPINION_FORMATION: 3
	HOUSE_ELECTION: 4
	SENATE_ELECTION: 5
