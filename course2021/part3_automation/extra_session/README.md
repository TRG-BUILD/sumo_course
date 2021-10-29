# Extra Session
Introduction to programming of urban traffic control algorithms.

Max-pressure control, original paper and extensive proofs by [Pravin Varaiya, 2013](DOI:10.1016/j.trc.2013.08.014). A more minimal explanation in a review by [Hua Wei, et al., 2020](https://arxiv.org/abs/1904.08117v3).

Features:
- Calculates "pressure" for each link (stage): using
link queues (+), downstream link queues (  )
- Queues may include arriving (detected) vehicles
- Greedy / memoryless algorithm - winner stage (max pressure) takes all!
- Very simple, decentralized feedback (no optimization problem solution required)
- Theorem (communication networks) proves stabilization, maximum network throughput
- No common cycle time; emerging offset?

Parameters:
- Detector types and sizes: reasonably long area detectors, fx, radars or cameras
- Update frequency: any! (the higher the better)
- Heuristics needed:
    - Whether to base pressure on number of cars visible, a jam with different [proximity thresholds]((https://sumo.dlr.de/docs/Simulation/Output/Lanearea_Detectors_%28E2%29.html#attributes)) or both.
    - to punish lost time due to transitions
    - stage sequence
    - minimum greens
    - pressure component due to cars jammed inside the intersection by right turn prioritizng pedestrians or cyclists, or left turn.
    - weighting factors between phases that contain eachother, fx, in all maneuvers versus left turn the pressure of all maneuvers is always greater or equal to the left turn.