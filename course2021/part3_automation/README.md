## TraCI Hello World

So far our best way to run a simulation was to call a following command:

```sh
sumo-gui -n network.net.xml -r demands.rou.xml
```

First of all we need to ensure that `python` knows where to loof ro TraCI. Originally TraCI is installed into `SUMO_HOME/tools` directory, we just need to provide path to it.

```python
 import os, sys
 if 'SUMO_HOME' in os.environ:
     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
     sys.path.append(tools)
 else:
     sys.exit("please declare environment variable 'SUMO_HOME'")
```

When the path is established we can import `traci`
```python
import traci
```

```python
sumo_command = ["sumo-gui", "-n", "network.net.xml", "-r", "demands.rou.xml"]
```

Lets make a minimal example of running a simulation. Simulation always starts with establishing the connection between `traci` and `sumo`:
```python
traci.start(sumo_command)
```

Simulation is run by asking `traci` to take a `simulationStep()` that advances time and updates the network and vehcles. Simulation steps are taken until there are no more vehicles running or waiting to be inserted into the network. This is taken care of using `simulation.getMinExpectedNumber()` according to [this doc](https://sumo.dlr.de/pydoc/traci._simulation.html):
```python
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep() # move simulation forward 1 step

    ###
    # Here you can decide what to do with simulation data at each step
    ###

```

Simulation always ends with closing the connection between `traci` and `sumo`:
```python
traci.close()
```


