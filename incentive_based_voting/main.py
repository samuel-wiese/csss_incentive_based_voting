from congress import Congress
from timeline import create_timeline
from event import Event
from coalition import coalition_formation
from president import President


# Settings
year = 2010  # the current (start) year
t_max = 120  # the total number of time steps in months
n_bills = 500  # the number of bills that are brought before congress each month

# Data


# Initialise the Congress
congress = Congress(year, t_max)

# Create a timeline and run
timeline = create_timeline(t_max)
for t, monthly_events in enumerate(timeline):
	for event in monthly_events:

		# New bills are being voted on every month
		# TODO: this depends on the incentives
		if event == Event.NEW_LEGISLATURE:

			# Create a few new bills and try to pass them
			congress.generate_some_bills(n_bills, t)
			congress.attempt_passing_bills(t)

			# The president makes the final decision




		# New poll results come out every 3 months
		if event == Event.NEW_POLLS:

			# TODO: either use data or do scenario generation

			pass

		# New coalition formation occurs every month
		if event == Event.OPINION_FORMATION:
			coalition_formation(congress.house.representatives, congress.house.coalitions,
								congress.house.broken_coalitions, t, t_max)
			coalition_formation(congress.senate.representatives, congress.senate.coalitions,
								congress.senate.broken_coalitions, t, t_max)

		# Elections in the House happen every 2 years
		if event == Event.HOUSE_ELECTION:
			# TODO: nice for scenario generation, but ignore for now
			pass

		# Elections in the Senate happen every 6 years
		if event == Event.SENATE_ELECTION:
			# TODO: nice for scenario generation, but ignore for now
			pass


# TODO: Add a framework for network plotting in 2D
# TODO: Add a framework for Congress election results
