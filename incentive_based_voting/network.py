import networkx as nx
import matplotlib.pyplot as plt

from congress_voter import CongressVoter
from coalition import Coalition
from representative import Representative

from typing import List


def create_network(representatives: List[Representative]) -> nx.Graph:
    """
    Draws a new network to include what happened in the current time step.

    Parameters
    ----------
    graph : nx.Graph
        Our graph.
    representatives : List[CongressVoter]
        The set of all.
    """

    # Plot nodes and edges for representatives in coalitions
    graph = nx.Graph()

    for i1, representative1 in enumerate(representatives):
        graph.add_node(representative1.id, pos=(representative1.policy_preference.libertarian,
                                                representative1.policy_preference.progressive))
        if representative1.coalition is not None:
            for i2, representative2 in enumerate(representative1.coalition.representatives):
                if ~graph.has_edge(representative2.id, representative1.id):
                    graph.add_edge(representative1.id, representative2.id)

    return graph


def draw_network(graph: nx.Graph, t: int) -> None:
    """
    Draws our network.

    Parameters
    ----------
    graph : nx.Graph
        Our graph.
    t : int
        The current time step.
    """

    pos = nx.get_node_attributes(graph, 'pos')
    nx.draw(graph, pos, node_size=20)
    plt.savefig("networks/network_t{}.pdf".format(t), dpi=300, tight_layout=True)
