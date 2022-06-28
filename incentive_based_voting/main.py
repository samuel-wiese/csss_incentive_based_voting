from congress import Congress
from timeline import Timeline
from event import Event
from coalition import Coalition
from president import President
from party import Party
from parties import Parties
from voting_bodies import VotingBodies


# Settings
start_year = 2010
end_year = 2020
n_bills = 500  # the number of bills that are brought before congress each month

# Create a timeline
timeline = Timeline(start_year, end_year)

# Initialise the Congress
congress = Congress(start_year, timeline.t_max)

# Create our parties
democrats = Party(Parties.DEMOCRATIC)
republicans = Party(Parties.REPUBLICAN)
otherparty = Party(Parties.OTHER)

# Initialise the President
president = President(Parties.DEMOCRATIC)

# Run
for t, time in enumerate(timeline.events):
	for event in timeline.events[time]:

		# New bills are being voted on every month
		if event == Event.NEW_LEGISLATURE:

			# Update party policy preferences
			democrats.update_policy_preference(congress.house.representatives, congress.senate.representatives, t=0)
			republicans.update_policy_preference(congress.house.representatives, congress.senate.representatives, t=0)
			otherparty.update_policy_preference(congress.house.representatives, congress.senate.representatives, t=0)

			# Create a few new bills and try to pass them
			congress.generate_some_bills(n_bills, t)
			congress.attempt_passing_bills(democrats, republicans, otherparty, t)

			# The president makes the final decision
			president.vote_for_bills(congress.bills_successful)

		# New poll results come out every 3 months
		if event == Event.NEW_POLLS:
			# TODO: either use data or do scenario generation
			pass

		# New coalition formation occurs every month
		if event == Event.OPINION_FORMATION:
			Coalition.coalition_formation(congress.house.representatives, congress.house.coalitions,
										  congress.house.broken_coalitions, VotingBodies.HOUSE, t, timeline.t_max)
			Coalition.coalition_formation(congress.senate.representatives, congress.senate.coalitions,
										  congress.senate.broken_coalitions, VotingBodies.SENATE, t, timeline.t_max)

		# Elections in the House happen every 2 years
		if event == Event.HOUSE_ELECTION:
			# TODO: nice for scenario generation, but ignore for now
			pass

		# Elections in the Senate happen every 6 years
		if event == Event.SENATE_ELECTION:
			# TODO: nice for scenario generation, but ignore for now
			pass

		# Presidential elections happen every 4 years
		if event == Event.PRESIDENTIAL_ELECTION:
			# TODO: nice for scenario generation, but ignore for now
			pass

print("Done!")
