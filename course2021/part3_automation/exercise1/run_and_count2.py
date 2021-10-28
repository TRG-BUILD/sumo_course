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
    "sumo-gui",
    "-n", "data/cross.net.xml",
    "-a", "data/radars.add.xml,data/early_bikes.tll.xml",
    "-r", "data/vehicles.rou.xml,data/cyclists.rou.xml,data/pedestrians.rou.xml"
    ]

# Connect TraCI to the simulation
traci.start(sumo_command)

# print all edges
edge_ids = traci.edge.getIDList()
print(edge_ids)

time = 0
# Simulate until there are no more vehicles
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep() # move simulation forward 1 step
    
    n_vehicles = 0
    for e_id in edge_ids:
        vehicle_ids = traci.edge.getLastStepVehicleIDs(e_id)
        for v_id in vehicle_ids:
            v_class = traci.vehicle.getVehicleClass(v_id)
            if v_class == "passenger":
                n_vehicles += 1

    print("time: {}, vehicles: {}".format(time, n_vehicles))

    time += 1

# disconnect
traci.close()