from __future__ import annotations

import numpy as np

from congress_voter import CongressVoter
from policy import Policy
from financial_incentive import FinancialIncentive
from incentive import Incentive

from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
	from representative import Representative
	from bill import Bill
	from party import Party
	from voting_bodies import VotingBodies
	from parties import Parties


class Coalition(CongressVoter):
	"""
	Represents a single coalition in the House or the Senate with a policy preference.
	"""

	def __init__(self, id_: str, created_from: List[Representative], voting_body: VotingBodies, t: int, t_max: int):
		"""
		Initialises a new coalition.

		Parameters
		----------
		id_ : str
			The ID of the coalition.
		created_from : List[Representative]
			The initial list of representatives the coalition consists of.
		voting_body : VotingBodies
			The corresponding voting body.
		t : int
			The current time step.
		t_max : int
			The total number of time steps.
		"""

		# Basic parameters
		super().__init__(id_, created_from[0].party, voting_body, t, t_max)

		# The initial representatives that are part of the coalition
		self.representatives: List[Representative] = created_from

		# The corresponding party
		self.party: Parties = self.representatives[0].party

		# Set the initial policy preference
		self.policy_preference = self.compute_policy_preference(t)

		# Set the initial influence of the coalition
		self.party_importance_t[t] = self.compute_party_importance(t)

		# Set the incentives
		self.incentive = self.compute_incentives()

	def compute_policy_preference(self, t: int) -> Policy:
		"""
		Compute policy preference of the coalition by taking a simple weighted average.

		Parameters
		----------
		t : int
			The current time step.

		Returns
		-------
		policy : Policy
			The policy preference of the coalition.
		"""

		libertarian = sum([r.party_importance_t[t] * r.policy_preference.libertarian for r in self.representatives])\
					  / sum([r.party_importance_t[t] for r in self.representatives])
		progressive = sum([r.party_importance_t[t] * r.policy_preference.progressive for r in self.representatives]) \
					  / sum([r.party_importance_t[t] for r in self.representatives])

		return Policy(libertarian, progressive)

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

	def compute_incentives(self) -> Incentive:
		"""
		Compute the incentive structure of the coalition.

		Returns
		-------
		incentive : Incentive
			The incentive structure of the coalition
		"""

		if FinancialIncentive.BIG_DOLLAR in [r.incentive.financial for r in self.representatives]:
			financial_incentive = FinancialIncentive.BIG_DOLLAR
		else:
			financial_incentive = FinancialIncentive.SMALL_DOLLAR
		ideological_incentive = float(np.mean([r.incentive.ideological for r in self.representatives]))
		party_pressure = float(np.mean([r.incentive.party_pressure for r in self.representatives]))

		return Incentive(financial_incentive, ideological_incentive, party_pressure)

	def vote(self, bill: Bill, democrats: Party, republicans: Party, otherparty: Party) -> bool:
		"""
		The coalition votes on a bill together.

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
	def coalition_formation(representatives: List[Representative], coalitions: List[__class__],
							broken_coalitions: List[__class__], voting_body: VotingBodies, t: int, t_max: int)\
			-> List[__class__]:
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
		voting_body : VotingBodies
			The corresponding voting body.
		t : int
			Current time step.
		t_max : int
			The total number of time steps.

		Returns
		-------
		new_coalitions : List[Coalition]
			The new list of coalitions.
		"""

		# Representatives may join existing coalitions
		representatives_who_recently_joined = []
		for representative in representatives:
			if len(coalitions) == 0:
				break

			# Find the closest coalition
			closest_coalition = None
			closest_coalition_dist = np.inf
			for coalition in coalitions:
				if coalition.party != representative.party:
					continue
				policy_dist = Policy.compute_distance(representative.policy_preference, coalition.policy_preference)
				if closest_coalition_dist > policy_dist:
					closest_coalition = coalition
					closest_coalition_dist = policy_dist

			# An agent is more likely to join a coalition if they are less powerful, if the coalition is more powerful, or
			# if the coalition is closer to them
			if closest_coalition_dist\
					< 0.05 * closest_coalition.party_importance_t[t] / representative.party_importance_t[t]\
					and representative.incentive.financial == closest_coalition.incentive.financial:
				representative.coalition = closest_coalition
				closest_coalition.representatives.append(representative)

				# Re-compute policy-preference and importance of the coalition
				closest_coalition.policy_preference = closest_coalition.compute_policy_preference(t)
				closest_coalition.party_importance_t[t] = closest_coalition.compute_party_importance(t)
				closest_coalition.incentive = closest_coalition.compute_incentives()

				# Won't have these people join and leave in the same month
				representatives_who_recently_joined.append(representative)

		# Representatives may decide to leave existing coalitions
		for representative in representatives:
			if len(coalitions) == 0:
				break
			if representative.coalition is None or representative in representatives_who_recently_joined:
				continue

			# Similar rules as before -- we are more likely to leave if the coalition doesn't represent us anymore and if we
			# don't depend on it
			# TODO: Should take the positions and strength of other existing coalitions into account
			# TODO: might want to include incentives here, in particular financial ones
			# TODO: the inequality needs to be normalised
			policy_dist = Policy.compute_distance(representative.policy_preference,
												  representative.coalition.policy_preference)
			if policy_dist > 0.1 * representative.coalition.party_importance_t[t]\
					/ representative.party_importance_t[t]:
				representative.coalition.representatives.remove(representative)

				# Re-compute policy-preference and importance of the coalition
				if len(representative.coalition.representatives) > 0:
					representative.coalition.policy_preference = representative.coalition.compute_policy_preference(t)
					representative.coalition.party_importance_t[t]\
						= representative.coalition.compute_party_importance(t)
					representative.coalition.incentive = representative.coalition.compute_incentives()

				representative.coalition = None

		# A coalition with only one or no existing members falls apart
		del_coalitions = []
		for i, coalition in enumerate(coalitions):
			if len(coalition.representatives) <= 1:
				if len(coalition.representatives) == 1:
					coalition.representatives[0].coalition = None
				broken_coalitions.append(coalition)
				del_coalitions.append(i)
		coalitions = [coalitions[i] for i in range(len(coalitions)) if i not in del_coalitions]

		# Representatives may decide to form a new coalition; first, look for the pairwise closest representatives
		closest_representatives = []
		for representative1 in representatives:
			if representative1.coalition is not None:
				closest_representatives.append(None)
				continue

			# Each representative looks for the representative closest to them
			closest_representative = None
			closest_representative_dist = np.inf
			for representative2 in representatives:
				if representative2.coalition is not None or representative1 == representative2:
					continue
				if representative1.party != representative2.party:
					continue
				policy_dist = Policy.compute_distance(representative1.policy_preference, representative2.policy_preference)
				if closest_representative_dist > policy_dist:
					closest_representative = representative2
					closest_representative_dist = policy_dist
			closest_representatives.append(closest_representative)

		# Second, check for new matches
		coalition_counter = 1
		for i, representative1 in enumerate(representatives):
			matched_representative = None
			for j, representative2 in enumerate(representatives):
				if (closest_representatives[i] is not None and closest_representatives[j] is not None
						and closest_representatives[i].id == representative2.id
						and closest_representatives[j].id == representative1.id and i < j):
					matched_representative = representative2
					break
			if matched_representative is None:
				continue

			# Form a new coalition
			new_coalition = Coalition("CO_" + str(t) + "_" + str(coalition_counter),
									  [representative1, matched_representative], voting_body, t, t_max)
			coalitions.append(new_coalition)
			coalition_counter += 1

			# Update the representatives
			representative1.coalition = new_coalition
			matched_representative.coalition = new_coalition

		return coalitions
