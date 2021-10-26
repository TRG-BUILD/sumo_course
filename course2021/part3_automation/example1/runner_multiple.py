import os, sys
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci

for i in range(0, 5):

    # here is a good place to introduce changes to the simulation settings such
    # as different input demands or output file names
    print("simulation run: ", i)


    sumo_command = ["sumo", "-n", "network.net.xml", "-r", "demands.rou.xml"]
    traci.start(sumo_command)

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep() # move simulation forward 1 step

        ###
        # Here you can decide what to do with simulation data at each step
        ###

    traci.close()