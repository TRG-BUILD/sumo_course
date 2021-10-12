Generating a simple intersection and demand like in part 1 exercise 1

## Generate network
The network is defined with following componenets:
- `nodes2.nod.xml`
- `edges2.edg.xml`
- `types2.type.xml`
- `connections2.con.xml`

Build network from componenets:
```
netconvert -n nodes2.nod.xml -e edges2.edg.xml -t types2.type.xml -x connections2.con.xml -o network2.net.xml
```

## Generate demands 

## Generate timed TLS
A simple tls can be generated within `netedit` by choosing Network Mode -> Traffic light mode, pressing on a junction and pressing create.  Tis corresponds to the following `netconvert` command. You can see other traffic light definition options of `netconvert` in [this doc](https://sumo.dlr.de/docs/netconvert.html#tls_building) 
```sh
netconvert --sumo-net-file network2.net.xml --tls.guess --output-file network3.net.xml
```

Saving the program with File -> Traffic lights -> Save TLS Program generates an additional file `program.tll.xml`. The `id` describes the junction, `type` describes whether the program is pre-timed to actuated and the `offset` describes coordination time offset. `programID` is often used to describe multiple programs on one junction, for example depending on the time of the day. 

```xml
<!--in program.tll.xml-->
<additionals>
    <tlLogic id="C" type="static" programID="0" offset="0">
        <phase duration="28" state="rrrrgGggrrrrgGggGrGr"/>
        <phase duration="5"  state="rrrrgGggrrrrgGggrrrr"/>
        <phase duration="3"  state="rrrryyggrrrryyggrrrr"/>
        <phase duration="6"  state="rrrrrrGGrrrrrrGGrrrr"/>
        <phase duration="3"  state="rrrrrryyrrrrrryyrrrr"/>
        <phase duration="28" state="gGggrrrrgGggrrrrrGrG"/>
        <phase duration="5"  state="gGggrrrrgGggrrrrrrrr"/>
        <phase duration="3"  state="yyggrrrryyggrrrrrrrr"/>
        <phase duration="6"  state="rrGGrrrrrrGGrrrrrrrr"/>
        <phase duration="3"  state="rryyrrrrrryyrrrrrrrr"/>
    </tlLogic>
</additionals>
```

The phases are held for a given `duration` and the configuration of the signal consists of letter for each controllable maneuver. The maneuvers are listed clockwise starting from the north and pedestrian maneuvers are always listed last according to [this doc](https://sumo.dlr.de/docs/Simulation/Traffic_Lights.html#signal_state_definitions). 

## Python tools
Lets try to use one of the python tools to adjust the time.
Adapt time accrding to [this doc](https://sumo.dlr.de/docs/Tools/tls.html#tlscycleadaptationpy).

Unlike our `flow` and `trip` definitions form [this doc](https://sumo.dlr.de/docs/Demand/Shortest_or_Optimal_Path_Routing.html) the coordinatinon tools only support the `vehicle` and `route` definitions.

We will use [Dynamic User Assignment](https://sumo.dlr.de/docs/Demand/Dynamic_User_Assignment.html) router `duarouter` to expand our `trip` and `flow` demand definitions to `routes`.

```sh
duarouter --route-files trips.rou.xml --net-file network3.net.xml --output-file single_routes.rou.xml
```

Windows:
```sh
python "%SUMO_HOME%\\tools\\tlsCycleAdaptation.py" -n network3.net.xml -r routes.rou.xml -o new_tls.add.xml --verbose
```

Linux:
```sh
python $SUMO_HOME/tools/tlsCycleAdaptation.py -n network3.net.xml -r routes.rou.xml -o newTLS.add.xml --verbose
```

```
python "%SUMO_HOME%\\tools\\tlsCycleAdaptation.py" --help
```

- `-y` yellow time
- `-a` all red time
- `-g` minimum green
- `-c` minimum cycle
- `-C` maximum cycle

```sh
sumo-gui -n network3.net.xml -r single_routes.rou.xml --additional-files newTLS.add.xml
```
That looks very good, but in reality those cars have alreadey passed, unfortionately it is based on historical data, that is not always a good predictor of the future. 

## Traffic signal coordination
Lets create a network consisting of 2 intersections. Unfortunately `netedit` does not have select and copy for network components. A simple but long solution is to draw the other intersection. A more hacky solution would be to make a copy of `network2.net.xml` that is offset by say 1000m on x, and combine 2 networks which is allowed according to [this doc](https://sumo.dlr.de/docs/netconvert.html#import). And since we want to learn something today lets try method 2.

Part 1 create a new offset network with different node names
```sh
netconvert -s network2.net.xml --offset.x -200 -o network2_left.net.xml --prefix left
netconvert -s network2.net.xml --offset.x 200 -o network2_right.net.xml --prefix right
```

Part 2 merge main and the offset network.
```sh
netconvert --sumo-net-file network2_left.net.xml,network2_right.net.xml -o network2_double.net.xml 
```

Generate some random trips for visuals.
```sh
python $SUMO_HOME/tools/randomTrips.py -n network3_double.net.xml -p 10 --validate --route-file double_routes.rou.xml
```

```sh
sumo-gui -n network3_double.net.xml -r double_routes.rou.xml 
```

Lets use the same principle to calculate the coordination offset to create green waves.

Adapt coordination according to [this doc](https://sumo.dlr.de/docs/Tools/tls.html#tlscoordinatorpy)

```sh
python $SUMO_HOME/tools/tlsCoordinator.py -n network3_double.net.xml -r double_routes.rou.xml -o tlsOffsets.add.xml
```

Here we can see negative value, so when we start the simulation the traffic light 1 has been in the first phase already for N seconds, the phase switch for a traffic light 2 will happen on time. Modify the existing tls program by loading the new tls additional file according to [this doc](https://sumo.dlr.de/docs/Simulation/Traffic_Lights.html#modifying_existing_tls-programs)
```sh
sumo-gui -n network3_double.net.xml -r double_routes.rou.xml --additional-files tlsOffsets.add.xml
```

## Actuated traffic control / demand responsive traffic control

With presence detectors, like induction loops:

Basic actiated traffic control is gap-based control that works by prolonging traffic phases whenever a continuous stream of traffic is detected according to [this doc](https://sumo.dlr.de/docs/Simulation/Traffic_Lights.html#traffic_lights_that_respond_to_traffic)

Generates E1 detectors automatically based on given time offset from stop lines.

The max-gap and detector gap values can be inserted into the `tlLogic` using the `key` `value` parameters:
- max-gap: the maximum time gap between successive vehicles that will cause the current phase to be prolonged (within maxDur limit)
- detector-gap: determines the time distance between the (automatically generated) detector and the stop line in seconds (at each lanes maximum speed). 
- show-detectors controls whether generated detectors will be visible or hidden in sumo-gui. 

Instead of a phase duration we are going to use minimum and maximum durations can be set using phase attributes `minDur` and `maxDur` according to [this doc](https://sumo.dlr.de/docs/Simulation/Traffic_Lights.html#phase_attributes).


With area detectors, like radar or camera:

`delay = dt ( 1 - v(t) / v_max )`  
Total delay is the summation of all delays


Generates E2 detectors automatically based on given `detectorRange` in meters.

## Generate detectors

## Link TLS to detectors

