# Ensure Python knows where TraCI is
import os, sys
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci

# compose the SUMO simulation command
sumo_command = [
    "sumo",
    "-n", "data/cross.net.xml",
    "-a", "data/radars.add.xml,data/early_bikes.tll.xml",
    "-r", "data/vehicles.rou.xml,data/cyclists.rou.xml,data/pedestrians.rou.xml"
    ]

# Connect TraCI to the simulation
traci.start(sumo_command)

# Simulate until there are no more vehicles
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep() # move simulation forward 1 step

# disconnect
traci.close()