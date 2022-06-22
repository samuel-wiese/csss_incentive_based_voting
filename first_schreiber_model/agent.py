from __future__ import annotations

from typing import Optional, List, Union, TYPE_CHECKING
if TYPE_CHECKING:
	from voter import Voter
	from coalition import Coalition


class Agent:
	"""
	Represents a single voter or coalition with a type and an ID.
	"""

	def __init__(self, id_: str, type_: str, created_from_: List[Union[Voter, Coalition]]):
		"""
		Initialises the agent.

		Parameters
		----------
		id_ : str
			The ID of the agent.
		type_ : str
			The type of agent.
		created_from_ : List[Union[Voter, Coalition]]
			The list of agents this one consists of.
		"""

		self.id = id_
		self.type = type_
		self.created_from = created_from_
		self.policy_preference: Optional[float] = None

	def __repr__(self):
		"""
		Text representation of the agent.
		"""

		return "Agent (" + self.type + "|" + str(self.id) + "|" + str(self.policy_preference) + ")"

	def find_closest_agent(self, agents: List[Union[Voter, Coalition]]) -> Union[Voter, Coalition]:
		"""
		Finds the closest agent to this one in terms of policy preferences.

		Parameters
		----------
		agents : List[Union[Voter, Coalition]]
			The complete list of agents.

		Returns
		-------
		agents : Union[Voter, Coalition]
			The closest agent, policy-wise.
		"""

		# Find the closest agent in terms of policy preference
		closest_agent_num = None
		closest_agent_dist = 10000.0
		for i, agent in enumerate(agents):
			policy_differences = abs(agent.policy_preference - self.policy_preference)
			if policy_differences == 0:
				continue
			if closest_agent_dist > policy_differences:
				closest_agent_num = i
				closest_agent_dist = policy_differences

		# Return that agent
		return agents[closest_agent_num]

	def update_policy_preference(self) -> None:
		"""
		Updates the policy preferences of the agent.
		"""

		# Compute political preference of the coalition
		self.policy_preference = sum([agent.policy_preference for agent in self.created_from]) / len(self.created_from)
