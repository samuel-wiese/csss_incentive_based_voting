import numpy as np

from representative import Representative
from policy import compute_distance


from typing import List


class Coalition:
	"""
	Represents a single coalition in the House or the Senate with a policy preference.
	"""

	def __init__(self, coa_id: str, created_from: List[Representative], t: int, t_max: int):
		"""
		Initialises a new coalition.

		Parameters
		----------
		coa_id : str
			The ID of the coalition.
		created_from : List[Representative]
			The initial list of representatives the coalition consists of.
		t : int
			The current time step.
		t_max : int
			The total number of time steps.
		"""

		# The ID of the representative
		self.id: str = coa_id

		# The initial representatives that are part of the coalition
		self.representatives: List[Representative] = created_from

		# Set the initial policy preference
		self.policy_preference_t: np.ndarray = np.zeros(t_max)
		self.policy_preference_t[t] = self.compute_policy_preference(t)

		# Set the initial influence of the coalition
		self.party_importance_t: np.ndarray = np.zeros(t_max)
		self.party_importance_t[t] = self.compute_party_importance(t)

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

		return sum([r.party_importance_t[t] * r.policy_preference_t[t] for r in self.representatives])\
			   / sum([r.party_importance_t[t] for r in self.representatives])

	def compute_party_importance(self, t: int) -> float:
		"""
		Compute party importance of the coalition by taking a sum over the party importances of its members.

		Parameters
		----------
		t : int
			The current time step.

		Returns
		-------
		party_importance : float
			The party importance of the coalition.
		"""

		return sum([r.party_importance_t[t] for r in self.representatives])


def coalition_formation(representatives: List[Representative], coalitions: List[Coalition],
						broken_coalitions: List[Coalition], t: int, t_max: int) -> None:
	"""
	Performs coalition formation in the House or the Senate.

	Parameters
	----------
	representatives : List[Representative]
		The list of current representatives.
	coalitions : List[Coalition]
		The list of current coalitions.
	broken_coalitions : List[Coalition]
		The list of broken coalitions.
	t : int
		Current time step.
	t_max : int
		The total number of time steps.
	"""

	# Representatives may join existing coalitions
	representatives_who_recently_joined = []
	for representative in representatives:

		# Find the closest coalition
		closest_coalition = None
		closest_coalition_dist = np.inf
		for coalition in coalitions:
			policy_dist = compute_distance(representative.policy_preference_t[t], coalition.policy_preference_t[t])
			if closest_coalition_dist > policy_dist:
				closest_coalition = coalition
				closest_coalition_dist = policy_dist

		# An agent is more likely to join a coalition if they are less powerful, if the coalition is more powerful, or
		# if the coalition is closer to them
		# TODO: Really fucking arbitrary inequality.
		if closest_coalition_dist < closest_coalition.party_importance_t[t] / representative.party_importance_t[t]:
			representative.coalition = closest_coalition
			closest_coalition.representatives.append(representative)

			# Re-compute policy-preference and importance of the coalition
			closest_coalition.policy_preference_t[t] = closest_coalition.compute_policy_preference(t)
			closest_coalition.party_importance_t[t] = closest_coalition.compute_party_importance(t)

			# Won't have these people join and leave in the same month
			representatives_who_recently_joined.append(representative)

	# Representatives may decide to leave existing coalitions
	for representative in representatives:
		if representative.coalition is None or representative in representatives_who_recently_joined:
			continue

		# Similar rules as before -- we are more likely to leave if the coalition doesn't represent us anymore and if we
		# don't depend on it
		# TODO: Should take the positions and strength of other existing coalitions into account
		policy_dist = compute_distance(representative.policy_preference_t[t],
									   representative.coalition.policy_preference_t[t])
		if policy_dist > representative.coalition.party_importance_t[t] / representative.party_importance_t[t]:
			representative.coalition.representatives.remove(representative)

			# Re-compute policy-preference and importance of the coalition
			representative.coalition.policy_preference_t[t] = representative.coalition.compute_policy_preference(t)
			representative.coalition.party_importance_t[t] = representative.coalition.compute_party_importance(t)

			representative.coalition = None

	# A coalition with only one existing member falls apart
	for coalition in coalitions:
		if len(coalition.representatives) == 1:
			coalition.representatives[0].coalition = None
			broken_coalitions.append(coalition)
			coalitions.remove(coalition)

	# Representatives may decide to form a new coalition; first, look for the pairwise closest representatives
	closest_representatives = []
	for representative1 in representatives:
		if representative1.coalition is not None:
			continue

		# Each representative looks for the representative closest to them
		closest_representative = None
		closest_representative_dist = np.inf
		for representative2 in representatives:
			if representative2.coalition is not None or representative1 == representative2:
				continue
			policy_dist = compute_distance(representative1.policy_preference_t[t],
										   representative2.policy_preference_t[t])
			if closest_representative_dist > policy_dist:
				closest_representative = representative2
				closest_representative_dist = policy_dist
		closest_representatives.append(closest_representative)

	# Second, check for new matches
	coalition_counter = 1
	for i, representative1 in enumerate(representatives):
		matched_representative = None
		for j, representative2 in enumerate(representatives):
			if (closest_representatives[i] is not None and closest_representatives[i].rep_id == representative2.rep_id
					and closest_representatives[j].rep_id == representative1.rep_id and i < j):
				matched_representative = representative2
				break
		if matched_representative is None:
			continue

		# Form a new coalition
		new_coalition = Coalition("CO_" + str(t) + "_" + str(coalition_counter),
								  [representative1, matched_representative], t, t_max)
		coalitions.append(new_coalition)
		coalition_counter += 1
