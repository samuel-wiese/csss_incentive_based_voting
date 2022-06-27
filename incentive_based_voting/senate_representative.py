from representative import Representative
from party import Party


class SenateRepresentative(Representative):
	"""
	A member of the US Senate.
	"""

	def __init__(self, rep_id: str, state: str, name: str, party: Party, t: int, t_max: int):
		"""
		Initialises our Senate representative.

		Parameters
		----------
		rep_id : str
			The ID of the House representative.
		state : str
			The corresponding state.
		name : str
			The name of the representative.
		party : Party
			The party of the representative.
		t : int
			The current time step.
		t_max : int
			The number of years we are running the simulation for.
		"""

		super().__init__(rep_id, state, name, party, t, t_max)
