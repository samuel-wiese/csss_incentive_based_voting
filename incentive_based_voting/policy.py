import numpy as np

from party import Party


class Policy:
	"""
	A policy preference.
	"""

	def __init__(self, libertarian: float, progressive: float):
		"""
		Initialises a new policy preference.

		Parameters
		----------
		libertarian : float
			Determines how libertarian the policy preference is.
		progressive : float
			Determines how progressive the policy preference is.
		"""

		assert 0.0 <= libertarian <= 1.0
		assert 0.0 <= progressive <= 1.0

		self.libertarian = libertarian
		self.authoritarian = 1.0 - libertarian

		self.progressive = progressive
		self.conservative = 1.0 - progressive


def pick_policy_preference_at_random(party: Party) -> Policy:
	"""
	Selects a policy preference at random based on the Party.

	TODO: These are arbitrary.

	Parameters
	----------
	party : Party
		The party.

	Returns
	-------
	policy : Policy
		The chosen policy.
	"""

	if party == Party.DEMOCRAT:
		libertarian = 0.2 + 0.6 * np.random.random()
		progressive = 0.7 + 0.2 * np.random.random()
	elif party == Party.REPUBLICAN:
		libertarian = 0.4 + 0.3 * np.random.random()
		progressive = 0.2 + 0.2 * np.random.random()
	else:
		libertarian = np.random.random()
		progressive = np.random.random()

	return Policy(libertarian, progressive)


def compute_distance(p1: Policy, p2: Policy) -> float:
	"""
	Computes the (Euclidean) distance between two policies.

	TODO: Again, somewhat arbitrary.

	Parameters
	----------
	p1 : Policy
		The first policy.
	p2 : Policy
		The second policy.

	Returns
	-------
	distance : float
		The (Euclidean) distance between two policies.
	"""

	return np.sqrt((p1.libertarian - p2.libertarian) ** 2 + (p1.progressive - p2.progressive) ** 2)
