from __future__ import annotations

import numpy as np

from agent import Agent

from typing import List, Union, TYPE_CHECKING
if TYPE_CHECKING:
	from coalition import Coalition


class Voter(Agent):
	"""
	Represents a single voter with a policy preference among a one-dimensional interval [0,1].
	"""

	def __init__(self, id_: str):
		"""
		Initialises our voter.

		Parameters
		----------
		id_ : str
			The ID of the voter.
		"""

		super().__init__(id_, "voter", [self])

		# Choose a policy preference at random
		self.policy_preference = int(id_)

	def find_closest_agent(self, agents: List[Union[__class__, Coalition]]) -> Union[__class__, Coalition]:
		"""
		Finds the closest agent to this one in terms of policy preferences.

		Parameters
		----------
		agents : List[Union[__class__, Coalition]]
			The complete list of agents.

		Returns
		-------
		closest_agent : Union[__class__, Coalition]
			The closest agent, policy-wise.
		"""

		return super().find_closest_agent(agents)
