from __future__ import annotations

import numpy as np

from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
	from representative import Representative


class Coalition:
	"""
	Represents a single coalition with a policy preference.
	"""

	def __init__(self, id_: str, created_from_: List[Representative], t: int, t_max: int):
		"""
		Initialises a new coalition.

		Parameters
		----------
		id_ : str
			The ID of the agent.
		created_from_ : List[Representative]
			The initial list of representatives the coalition consists of.
		t : int
			The current time step.
		t_max : int
			The total number of time steps.
		"""

		# The ID of the representative
		self.id: str = id_

		# The initial representatives that are part of the coalition
		self.representatives_t: List[List[Representative]] = [] * t_max
		self.representatives_t[t] = created_from_

		# Set the initial policy preference
		self.policy_preference_t: np.ndarray = np.zeros(t_max)
		self.policy_preference_t[t] = self.compute_policy_preference(t)

	def compute_policy_preference(self, t: int) -> float:
		"""
		Compute policy preference of the coalition by taking a simple weighted average.

		Parameters
		----------
		t : int
			The current time step.

		Returns
		-------
		policy_preference : float
			The policy preference of the coalition.
		"""

		return sum([r.party_importance_t[t] * r.policy_preference_t[t] for r in self.representatives_t[t]])\
			   / sum([r.party_importance_t[t] for r in self.representatives_t[t]])

	def has_simple_majority(self, n_representatives: int, t: int) -> bool:
		"""
		Checks if the coalition has a simple majority.

		Parameters
		----------
		n_representatives : int
			The total number of representatives.
		t : int
			The current time step.

		Returns
		-------
		stop : bool
			Whether the coalition has a simple majority.
		"""

		return len(self.representatives_t[t]) > n_representatives / 2


def get_initial_party_importance() -> float:
	"""
	Gets the representatives' initial importance in the party.
	"""

	return np.random.power(a=5)
