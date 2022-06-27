from congress import Congress
from timeline import create_timeline


# Settings
year = 2010  # the current (start) year
t_max = 120  # the total number of time steps in months

# Initialise the Congress
congress = Congress(year, t_max)

# Create a timeline and run
timeline = create_timeline(t_max)
for monthly_events in timeline:

	# TODO: do something

	for event in monthly_events:


		pass




# TODO: leave this up; need it for opinion formation

# Initialise the representatives
representatives = Representative.initialise_representatives(t_max)

# Go
for t in range(t_max):

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
