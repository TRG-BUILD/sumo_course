## Exercises 1
### Part 1
- Model an intersection from an assignment with Rasmus
- Generate corresponding demands
- Visualize how the intersection functions without TLS
- Add a pre-timed TLS to the intersection with your phase and durations times and generate tripinfos-output
- Calculate pre-timed TLS with SUMO optimization using https://sumo.dlr.de/docs/Tools/tls.html#tlscycleadaptationpy 
- Compare those 2 scenarios using the trip statistics tool https://sumo.dlr.de/docs/Tools/Output.html#tripstatisticspy

### Part 1 modelling te network
Lets model the network in `netedit` using a background image similar to lecture 1 exercise 2. On upload the image dimensions will be 100 by 100 meters. Lets use lane width hints in the image to recalculate image dimensions so that we draw in the correct units. To do it lets draw a dummy edge next to the lane width measurements and check what edge`s length.

![](doc/howtomeasure.png)

New approximate dimensions are then calculated as follows:

`new_height = (3.0 + 3.0 + 3.0 + 2.4) / 11.22 * 100 = 102 m`

`new_width = (4.0 + 3.0 + 3.5) / 7.73 * 100 = 136 m`


### Demand generation

Difference between route defined and created route displays

![](doc/route_definition.png)

![](doc/created_route.png)

Use `netedit` to define routes, then edit the `*.rou.xml` file to add `flow` with `vehPerHour` parameter according to [this doc]().

resulting `demands.rou.xml` file content is shown below. For better readablity the xml schema verification header and the route color property were ommited.
```xml
<routes>
<!-- in demands.rou.xml -->
    <route edges="fromA1 fromA11 toA22 toA2" id="A1forward"/>
    <route edges="fromA1 fromA11 toB1" id="A1left"/>
    <route edges="fromA1 fromA11 toB22 toB2" id="A1right"/>
    <route edges="fromA2 fromA22 toA11 toA1" id="A2forward"/>
    <route edges="fromA2 fromA22 toB22 toB2" id="A2left"/>
    <route edges="fromA2 fromA22 toB1" id="A2right"/>
    <route edges="fromB1 toB22 toB2" id="B1forward"/>
    <route edges="fromB1 toA22 toA2" id="B1left"/>
    <route edges="fromB1 toA11 toA1" id="B1right"/>
    <route edges="fromB2 fromB22 toB1" id="B2forward"/>
    <route edges="fromB2 fromB22 toA11 toA1" id="B2left"/>
    <route edges="fromB2 fromB22 toA22 toA2" id="B2right"/>
</routes>
```

Now we can add a `vType` and `flow` definitions between `<routes> <\routes>` tags. Up until now we have used a static `vType` and all vehicles had the same characteristics, to come closer to modelling real traffic flow we can use vehicle distributions according to [this doc](https://sumo.dlr.de/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.html#route_and_vehicle_type_distributions)

```xml
<!-- in demands.rou.xml -->
...

    <vTypeDistribution id="dvehicles">
        <vType id="type1" accel="1.8" length="4" maxSpeed="50" color="1,1,0" probability="0.3"/>
        <vType id="type2" accel="2.5" length="5" maxSpeed="60" color="1,0,1" probability="0.5"/>
        <vType id="type3" accel="1.0" length="6" maxSpeed="40" color="0,1,1" probability="0.2"/>
    </vTypeDistribution>

```

Now our custom vehicle type `dvehicles` can be used as a `type` parameter to the `flow` definition.

```xml
<!-- in demands.rou.xml -->
...
    <flow id="fA1left" type="dvehicles" begin="0" end= "3600" vehsPerHour="175" route="A1left">
    <flow id="fA1forward" type="dvehicles" begin="0" end= "3600" vehsPerHour="725" route="A1forward">
    <flow id="fA1right" type="dvehicles" begin="0" end= "3600" vehsPerHour="106" route="A1right">

    <flow id="fB1left" type="dvehicles" begin="0" end= "3600" vehsPerHour="100" route="B1left">
    <flow id="fB1forward" type="dvehicles" begin="0" end= "3600" vehsPerHour="475" route="B1forward">
    <flow id="fB1right" type="dvehicles" begin="0" end= "3600" vehsPerHour="125" route="B1right">

    <flow id="fA2left" type="dvehicles" begin="0" end= "3600" vehsPerHour="17" route="A2left">
    <flow id="fA2forward" type="dvehicles" begin="0" end= "3600" vehsPerHour="497" route="A2forward">
    <flow id="fA2right" type="dvehicles" begin="0" end= "3600" vehsPerHour="253" route="A2right">

    <flow id="fB2left" type="dvehicles" begin="0" end= "3600" vehsPerHour="70" route="B2left">
    <flow id="fB2forward" type="dvehicles" begin="0" end= "3600" vehsPerHour="330" route="B2forward">
    <flow id="fB2right" type="dvehicles" begin="0" end= "3600" vehsPerHour="30" route="B2right">
```

### Part 2:
- Model another similar intersection on the western approach 400 meters away
- Generate new demand that includes western intersection, make sure most of the traffic happens between the intersections
- Experiment with simulating different coordination offsets manually
- Calculate optimal coordination offset with https://sumo.dlr.de/docs/Tools/tls.html#tlscoordinatorpy 

 

## Exercise 2
Using the intersection from Exercise 1 part 1:
- Change the controller to time-gap based and output trip info
- Change the controller to the time loss based and output trip info
- Compare them to the results pre-timed control. 




