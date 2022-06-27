import numpy as np

from party import Party
from financial_incentive import FinancialIncentive


class Incentive:
	"""
	The incentive structure of a representative.
	"""

	def __init__(self, financial_incentive: FinancialIncentive, ideological: float, party_pressure: float):
		"""
		Initialises the incentive structure.

		TODO: removed the "incumbent"-parameter for now, because it would be a dynamic one.

		Parameters
		----------
		financial_incentive : FinancialIncentive
			The financial incentive a representative, either small or big dollar.
		ideological : float
			The ideological
		party_pressure : float
			How much pressure from other members the representative faces.
		"""

		self.financial: FinancialIncentive = financial_incentive
		self.ideological: float = ideological
		self.party_pressure: float = party_pressure

	def __repr__(self):
		"""
		String-representation of an incentive.
		"""

		return "Incentive (Fin: " + str(self.financial) + ", IDEO: " + str(self.ideological) + ", PP: "\
			   + str(self.party_pressure) + ")"


def pick_incentive_at_random(party: Party) -> Incentive:
	"""
	Selects an incentive at random based on the Party.

	TODO: These are arbitrary.

	Parameters
	----------
	party : Party
		The party.

	Returns
	-------
	incentive : Incentive
		The chosen incentive.
	"""

	if party == Party.DEMOCRAT:
		financial_incentive = np.random.choice([FinancialIncentive.SMALL_DOLLAR, FinancialIncentive.BIG_DOLLAR],
											   p=[0.7, 0.3])
		ideological_incentive = 0.4 + 0.4 * np.random.random()
		party_pressure = np.random.random()
	elif party == Party.REPUBLICAN:
		financial_incentive = np.random.choice([FinancialIncentive.SMALL_DOLLAR, FinancialIncentive.BIG_DOLLAR],
											   p=[0.3, 0.7])
		ideological_incentive = 0.4 + 0.4 * np.random.random()
		party_pressure = np.random.random()
	else:
		financial_incentive = np.random.choice([FinancialIncentive.SMALL_DOLLAR, FinancialIncentive.BIG_DOLLAR],
											   p=[0.9, 0.1])
		ideological_incentive = 0.2 * np.random.random()
		party_pressure = 0.1 * np.random.random()

	return Incentive(financial_incentive, ideological_incentive, party_pressure)
