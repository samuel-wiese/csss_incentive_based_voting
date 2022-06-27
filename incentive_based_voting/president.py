import numpy as np

from party import Party


class President:
	"""
	The president.
	"""

	def __init__(self):
		"""
		Initialises the president.
		"""

		#

	def vote(self, bill: Bill, t: int) -> Vote:
		"""
		The president votes on a bill.

		Parameters
		----------
		bill : Bill
			The bill in question.
		t : int
			The current time step.

		Returns
		-------
		vote : Vote
			The resulting vote.
		"""

		# 


		# Have all coalitions vote
		for coalition in self.coalitions:
			coalition_ids = [r.rep_id for r in coalition.representatives]
			if bill.policy_range.in_range(coalition.policy_preference_t[t]):
				yeas.extend(coalition_ids)
			else:
				nays.extend(coalition_ids)

		# Have all other representatives vote
		for representative in self.representatives:
			if representative.coalition is None:
				if bill.policy_range.in_range(representative.policy_preference_t[t]):
					yeas.append(representative.rep_id)
				else:
					nays.append(representative.rep_id)

		# Return the results
		return Vote(self.body, yeas, nays, t)



