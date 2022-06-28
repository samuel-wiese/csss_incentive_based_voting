from representative import Representative
from parties import Parties
from voting_bodies import VotingBodies


class HouseRepresentative(Representative):
	"""
	A member of the US House of Representatives.
	"""

	def __init__(self, rep_id: str, state: str, district: str, name: str, party: Parties, t: int, t_max: int):
		"""
		Initialises our House representative.

		Parameters
		----------
		rep_id : str
			The ID of the House representative.
		state : str
			The corresponding state.
		district : str
			The corresponding district.
		name : str
			The name of the representative.
		party : Parties
			The party of the representative.
		t : int
			The current time step.
		t_max : int
			The number of years we are running the simulation for.
		"""

		super().__init__(rep_id, state, name, party, VotingBodies.HOUSE, t, t_max)
		self.district = district
