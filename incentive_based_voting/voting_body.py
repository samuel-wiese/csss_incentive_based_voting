from enum import Enum


class VotingBody(Enum):
	"""
	Voting bodies in the US congress.
	"""

	SENATE: 0
	HOUSE: 1

	# TODO: turn this into something we can inherit from, maybe
