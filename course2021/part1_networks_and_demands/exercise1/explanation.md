## Exercise 1

### Creating network from components

1. Creating `nodes.nod.xml` with nodes named `C`-center, `E`-east, `W`-west, `N`-north, `S`-south.
Legs are chosen to be 200 meters.
```xml
<!--in nodes.nod.xml-->
<nodes>
    <node id="C" x="0.0" y="0.0"/>
    <node id="E" x="-200.0" y="0.0"/>
    <node id="W" x="200.0" y="0.0"/>
    <node id="N" x="0.0" y="200.0"/>
    <node id="S" x="0.0" y="-200.0"/>
</nodes>
```

2. Creating a road type in `types.type.xml` with 1 lane and max speed of 50 km/h that corresponds to 13.3 m/s.

```xml
<!--in types.type.xml-->
<types>
    <type id="1L13.3" numLanes="1" speed="13.3"/>
</types>
```

3. Creating incoming and outgoing approaches in `edges.edg.xml` and assigning the correct type.

```xml
<!--in edges.edg.xml-->
<edges>
    <edge from="E" to="C" id="EC" type="1L13.3"/>
    <edge from="W" to="C" id="WC" type="1L13.3"/>
    <edge from="N" to="C" id="NC" type="1L13.3"/>
    <edge from="S" to="C" id="SC" type="1L13.3"/>

    <edge from="C" to="E" id="CE" type="1L13.3"/>
    <edge from="C" to="W" id="CW" type="1L13.3"/>
    <edge from="C" to="N" id="CN" type="1L13.3"/>
    <edge from="C" to="S" id="CS" type="1L13.3"/>
</edges>

```

4. Converting the raw network components to a network file
```sh
netconvert -n nodes.nod.xml -e edges.edg.xml -t types.type.xml -o network.net.xml
```

Preview the network to see that it looks correct:
```sh
netedit network.net.xml
```
![](doc/connections1.png)

5. Looking at the connections in Network -> Connection Mode it looks like SUMO has created a turnaround connection for us. Lets specify that we only want forward, left and right turns to be available. Connections can be edited in `netedit` but instead we will make `connections.con.xml` based on [this doc](https://sumo.dlr.de/docs/Networks/PlainXML.html#connection_descriptions).

```xml
<!--in connections.con.xml-->
<connections>
  <connection from="EC" to="CN"/>
  <connection from="EC" to="CW"/>
  <connection from="EC" to="CS"/>

  <connection from="NC" to="CW"/>
  <connection from="NC" to="CS"/>
  <connection from="NC" to="CE"/>

  <connection from="WC" to="CS"/>
  <connection from="WC" to="CE"/>
  <connection from="WC" to="CN"/>

  <connection from="SC" to="CE"/>
  <connection from="SC" to="CN"/>
  <connection from="SC" to="CW"/>
</connections>
```

```sh
netconvert -n nodes.nod.xml -e edges.edg.xml -t types.type.xml -x connections.con.xml -o network.net.xml
```

Preview the network to see that it looks correct:
```sh
netedit network.net.xml
```
![](doc/connections2.png)

### Creating a demand component
To define the demand we need to create a `routes.rou.xml` file to specify:
- car and a bus vehicle types with `vType` tag
- 3 routes with `route` tag
- 3 car flows with `flow` tag
- 4 bus trips with `vehicle` tag (`trip` could be used too, but instead of route you need to provide `from` and `to` edge ids) 

We will use the parameters from [this doc](https://sumo.dlr.de/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.html#available_vehicle_attributes) to specify the demands:


```xml
<routes>
    <vType id="bus1" maxSpeed="20.00" vClass="bus" color="red"/>
    <vType id="car1" maxSpeed="50.00" vClass="passenger" color="green"/>

    <route edges="EC CN" color="yellow" id="routeEtoN"/>
    <route edges="EC CS" color="yellow" id="routeEtoS"/>
    <route edges="EC CW" color="yellow" id="routeEtoW"/>

    <flow id="c0" type="car1" begin="0.00" route="routeEtoN" end="500.00" number="50"/>
    <flow id="c1" type="car1" begin="0.00" route="routeEtoW" end="500.00" number="50"/>
    <flow id="c2" type="car1" begin="0.00" route="routeEtoS" end="500.00" number="50"/>

    <vehicle id="b0" type="bus1" depart="100.00" route="routeEtoN"/>
    <vehicle id="b1" type="bus1" depart="200.00" route="routeEtoN"/>
    <vehicle id="b2" type="bus1" depart="300.00" route="routeEtoN"/>
    <vehicle id="b3" type="bus1" depart="400.00" route="routeEtoN"/>
</routes>
```

Simulate the results
```sh
sumo-gui -n network.net.xml -r routes.rou.xml
```

![](doc/sim.gif)
