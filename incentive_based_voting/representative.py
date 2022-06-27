from __future__ import annotations

import numpy as np

from party import Party
from policy import Policy, pick_policy_preference_at_random
from coalition import Coalition, get_initial_party_importance
from incentive import pick_incentive_at_random

from typing import List, Optional


class Representative:
	"""
	A US Congress representative.
	"""

	def __init__(self, rep_id: str, state: str, name: str, party: Party, t: int, t_max: int):
		"""
		Initialises our representative.

		Parameters
		----------
		rep_id : str
			The ID of the House representative.
		state : str
			The corresponding state.
		name : str
			The name of the representative.
		party : Party
			The party of the representative.
		t : int
			The current time step.
		t_max : int
			The number of years we are running the simulation for.
		"""

		# Basic parameters
		self.rep_id: str = rep_id
		self.state: str = state
		self.name: str = name
		self.party: Party = party
		self.t_joined_congress: int = t

		# Set the initial policy preference
		self.policy_preference_t: List[Policy] = []
		self.policy_preference_t[0] = pick_policy_preference_at_random(self.party)

		# Set the incentive
		self.incentive = pick_incentive_at_random(self.party)

		# Set the initial importance of the representative in terms of party pressure
		self.party_importance_t: np.ndarray = np.zeros(t_max)
		self.party_importance_t[0] = get_initial_party_importance()

		# The corresponding coalition
		self.coalition: Optional[Coalition] = None
