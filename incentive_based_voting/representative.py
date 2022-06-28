import numpy as np

from congress_voter import CongressVoter
from parties import Parties
from coalition import Coalition
from policy import Policy
from incentive import Incentive
from bill import Bill
from party import Party
from voting_bodies import VotingBodies

from typing import Optional


class Representative(CongressVoter):
	"""
	A US Congress representative.
	"""

	def __init__(self, id_: str, state: str, name: str, party: Parties, voting_body: VotingBodies, t: int, t_max: int):
		"""
		Initialises our representative.

		Parameters
		----------
		id_ : str
			The ID of the representative.
		state : str
			The corresponding state.
		name : str
			The name of the representative.
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
		super().__init__(id_, party, voting_body, t, t_max)
		self.state: str = state
		self.name: str = name

		# Set the initial policy preference
		self.policy_preference = Policy.pick_policy_preference_at_random(self.party)

		# Set the initial importance of the representative in terms of party pressure
		self.party_importance_t[0] = Representative.get_initial_party_importance()

		# Set the incentive at random
		self.incentive = Incentive.pick_incentive_at_random(self.party)

		# The corresponding coalition
		self.coalition: Optional[Coalition] = None

	def vote(self, bill: Bill, democrats: Party, republicans: Party, otherparty: Party) -> bool:
		"""
		The representative votes on a bill.

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
			Whether the representative voted for or against the bill.
		"""

		return super().vote(bill, democrats, republicans, otherparty)

	@staticmethod
	def get_initial_party_importance() -> float:
		"""
		Gets the representatives' initial importance in the party.
		"""

		return np.random.power(a=5)
