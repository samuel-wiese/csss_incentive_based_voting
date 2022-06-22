from __future__ import annotations

from agent import Agent

from typing import List, Union, TYPE_CHECKING
if TYPE_CHECKING:
	from voter import Voter


class Coalition(Agent):
	"""
	Represents a single coalition with a policy preference among a one-dimensional interval [0,1].
	"""

	def __init__(self, id_: str, created_from_: List[Union[Voter, Coalition]]):
		"""
		Initialises the coalition.

		Parameters
		----------
		id_ : str
			The ID of the agent.
		created_from_ : List[Union[Voter, Coalition]]
			The list of agents this one consists of.
		"""

		super().__init__(id_, "coalition", created_from_)

		# Compute political preference of the coalition
		super().update_policy_preference()

	def find_closest_agent(self, agents: List[Union[Voter, __class__]]) -> Union[Voter, __class__]:
		"""
		Finds the closest agent to this one in terms of policy preferences.

		Parameters
		----------
		agents : List[Union[Voter, __class__]]
			The complete list of agents.

		Returns
		-------
		closest_agent : Union[Voter, __class__]
			The closest agent, policy-wise.
		"""

		return super().find_closest_agent(agents)

	def check_for_formation_stop(self, n_voters: int) -> bool:
		"""
		Checks if the coalition stops extending itself.

		Parameters
		----------
		n_voters : int
			The total number of initial voters.

		Returns
		-------
		stop : bool
			Whether the coalition stops forming.
		"""

		return len(self.created_from) > n_voters / 2
