from parties import Parties
from policy import Policy
from house_representative import HouseRepresentative
from senate_representative import SenateRepresentative

from typing import List


class Party:
	"""
	Political parties.
	"""

	def __init__(self, party: Parties):
		"""
		Initialising a party.

		Parameters
		----------
		party : Parties
			Which party we are initialising.
		"""

		self.party: Parties = party
		self.policy_preference_house_t: List[Policy] = []
		self.policy_preference_senate_t: List[Policy] = []

	def update_policy_preference(self, house_representatives: List[HouseRepresentative],
								 senate_representatives: List[SenateRepresentative], t: int) -> None:
		"""
		Updates the policy preferences of the whole party in the House and the Senate.

		Parameters
		----------
		house_representatives : List[HouseRepresentative]
			The list of all representatives in the House.
		senate_representatives : List[SenateRepresentative]
			The list of all representatives in the Senate.
		t : int
			The current time step.
		"""

		# For the House
		party_house_reps = [r for r in house_representatives if r.party == self.party]
		libertarian = sum([r.party_importance_t[t] * r.policy_preference.libertarian for r in party_house_reps])\
					  / sum([r.party_importance_t[t] for r in party_house_reps])
		progressive = sum([r.party_importance_t[t] * r.policy_preference.progressive for r in party_house_reps]) \
					  / sum([r.party_importance_t[t] for r in party_house_reps])
		self.policy_preference_house_t.append(Policy(libertarian, progressive))

		# For the Senate
		party_senate_reps = [r for r in senate_representatives if r.party == self.party]
		libertarian = sum([r.party_importance_t[t] * r.policy_preference.libertarian for r in party_senate_reps])\
					  / sum([r.party_importance_t[t] for r in party_senate_reps])
		progressive = sum([r.party_importance_t[t] * r.policy_preference.progressive for r in party_senate_reps]) \
					  / sum([r.party_importance_t[t] for r in party_senate_reps])
		self.policy_preference_senate_t.append(Policy(libertarian, progressive))
