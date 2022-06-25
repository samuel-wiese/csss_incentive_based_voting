

class Incentives:
	"""
	The incentive structure of a representative.
	"""

	def __init__(self, financial_incentive: bool, ideological: float, party_pressure: float):
		"""
		Initialises the incentive structure.

		Parameters
		----------
		financial_incentive : bool
			The financial incentive a representative, either small or big dollar.
		ideological : float
			The ideological
		party_pressure : float

		"""

		self.financial: bool = financial_incentive
		self.ideological: float = ideological
		self.party_pressure: float = party_pressure






class Financial_incentive(Enum):




