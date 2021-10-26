# Step 1: establish path to traci
import os, sys
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

# Step 2: add traci to be able to access its functionality
import traci

# Step 3: compose a sumo command you would like to run 
sumo_command = ["sumo", "-n", "network.net.xml", "-r", "demands.rou.xml"]

# Step 4: open connection between sumo and traci
traci.start(sumo_command)

# Step 5: take simulation steps until there are no more vehicles in the network
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep() # move simulation forward 1 step

    ###
    # Here you can decide what to do with simulation data at each step
    ###

# Step 6: close connection between sumo and traci
traci.close()