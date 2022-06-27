from event import Event

from typing import List


def create_timeline(t_max: int) -> List[List[Event]]:
	"""
	Creates a list of events happening each month.

	Parameters
	----------
	t_max : int
		The number of time steps in months.

	Returns
	-------
	timeline: List[Event]
		The list of events for each year.
	"""

	timeline = []
	for month in range(t_max):

		# New legislature comes every month
		events = [Event.NEW_LEGISLATURE]

		# New poll results come every 6 months
		if month % 6 == 0:
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
