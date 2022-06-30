from __future__ import annotations

from time_step import TimeStep
from event import Event

from typing import List, Dict


class Timeline:
	"""
	Represents the timeline of the model.
	"""

	def __init__(self, start_year: int, end_year: int):
		"""
		Initialises the timeline.

		Parameters
		----------
		start_year : int
			The start year.
		end_year : int
			The end year.
		"""

		# Events happening at each time step
		self.events: Dict[TimeStep, List[Event]] = {}
		time = TimeStep(start_year)
		end_time = TimeStep(end_year, 12)
		while time <= end_time:

			# New bills are introduced every month
			events: List[Event] = [Event.NEW_LEGISLATURE]
	
			# New poll results come every 3 months
			if time.month % 3 == 0:
				events.append(Event.NEW_POLLS)
	
			# New opinion formation happens every month
			events.append(Event.OPINION_FORMATION)
	
			# House election happens every 2 years
			if time.year % 2 == 0:
				events.append(Event.HOUSE_ELECTION)
	
			# Senate election happens every 6 years
			if time.year % 6 == 0:
				events.append(Event.SENATE_ELECTION)

			# Presidential election happens every 4 years
			if time.year % 4 == 0:
				events.append(Event.PRESIDENTIAL_ELECTION)

			self.events[time] = events
			time.inc()

		# Total number of time steps
		self.t_max = len(self.events.keys())
