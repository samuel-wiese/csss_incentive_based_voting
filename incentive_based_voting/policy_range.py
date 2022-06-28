import numpy as np

from policy import Policy


class PolicyRange:
	"""
	A policy preference range.
	"""

	def __init__(self, libertarian_min: float, libertarian_max: float, progressive_min: float, progressive_max: float):
		"""
		Initialises a new policy range.

		Parameters
		----------
		libertarian_min : float
			Determines the lower libertarian bound for the policy range.
		libertarian_max : float
			Determines the upper libertarian bound for the policy range.
		progressive_min : float
			Determines the lower progressive bound for the policy range.
		progressive_max : float
			Determines the upper progressive bound for the policy range.
		"""

		assert 0.0 <= libertarian_min <= libertarian_max <= 1.0
		assert 0.0 <= progressive_min <= progressive_max <= 1.0

		self.libertarian_min = libertarian_min
		self.libertarian_max = libertarian_max
		self.authoritarian_min = 1.0 - self.libertarian_max
		self.authoritarian_max = 1.0 - self.libertarian_min

		self.progressive_min = progressive_min
		self.progressive_max = progressive_max
		self.conservative_min = 1.0 - progressive_max
		self.conservative_max = 1.0 - progressive_min

	def in_range(self, policy: Policy) -> bool:
		"""
		Checks if a policy preference lies in the policy range.

		Parameters
		----------
		policy : Policy
			A policy.

		Returns
		-------
		is_in_range : bool
			Whether a policy preference lies in the policy range.
		"""

		return (self.libertarian_min <= policy.libertarian <= self.libertarian_max)\
			   and (self.progressive_min <= policy.progressive <= self.progressive_max)

	@staticmethod
	def pick_policy_range_at_random(policy: Policy) -> __class__:
		"""
		Selects a policy range at random based on a given policy preference.

		Parameters
		----------
		policy : Policy
			The policy preference.

		Returns
		-------
		policy_range : PolicyRange
			The chosen policy range.
		"""

		wiggle = 0.2

		libertarian_min = max(0.0, policy.libertarian - wiggle * np.random.random())
		libertarian_max = min(1.0, policy.libertarian + wiggle * np.random.random())
		progressive_min = max(0.0, policy.progressive - wiggle * np.random.random())
		progressive_max = min(1.0, policy.progressive + wiggle * np.random.random())

		return PolicyRange(libertarian_min, libertarian_max, progressive_min, progressive_max)
