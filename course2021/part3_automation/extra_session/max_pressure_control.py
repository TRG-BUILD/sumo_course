# Ensure Python knows where TraCI is
import os, sys
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci

# define helper functions
def movement_pressure(det_in, det_out):
    """
    Calculate maneuver pressure based on a pair of detectors 
    """
    incoming = traci.lanearea.getJamLengthVehicle(det_in)
    outgoing = traci.lanearea.getJamLengthVehicle(det_out)
    return incoming - outgoing

def phase_pressure(phases, detectors):
    """
    Calculate phase pressure aggregating all of its maneuver pressures
    """
    pressures = {}
    for phase_id, movement_ids in phases.items():
        p_total = 0
        for m_id in movement_ids:
            det_in, det_out = detectors[m_id]
            p_total += movement_pressure(det_in, det_out)
        pressures[phase_id] = p_total

    return pressures

movement_detectors = [
    ("e2det_NC_2", "e2det_CW_2"),
    ("e2det_NC_3", "e2det_CS_2"),
    ("e2det_NC_4", "e2det_CE_2"),

    ("e2det_EC_2", "e2det_CN_2"),
    ("e2det_EC_3", "e2det_CW_2"),
    ("e2det_EC_4", "e2det_CS_2"),

    ("e2det_SC_2", "e2det_CE_2"),
    ("e2det_SC_3", "e2det_CN_2"),
    ("e2det_SC_4", "e2det_CW_2"),

    ("e2det_WC_2", "e2det_CS_2"),
    ("e2det_WC_3", "e2det_CE_2"),
    ("e2det_WC_4", "e2det_CN_2")
]

n_phases = 4
phases = {
    0: [0, 1, 2, 6, 7, 8],
    1: [2, 8],
    2: [3, 4, 5, 9, 10, 11],
    3: [5, 11],
}

min_green = 10
phase_timers = {
    0: 0,
    1: 0,
    2: 0,
    3: 0
}

transitions = {
    1: 4,
    2: 5,
    3: 6,
    0: 7
}

# compose the SUMO simulation command
sumo_command = [
    "sumo-gui",
    "-n", "data/cross.net.xml",
    "-a", "data/radars.add.xml,data/program_for_control.tll.xml",
    "-r", "data/vehicles.rou.xml,data/cyclists.rou.xml,data/pedestrians.rou.xml"
    ]

# Connect TraCI to the simulation
traci.start(sumo_command)

time = 0
# Simulate until there are no more vehicles
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep() # move simulation forward 1 step
    
    ###
    # controller implementation here
    phase = traci.trafficlight.getPhase("C")
    
    # calculate pressure and max pressure phase
    pressures = phase_pressure(phases, movement_detectors)
    max_pressure_phase = phase
    if any(pressures.values()):
        max_pressure_phase = max(pressures, key=pressures.get)

    if phase > n_phases:
        print("time: {}, status: transition phase {}, pressures: {}, max pressure phase: {}".format(
            time, phase, pressures, max_pressure_phase))
        continue

    if phase_timers[phase] < min_green:
        phase_timers[phase] += 1
        print("time: {}, status: min_green, current phase: {}, pressures: {}, max pressure phase: {}".format(
            time, phase, pressures, max_pressure_phase))
        continue

    # calulate phase switch
    if phase != max_pressure_phase:
        traci.trafficlight.setPhase("C", transitions[max_pressure_phase])
        phase_timers[phase] = 0
        print("time: {}, status: trainsition from: {} to {}, pressures: {}, max pressure phase: {}".format(
            time, phase, max_pressure_phase, pressures, max_pressure_phase))    
    else:
        traci.trafficlight.setPhase("C", phase)
        phase_timers[phase] + 1
        print("time: {}, status: extend phase, current phase: {}, pressures: {}, max pressure phase: {}".format(
            time, phase, pressures, max_pressure_phase))
        
    ###

    time += 1

# disconnect
traci.close()