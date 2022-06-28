import numpy as np

from party import Party
from parties import Parties
from voting_bodies import VotingBodies
from incentive import Incentive
from financial_incentive import FinancialIncentive
from bill import Bill
from policy import Policy

from typing import Optional


class CongressVoter:
	"""
	An agent allowed to vote in the US Congress -- either a representative or a coalition of representatives.
	"""

	def __init__(self, id_: str, party: Parties, voting_body: VotingBodies, t: int, t_max: int):
		"""
		Initialises our representative.

		Parameters
		----------
		id_ : str
			The ID of the voter.
		party : Party
			The party of the representative.
		voting_body : VotingBodies
			The corresponding voting body.
		t : int
			The current time step.
		t_max : int
			The number of years we are running the simulation for.
		"""

		# Basic parameters
		self.id: str = id_
		self.party: Parties = party
		self.voting_body: VotingBodies = voting_body
		self.t_init: int = t

		# Policy preferences over time
		self.policy_preference: Optional[Policy] = None

		# The party importance of the voter agent over time
		self.party_importance_t: np.ndarray = np.zeros(t_max)

		# Set the incentive
		self.incentive: Optional[Incentive] = None

	def vote(self, bill: Bill, democrats: Party, republicans: Party, otherparty: Party) -> bool:
		"""
		The agent votes on a bill.

		Parameters
		----------
		bill : Bill
			The bill.
		democrats : Party
			The democratic party.
		republicans : Party
			The republican party.
		otherparty : Party
			The other party.

		Returns
		-------
		decision : bool
			Whether the agent voted for or against the bill.
		"""

		# The agent is more likely to vote for the bill, if its political preference lie in its political space
		if bill.policy_range.in_range(self.policy_preference):
			metric_ideology = self.incentive.ideological
		else:
			metric_ideology = 0

		# The agent is more likely to vote for the bill, if they are taking small dollar donations and the vote is
		# popular, or if they are taking big dollar donations and the vote is not
		if self.incentive.financial == FinancialIncentive.SMALL_DOLLAR:
			metric_popularity_finance = bill.popularity
		else:
			metric_popularity_finance = 1.0 - bill.popularity

		# The agent is influenced by a certain amount of pressure from the party
		if self.party == Parties.DEMOCRATIC:
			if self.voting_body == VotingBodies.HOUSE:
				party_policy = democrats.policy_preference_house_t[-1]
			else:
				party_policy = democrats.policy_preference_senate_t[-1]
		elif self.party == Parties.REPUBLICAN:
			if self.voting_body == VotingBodies.HOUSE:
				party_policy = republicans.policy_preference_house_t[-1]
			else:
				party_policy = republicans.policy_preference_senate_t[-1]
		else:
			if self.voting_body == VotingBodies.HOUSE:
				party_policy = otherparty.policy_preference_house_t[-1]
			else:
				party_policy = otherparty.policy_preference_senate_t[-1]

		# The agent is more likely to vote for the bill if the party would and if they take big dollar donations
		if bill.policy_range.in_range(party_policy) and self.incentive.financial == FinancialIncentive.BIG_DOLLAR:
			metric_party_pressure = self.incentive.ideological
		else:
			metric_party_pressure = 0

		# Check if we're making it
		threshold = 2.0
		weights = {"ideology": 0.5, "popularity_finance": 0.3, "party_pressure": 0.2}
		metric = weights["ideology"] * metric_ideology + weights["popularity_finance"] * metric_popularity_finance\
				 + weights["party_pressure"] * metric_party_pressure
		return metric >= threshold
