from voter import Voter
from coalition import Coalition
from network import initialise_network, update_network, draw_network

from typing import List, Union


# Number of voters
n_voters = 51

# Initialise voters
voters = [Voter(str(voter_id + 1)) for voter_id in range(n_voters)]
agents: List[Union[Voter, Coalition]] = voters

# For keeping track and for drawing
graph = initialise_network(agents)

# Go
for t in range(1000):

	# Every voter and every coalition looks for the closest voter or coalition
	closest_agents = []
	for agent in agents:
		closest_agent = agent.find_closest_agent(agents)
		closest_agents.append(closest_agent)

	# Look for matches for all of them
	new_coalitions = []
	new_matched_agents = []
	for i, agent in enumerate(agents):

		# Check for matches
		agent_matched = None
		for j, agent_ in enumerate(agents):
			if closest_agents[i].id == agent_.id and closest_agents[j].id == agent.id and i < j:
				agent_matched = agent_
				break
		if agent_matched is None:
			continue

		# Match found, create a new coalition and remove the used ones
		new_coalition = Coalition("(" + agent.id + "|" + agent_matched.id + ")", created_from_=[agent, agent_matched])
		new_coalitions.append(new_coalition)
		new_matched_agents.append([agent, agent_matched])

	# Add new coalitions and remove matched agents from the active list of agents
	agents.extend(new_coalitions)
	for agent, agent_ in new_matched_agents:
		agents.remove(agent)
		agents.remove(agent_)

	# Check if a coalition has a simple majority
	for agent in agents:
		if agent.type == "coalition" and agent.check_for_formation_stop(n_voters):
			agents.remove(agent)

	# Update the network
	update_network(graph, new_coalitions, new_matched_agents, t)

	# If there are fewer than two agents left, quit
	if len(agents) < 2:
		break

# Draw our graph
draw_network(graph)
