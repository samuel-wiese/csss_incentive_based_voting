import networkx as nx
import matplotlib.pyplot as plt

from congress_voter import CongressVoter
from coalition import Coalition

from typing import List


def create_network(coalitions: List[Coalition],
                   representatives: List[CongressVoter]) -> nx.Graph:
    """
    Draws a new network to include what happened in the current time step.

    Parameters
    ----------
    graph : nx.Graph
        Our graph.
    coalitions : List[Coalition]
        The set of current coalitions.
    representatives : List[CongressVoter]
        The set of all.
    """

    # Plot nodes and edges for representatives in coalitions
    graph = nx.Graph()

    for i, coalition in enumerate(coalitions):
        for j, representative in enumerate(coalition.representatives):
            graph.add_node(representative.id, pos=(representative.policy_preference.libertarian,
                                                   representative.policy_preference.progressive))
        for j1, representative1 in enumerate(coalition.representatives):
            for j2, representative2 in enumerate(coalition.representatives):
                if j1 != j2:
                    graph.add_edge(representative1.id, representative2.id)

    representatives_in_coalitions = [coalition.representatives for coalition in coalitions]
    representatives_in_coalitions = [representative for representatives in representatives_in_coalitions
                                     for representative in representatives]

    # Plot nodes without edges for representatives not in coalitions
    for i, representative in enumerate(representatives):
        if representative not in representatives_in_coalitions:
            graph.add_node(representative.id, pos=(representative.policy_preference.libertarian,
                                                   representative.policy_preference.progressive))

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
