import networkx as nx
import matplotlib.pyplot as plt

from voter import Voter
from coalition import Coalition

from typing import List, Union


def initialise_network(initial_agents: List[Voter]) -> nx.Graph:
	"""
	Initialises our network.

	Parameters
	----------
	initial_agents : List[Voter]
		The initial set of agents.

	Returns
	-------
	g : nx.Graph
		The initialised graph.
	"""

	graph = nx.Graph()
	for agent in initial_agents:
		graph.add_node(agent.id, pos=(agent.policy_preference, 0))

	return graph


def update_network(graph: nx.Graph, new_coal: List[Coalition], new_match: List[List[Union[Voter, Coalition]]], t: int)\
		-> None:
	"""
	Updates the network to include what happened in the current time step.

	Parameters
	----------
	graph : nx.Graph
		Our graph.
	new_coal : List[Coalition]
		The set of new coalitions.
	new_match : List[List[Union[Voter, Coalition]]]
		Pairs of agents matched to form the new coalitions.
	t : int
		The current time step.
	"""

	for i, new_coalition in enumerate(new_coal):
		graph.add_node(new_coalition.id, pos=(new_coalition.policy_preference, -(t + 1)))
		graph.add_edge(new_coalition.id, new_match[i][0].id)
		graph.add_edge(new_coalition.id, new_match[i][1].id)


def draw_network(graph: nx.Graph) -> None:
	"""
	Draws our network.

	Parameters
	----------
	graph : nx.Graph
		Our graph.
	"""

	pos = nx.get_node_attributes(graph, 'pos')
	nx.draw(graph, pos, node_size=20)
	plt.savefig("network.pdf", dpi=300, tight_layout=True)
