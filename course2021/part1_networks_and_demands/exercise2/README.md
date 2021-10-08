## Exercise 2

- Model your favourite street in Aalborg that contains at least 3 intersections. Figure out how draw the network on top of a background image layer with [this](https://sumo.dlr.de/docs/sumo-gui.html#showing_background_images) and [that](https://www.youtube.com/watch?v=rTT0vKzikpg&ab_channel=AkharapongTepkeaw) links.
- Find a way to add bicycle lanes using `netconvert`.

- Experiment with adding different demands:
  - Single trips.
  - Flows.
  - `randomTrips.py` with / or without edge weights.
  - Turn ratios using [this doc](https://sumo.dlr.de/docs/Tools/Turns.html).
  - OD matrix with `od2trips.py` tool using [this doc](https://sumo.dlr.de/docs/Demand/Importing_O/D_Matrices.html).

### Image import
Lets try to model the [Stolpedalsvej in Aalborg](https://www.google.com/maps/@57.0355594,9.8815782,249m/data=!3m1!1e3). First step is to get a high resolution ortophoto with known boundary coordinates. QGIS can be used to get the `stolpedalsvej.png` image and its extents in UTM coordinates.
- `xmin = 553236.457`
- `ymin = 6321511.525`
- `xmax = 553746.574`
- `ymax = 6321872.214`

That gives us `width` of `510.1m` and `height` of `360.7m`.

![](doc/qgis.png)

This gives is an image width and image center that want to put it to `netedit`. Using Edit -> Edit Visualisation (F9) the image background layer can be added to `netedit`. 

![](doc/netedit_image.png)

By default the image is resized to a 100 by 100 m standart grid cell, using calculated width and height we can give the correct size to the image as follows:

![](doc/netedit_image2.png)

### Network drawing
From that point we need to follow the road as closely as possible, locating the nodes at the centers of the intersection. Node positions can be changed using Network mode -> Move button. The roads crossing the Stolpedalsvej are cut at some arbitrary length.

![](doc/netedit_image3.png)

The standart road width fits well in all the places except the Hasserisvej where on the north side we get a separating curb and on the south side road is wider. We can model the first case with edge properties `shapeStart` `shapeEnd` and second case with edge property `width`. Manual definition of `shapeStart` and `shapeEnd` is tedious since the offsets are in global coordinate system, luckily, `netedit` allows to isolate start and end points of the shape of the edge by shift + click on the edge according to [this doc](https://sumo.dlr.de/docs/Netedit/neteditUsageExamples.html#specifying_the_complete_geometry_of_an_edge_including_endpoints).

![](doc/connection1.png)
![](doc/connection2.png)

This lets us define more advanced intersection geometry that doesn`t have to co-incide with the main node of the intersection. We will not bother changing the connections as they look reasonable. Also, the traffic controls on the Hasserisvej-Stolpedalsvej is not modelled, since its outside of the scope of this exercise.

![](doc/net.png)

### Adding bike lanes

Option	Description
```sh
netconvert --sumo-net-file stolpedalsvej.net.xml --output-file stolpedalsvej2.net.xml --bikelanes.guess
```
Unfortunately during the `netconvert` call we got issued a dozen of warnings:
```
Warning: Lane '-gneE10_0' is not connected from any incoming edge at junction 'gneJ14'.
```

That according to [this doc](https://sumo.dlr.de/docs/netconvert.html#warnings_during_import) is best resolved by inspecting the network visually. Looking at the new network in the `netedit` se can indeed see that the bike lanes are added to the edges, but are not connected propperly to eachother.

![](doc/wrong_bikelanes.png)

Apart from adding the connections manually in `netedit`, a good timesaving alternative is to rebuilding entire network from its raw files using `netconvert`. To acheive that we first need to split the network into its nodes and edges as follows.

```sh
netconvert --sumo-net-file stolpedalsvej.net.xml --plain-output-prefix stolpedalsvej
```
The result of that are the files `stolpedalsvej.nod.xml, stolpedalsvej.edg.xml, stolpedalsvej.con.xml, stolpedalsvej.tll.xml`, last 2 files corresponding to connections and traffic lights we can ignore and re-build the network only using the nodes and edges.

```sh
netconvert --node-files stolpedalsvej.nod.xml --edge-files stolpedalsvej.edg.xml --bikelanes.guess --output-file stolpedalsvej2.net.xml
```

This time no warnings was issued so we can inspect the new network and verify that all the bike paths are now connected.

![](doc/correct_bikelanes.png)

Last thing before starting with the demand will be to take care of the edge naming on our network, since we will use `from` `to` parameters of the router to define the sources and the destinations of our trips. The system is arbitrary, i have decided to name southern origin edges as `S1, S2, ...`, and southern destination edges as `-S1, -S2, ...`. Same principle goes to the northern part, and the central part being Stolpedalsvej itself.

![](doc/renamed.png)

This concludes network building of this exercise.

### Traffic demand composed of vehicles, busses and bicycles
 [this doc](https://sumo.dlr.de/docs/Demand/Shortest_or_Optimal_Path_Routing.html)
- Single trips for busses
- Flows for vehicles and bicycles

random trips for vehicles and bicycles

### Single trips and flows
Similar to exercise 1, lets define single trips of busses and flows of cars in `routes1.rou.xml`. The cars will go from Thorsens Alle south to the Hasserisvej north and the busses will travel from Stolpedasvej east to Thorsens Alle north.

```xml
<!--in routes1.rou.xml-->
<routes>
    <vType id="bus1" maxSpeed="20.00" vClass="bus" color="red"/>
    <vType id="car1" maxSpeed="50.00" vClass="passenger" color="green"/>

    <flow id="c0" type="car1" begin="0.00" from="S1" to="-N4" end="200.00" number="50"/>

    <trip id="b0" type="bus1" depart="50.00" from="C10" to="-N1"/>
    <trip id="b1" type="bus1" depart="100.00" from="C10" to="-N1"/>
    <trip id="b2" type="bus1" depart="150.00" from="C10" to="-N1"/>
    <trip id="b3" type="bus1" depart="200.00" from="C10" to="-N1"/>
</routes>
```

Simulate the results
```sh
sumo-gui -n stolpedalsvej2.net.xml -r routes1.rou.xml
```

![](doc/routes1.gif)

### Random trips for cyclists
Lets add cyclists using `randomTrips.py` tool described in [this doc]()
Windows version
```python
python "%SUMO_HOME%\tools\randomTrips.py" 
```
macOS/Linux version
```python

```


### Turn data
Lets imagine that instead of simple flows we have vehicle turning ratios a few intersections. 

```xml
<!--in routes3.turn.xml-->
<data>
  <interval id="generated" begin="0.0" end="99.0">
    <edgeRelation from="-58.121.42" to="64" count="1"/>
    <edgeRelation from="-58.121.42" to="-31" count="3"/>
    <edgeRelation from="45" to="-68" count="3"/>
    <edgeRelation from="-31.80.00" to="31" count="1"/>
    <edgeRelation from="-31.80.00" to="37" count="1"/>
    <edgeRelation from="-31.80.00" to="-23" count="13"/>
    <edgeRelation from="-92.180.00" to="-60" count="1"/>
  </interval>
</data>
```









