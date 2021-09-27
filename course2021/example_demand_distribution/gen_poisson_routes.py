import argparse
import xml.etree.ElementTree as ET
from xml.dom import minidom
import numpy as np

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def get_routes_container() -> ET.Element:
    attribs = {
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsi:noNamespaceSchemaLocation": "http://sumo.dlr.de/xsd/routes_file.xsd"
    }
    top = ET.Element("routes", **attribs)
    return top

def get_trip_element(tid, time, efrom, eto, lane="best", prefix="") -> ET.Element:
    """
    Generates
    <trip id="p0" depart="0.00" from="E0" to="E1" departLane="0"/>
    """
    attribs = {
        "id": prefix + str(tid),
        "depart": str(time),
        "from": efrom,
        "to": eto,
        "departLane": str(lane) 
    }
    elm = ET.Element("trip",  **attribs)
    return elm
    
'<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">'
'</routes>'

def main():
    ap = argparse.ArgumentParser("Poisson disributed trip generation")
    ap.add_argument("-b", "--begin", type=int, default=0, help=
        "Trip generation start")
    ap.add_argument("-e", "--end", type=int, default=1000, help=
        "Trip generation end")
    ap.add_argument("-c", "--cars", type=int, default=500, help=
        "Total number of cars in the time interval")
    ap.add_argument("-s", "--source-edge", type=str, help=
        "Starting edge for the demand generation")
    ap.add_argument("-t", "--target-edge", type=str, help=
        "Final edge for the demand generation")
    ap.add_argument("-p", "--prefix", type=str, default="", help=
        "Prefix for vehicle IDs")
    ap.add_argument("-l", "--depart-lane", type=str, default="best", help=
        "Lane to depart from")
    ap.add_argument("-o", "--output", type=str, help=
        "Output file name")
    args = ap.parse_args()
 
    trips = []
    idx = 0

    interval = args.end - args.begin
    lambda_mean = args.cars / interval
    poisson = np.random.poisson(lambda_mean , interval)

    for t in range(args.begin, args.end):
        if poisson[t]:
            for i in range(poisson[t]):
                trip = get_trip_element(idx, t, args.source_edge, args.target_edge, args.depart_lane, args.prefix)
                trips.append(trip)
                idx += 1

    top = get_routes_container()
    top.extend(trips)
    
    with open(args.output, "w") as fout:
        fout.write(prettify(top))

if __name__ == "__main__":
    main()