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

Adjust time!
Adapt time accrding to [this doc](https://sumo.dlr.de/docs/Tools/tls.html#tlscycleadaptationpy)

Adapt coordination according to [this doc](https://sumo.dlr.de/docs/Tools/tls.html#tlscoordinatorpy)
## Generate detectors

## Link TLS to detectors

