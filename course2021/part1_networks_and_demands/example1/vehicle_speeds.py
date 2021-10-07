# import necessary packages for processing xml, inputs
# and generating plots

import xml.etree.ElementTree as ET
import argparse
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

# create input
ag = argparse.ArgumentParser()
ag.add_argument("-i", "--input", required=True, help="input .xml file")
ag.add_argument("-t", "--type", type=str, default="normal_car", help="type of the vehicle to fetch data for")
args = vars(ag.parse_args())

# build xml file tree from input
tree = ET.parse(args["input"])
print("stiff")

# loop over timesteps that are immediate children of the root
# get time values
data = []
for timestep in tqdm(tree.getroot()):
    time = float(timestep.attrib["time"])

    # loop over vehicles in each timestep and collect and average
    # speeds only for vehicles of the type we input as argument
    avg_speed = 0
    count = 0
    for vehicle in timestep:
        if vehicle.attrib["type"] == args["type"]:
            veh_speed = float(vehicle.attrib["speed"])
            avg_speed += veh_speed
            count += 1
            
    data.append([time, avg_speed / count])

# plot it
data = np.array(data)
fig, ax = plt.subplots()
ax.plot(data[:,0], data[:,1], "rx")
ax.set_xlabel("time [s]")
ax.set_ylabel("average speed [m/s]")
ax.set_title(f'Average speed evolution of type: {args["type"]}')
plt.show()


